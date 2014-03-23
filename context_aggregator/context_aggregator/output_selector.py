"""
The algorithm is based on - http://wiki.rubichev/contextAggregation/research/think/context_history/

Assume:

1. In this module, we only assume all the contexts are representd in standard format.

"""
from context_history import ContextHistory
from copy import copy
from utils_standard import add_standards
from utils import same

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

        >>> dictionary = {1:[[1,2,3],[3,4,5,6,7]], 2:[[2,3,4],[5,6,7]]}
        >>> new_info = [[3,4,5],[3,4,5,6,7]]
        >>> r = OutputSelector.select_hosts_to_send_contexts(dictionary=dictionary, new_info=new_info)
        >>> r[0]
        Traceback (most recent call last):
            ...
            r[0]
        KeyError: 0
        >>> same(r[1], [[4,5],[]])
        True
        >>> same(r[2], [[5],[3,4,5,6,7]])
        True
        """
        result = {}
        for d in dictionary:
            singles = dictionary[d][0]
            doubles = dictionary[d][1]

            # we need to find only the singles that we didn't send
            singles_new_info = sorted(list(set(new_info[0]) - set(singles)))
            # when new info in not new, we have nothing to send, otherwise we have all to send
            doubles_new_info = new_info[1] if set(new_info[1]) > set(doubles) else []

            result[d] = [singles_new_info, doubles_new_info]

        return result

    def run(self, timestamp=0):
        """
        >>> inputs = {0:[[1,2,3],[3,4,5]], 1:[[1,2],[3,4,5,6]]}
        >>> input = [[4,5],[3,4,5,6,7]]
        >>> h =ContextHistory()
        >>> h.set_history(1, input)
        >>> h.set_history(3, input)
        >>> new_info = [[1,2,3,4,5],[3,4,5,6,7,8]]
        >>> o = OutputSelector(inputs=inputs, context_history=h, new_info=new_info)
        >>> r = o.run()
        >>> #same(r, {0:[[1,2,3],[3,4,5]], 1:[[1,2,4,5],[3,4,5,6,7]], 3:[[4,5],[3,4,5,6,7]]}) # combined
        >>> r
        True
        """
        output = {}

        # add inputs and history
        history_at_timestamp = self.context_history.get(timestamp)
        combined = OutputSelector.add_standards_in_dictionary(self.inputs, history_at_timestamp)
        selection = OutputSelector.select_hosts_to_send_contexts(dictionary=combined, new_info = self.new_info)
        return selection

if __name__ == "__main__":
    import doctest
    doctest.testmod()
