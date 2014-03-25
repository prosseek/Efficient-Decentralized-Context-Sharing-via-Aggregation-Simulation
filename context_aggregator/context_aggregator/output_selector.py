"""
The algorithm is based on - http://wiki.rubichev/contextAggregation/research/think/context_history/

Assumptions:

* In this module, we only assume all the contexts are representd in standard format.

"""
from context_history import ContextHistory
from utils_standard import add_standards
from utils_same import same

class OutputSelector(object):
    def __init__(self, inputs=None, context_history=None, new_info=None, neighbors=None):
        self.inputs = inputs
        self.context_history = context_history
        self.new_info = new_info
        self.neighbors = neighbors

    @staticmethod
    def add_standards_in_dictionary(in1, in2):
        """

        >>> r1 = {1:[[1,2,3],[4,5,6]], 2:[[3,4,5],[6,7,8]], 3:[[4,5,7],[1]]}
        >>> r2 = {2:[[1,2,3],[8,9,10]], 3:[[7,8,9],[]], 4:[[1,2,3],[5,6,7]]}
        >>> r = OutputSelector.add_standards_in_dictionary(r1, r2)
        >>> expect = {1:[[1,2,3],[4,5,6]], 2:[[1,2,3,4,5],[6,7,8,9,10]], 3:[[4,5,7,8,9],[1]], 4:[[1,2,3],[5,6,7]]}
        >>> same(r, expect)
        True
        """
        assert type(in1) is dict and type(in2) is dict
        keys1 = in1.keys()
        keys2 = in2.keys()

        result = {}
        for k in keys1:
            if k in keys2:
                keys2.remove(k)
                result[k] = add_standards(in1[k], in2[k])
            else:
                result[k] = in1[k]

        for k in keys2:
            result[k] = in2[k]

        return result

    @staticmethod
    def select_hosts_to_send_contexts(dictionary, new_info):
        """Given combined dictionary, comparing it with new_info
        to select the hosts to send the new_info.

        The returned value is a dictionary that maps host -> standard contexts.
        The standard can be consists of singles or aggregate only.

        >>> dictionary = {1:[[1,2,3],[3,4,5,6,7]], 2:[[2,3,4],[5,6,7]], 3:[[],[3,4]]}
        >>> new_info = [[3,4,5],[3,4,5,6,7]]
        >>> r = OutputSelector.select_hosts_to_send_contexts(dictionary=dictionary, new_info=new_info)
        >>> r[0]
        Traceback (most recent call last):
            ...
            r[0]
        KeyError: 0
        >>> same(r[1], [[4,5],[]])
        True
        >>> same(r[2], [[5],[]]) # 2,3,4+5,6,7 is already known to r[2], so nothing to send for aggr
        True
        >>> same(r[3], [[3,4,5],[3,4,5,6,7]])
        True
        """
        result = {}
        for d in dictionary:
            singles = dictionary[d][0]
            aggregate = dictionary[d][1]

            # we need to find only the singles that we didn't send
            singles_new_info = sorted(list(set(new_info[0]) - set(singles)))
            # when new info in not new, we have nothing to send, otherwise we have all to send
            new_aggregate_info = set(new_info[1])
            old_aggregate_info = set(aggregate) | set(singles)
            aggregate_new_info = new_info[1] if new_aggregate_info > old_aggregate_info else []

            result[d] = [singles_new_info, aggregate_new_info]

        return result

    def run(self):
        """

        ## selection example:
        new info -> [[1,2,3,4,5],[3,4,5,6,7,8]]

        node 0:
        input only -> [[1,2,3],[3,4,5]]
        selection -> [[4,5],[3,4,5,6,7,8]]

        node 1:
        new input -> [[1,2],[3,4,5,6]]
        history -> [[4,5],[3,4,5,6,7]]
        combined -> [[1,2,4,5],[3,4,5,6,7]]
        selection -> [[3],[3,4,5,6,7,8]]

        node 3:
        only history -> [[4,5],[3,4,5,6,7]]
        selection -> [[1,2,3],[3,4,5,6,7,8]]

        ## final example
        neighbors = [0,3,4]

        From the result, 1 should be missed out, and 4 should be added
        0: [[4, 5], [3, 4, 5, 6, 7, 8]]
        <- 1 is missed out
        3: [[1, 2, 3], [3, 4, 5, 6, 7, 8]]
        4: [[1, 2, 3, 4, 5], [3, 4, 5, 6, 7, 8]] <-- all the new info

        >>> inputs = {0:[[1,2,3],[3,4,5]], 1:[[1,2],[3,4,5,6]]}
        >>> input = [[4,5],[3,4,5,6,7]]
        >>> h = {1:input, 3:input}
        >>> new_info = [[1,2,3,4,5],[3,4,5,6,7,8]]
        >>> neighbors = [0,3,4]
        >>> o = OutputSelector(inputs=inputs, context_history=h, new_info=new_info, neighbors=neighbors)
        >>> r = o.run()
        >>> # combined
        >>> #same(r, {0:[[1,2,3],[3,4,5]], 1:[[1,2,4,5],[3,4,5,6,7]], 3:[[4,5],[3,4,5,6,7]]})
        >>> # after selection
        >>> # same(r, {0: [[4, 5], [3, 4, 5, 6, 7, 8]], 1: [[3], [3, 4, 5, 6, 7, 8]], 3: [[1, 2, 3], [3, 4, 5, 6, 7, 8]]})
        >>> # TODO, # I didn't check this thoroughly, so check it out
        >>> same(r,{0: [[4, 5], []], 3: [[1, 2, 3], [3, 4, 5, 6, 7, 8]], 4: [[1, 2, 3, 4, 5], [3, 4, 5, 6, 7, 8]]})
        True
        """
        assert self.inputs is not None
        assert self.context_history is not None
        assert self.new_info is not None
        output = {}

        # add inputs and history
        #history_at_timestamp = self.context_history.get(timestamp)
        combined = OutputSelector.add_standards_in_dictionary(self.inputs, self.context_history)
        selection = OutputSelector.select_hosts_to_send_contexts(dictionary=combined, new_info = self.new_info)

        if self.neighbors is not None:
            for n in self.neighbors:
                if n in selection:
                    output[n] = selection[n]
                else:
                    output[n] = self.new_info
        else:
            output = selection

        return output

if __name__ == "__main__":
    import doctest
    doctest.testmod()
