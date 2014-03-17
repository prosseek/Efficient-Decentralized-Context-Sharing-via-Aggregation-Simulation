"""context history

Takes care of anything related to context history sent and received

"""

from context.context import Context
from utils import *

class ContextHistory(object):
    """database class"""

    class Container(object):
        """
        This is the information for one timestamp
        old_aggregate_as_set <- Context
        singles <- a dictionary that maps from host_id -> set of contexts of the host_ids
        """
        def __init__(self):
            self.old_aggregate_as_set = set([])
            self.sent_singles = {}
            self.sent_aggregate = {}

    def __init__(self):
        self.context_history = {}

    def get_container(self, timestamp=0):
        """Returns the container for timestamp

        Returned None means that there is no timestamp for it.
        """
        if timestamp in self.context_history:
            return self.context_history[timestamp]
        return None

    def check_and_get_container(self, timestamp=0):
        if timestamp not in self.context_history:
            self.context_history[timestamp] = ContextHistory.Container()
        return self.get_container(timestamp)

    def set_old_aggregate(self, context, timestamp=0):
        """
        WARNING: The aggregate is stored in a set, not in a context form, because we only need the set
        for comparison

        >>> h = ContextHistory()
        >>> h.set_old_aggregate(set([1,2,3]), timestamp=100)
        >>> h.get_container(100).old_aggregate_as_set == set([1,2,3])
        True

        >>> h.set_old_aggregate(Context(value=1.1, cohorts=set([1,2,3])), timestamp=10)
        >>> h.get_container(10).old_aggregate_as_set == set([1,2,3])
        True
        """
        container = self.check_and_get_container(timestamp)
        if type(context) == Context:
            container.old_aggregate_as_set = context.get_cohorts_as_set()
        elif type(context) == set:
            container.old_aggregate_as_set = context


    def get_old_aggregate_as_set(self, timestamp=0):
        """

        >>> h = ContextHistory()
        >>> h.set_old_aggregate(set([1,2,3]), timestamp=100)
        >>> h.get_old_aggregate_as_set(100) == set([1,2,3])
        True

        >>> h.set_old_aggregate(Context(value=1.1, cohorts=set([1,2,3])), timestamp=10)
        >>> h.get_old_aggregate_as_set(100) == set([1,2,3])
        True
        """
        container = self.get_container(timestamp)
        if container is None:
            return set()
        else:
            return container.old_aggregate_as_set

    def sent(self, index, contexts, timestamp=0):
        """
        >>> h = ContextHistory()
        >>> h.sent(1, [[1],[2],[3],[4,5,6,7]], timestamp=10)
        >>> h.context_history[10].sent_singles[1] == set([1,2,3])
        True
        >>> h.context_history[10].sent_aggregate[1] == set([4,5,6,7])
        True
        """
        singles = set([])
        aggregate = set([])
        for c in contexts:
            if type(c) is Context:
                if c.is_single():
                    singles = singles.union(c.get_cohorts_as_set())
                else:
                    aggregates = c.get_cohorts_as_set()
            elif type(c) in [list, set]:
                c = list(c)
                if len(c) == 1:
                    singles.add(c[0])
                else:
                    aggregate = aggregate.union(c)
        self.set_sent_singles(index, singles, timestamp)
        self.set_sent_aggregate(index, aggregate, timestamp)


    def set_sent_singles(self, index, singles, timestamp=0):
        """Sets the singles as input of a list of Contexts to store it corresponding history

        >>> h = ContextHistory()
        >>> h.set_sent_singles(1, set([Context(value=1.0, cohorts=[1]), Context(value=2.0, cohorts=[2])]), timestamp=10)
        >>> h.set_sent_singles(2, set([Context(value=1.0, cohorts=[3]), Context(value=2.0, cohorts=[2])]), timestamp=10)
        >>> # When the index is wrong, it returns null set
        >>> h.context_history[10].sent_singles[1] == set([1,2])
        True
        >>> h.context_history[10].sent_singles[2] == set([3,2])
        True
        >>> h.context_history[10].sent_singles[0]
        Traceback (most recent call last):
            ...
        KeyError: 0
        """
        container = self.check_and_get_container(timestamp)
        result = set()
        for c in singles:
            if type(c) is Context:
                s = list[c.get_cohorts_as_set()]
                assert len(s) == 1
                s = s[0]
            else:
                # [1,2,3] <- context with cohorts 1, 2, and 3
                s = c
            result.add(s)
        container.sent_singles[index] = result

    def get_sent_singles(self, index = None, timestamp=0):
        """
        >>> h = ContextHistory()
        >>> h.set_sent_singles(1, set([Context(value=1.0, cohorts=[1]), Context(value=2.0, cohorts=[2])]), timestamp=10)
        >>> h.set_sent_singles(2, set([Context(value=1.0, cohorts=[3]), Context(value=2.0, cohorts=[2])]), timestamp=10)
        >>> # When the index is wrong, it returns null set
        >>> h.get_sent_singles(index=0, timestamp=10)
        set([])
        >>> h.get_sent_singles(index=1, timestamp=10) == set([1, 2])
        True
        >>> h.get_sent_singles(index=2, timestamp=10) == set([2, 3])
        True
        """
        container = self.get_container(timestamp)
        if container is None: return set()

        if index is None:
            return container.sent_singles
        else:
            if index in container.sent_singles:
                return container.sent_singles[index]
            else:
                return set()

    def set_sent_aggregate(self, index, context, timestamp=0):
        """Sets the singles as input of a list of Contexts to store it corresponding history

        >>> h = ContextHistory()
        >>> h.set_sent_aggregate(1, Context(value=1.0, cohorts=[1,3,4]), timestamp=10)
        >>> h.set_sent_aggregate(2, set([1,3,4]), timestamp=10)
        >>> # When the index is wrong, it returns null set
        >>> h.context_history[10].sent_aggregate[1] == set([1,3,4])
        True
        >>> h.context_history[10].sent_aggregate[2] == set([1,3,4])
        True
        >>> h.context_history[10].sent_aggregate[0]
        Traceback (most recent call last):
            ...
        KeyError: 0
        """
        container = self.check_and_get_container(timestamp)
        if type(context) is Context:
            container.sent_aggregate[index] = context.get_cohorts_as_set()
        else:
            container.sent_aggregate[index] = set(context)

    def get_sent_aggregate(self, index = None, timestamp=0):
        """
        >>> h = ContextHistory()
        >>> h.set_sent_aggregate(1, Context(value=1.0, cohorts=[1,3,2]), timestamp=10)
        >>> h.set_sent_aggregate(2, Context(value=1.0, cohorts=[1,3,2]), timestamp=10)
        >>> # When the index is wrong, it returns null set
        >>> h.get_sent_aggregate(index=0, timestamp=10)
        set([])
        >>> h.get_sent_aggregate(index=1, timestamp=10) == set([1, 3, 2])
        True
        >>> h.get_sent_aggregate(index=2, timestamp=10) == set([2, 3, 1])
        True
        """
        container = self.get_container(timestamp)
        if container is None: return set()

        if index is None:
            return container.sent_aggregate
        else:
            if index in container.sent_aggregate:
                return container.sent_aggregate[index]
            else:
                return set()

    #
    # Utility
    #

    def is_new_aggregate_and_set(self, context,timestamp=0):
        if self.is_new_aggregate(context):
            self.set_old_aggregates(context)
            return True
        return False

    def is_new_aggregate(self, context, timestamp=0):
        """Check if context has new information

        >>> h = ContextHistory()
        >>> h.set_old_aggregate(Context(value=1.0, cohorts=[1,2,3]), timestamp=10)
        >>> h.is_new_aggregate(Context(value=1.0, cohorts=[1,2,3]), timestamp=10)
        False
        >>> h.is_new_aggregate(None, timestamp=10)
        Traceback (most recent call last):
            ...
        AssertionError
        >>> h.is_new_aggregate(Context())
        Traceback (most recent call last):
            ...
        AssertionError
        >>> h.is_new_aggregate(Context(value=2.0, cohorts=[1,2,3,4]), timestamp=10)
        True
        >>> h.is_new_aggregate(Context(value=2.0, cohorts=[2,3,4,5,6,7]), timestamp=10)
        False
        >>> h.is_new_aggregate(Context(value=2.0, cohorts=[2,3]), timestamp=10)
        False
        """
        assert context is not None
        s = context.get_cohorts_as_set()
        assert s != set([])

        container = self.get_container(timestamp)

        # When there is no self.context_history[timestamp], it means that
        # We sent nothing at this timestamp
        if container is None: return True

        old_aggregate_as_set = container.old_aggregate_as_set
        if old_aggregate_as_set == set([]):
            return True

        o = old_aggregate_as_set

        if s > o:
            container.old_aggregate_as_set = s
            return True
        return False

    def calculate_output_for_aggregates(self, new_aggregates, inputs, timestamp=0):
        """
        Input:
            new_aggregates: newly generated aggregate
            inputs: a dictionary of "input:set of contexts",
        calculate what neighbors should be sent what a set of contexts

        >>> # case1. When there is no history of sending information, return {}
        >>> h = ContextHistory()
        >>> new_aggregate = Context(value=1.0, cohorts=[1,2,3])
        >>> r = h.calculate_output_for_aggregates(new_aggregate, {1:set([Context(value=1.0, cohorts=[1,2])]), 2:set([Context(value=1.0, cohorts=[2,3])])})
        >>> r[1].get_cohorts_as_set() == set([1,2,3])
        True
        >>> r[2].get_cohorts_as_set() == set([1,2,3])
        True
        """
        # check new inputs first
        assert type(new_aggregates) == Context

        new_cohorts = new_aggregates.get_cohorts_as_set()

        # Check the inputs
        result = {}
        for i in inputs:
            # {1: set([context ... } -> 1:...
            contexts = inputs[i]
            # set([...
            for context in contexts:
                # When the context is aggregated
                # Assumption: There is only one aggregate
                if not context.is_single():
                    result[i] = context.get_cohorts_as_set()
                else: # even though there is no aggregate, set none to get comparison
                    result[i] = set([])

        # Check all the previous aggregates that was sent
        try:
            container = self.context_history[timestamp]
            for i in container.sent_aggregate:
                sent_set = container.sent_aggregate[i]
                if i in result: # If index i already sent aggregates before
                    result[i] = result[i].union(sent_set)
                else:
                    result[i] = sent_set
        except KeyError: # no context_history[timestamp]
            pass

        # Finally, send the dictionary {1:Context ...} only when there is something to send
        final_result = {}
        for i in result:
            # from the new cohorts remove all the elements sent or received just now
            result[i] = new_cohorts - result[i]
            if result[i]: # remove {1:set([])...}
                final_result[i] = new_aggregates

        return final_result

    @staticmethod
    def filter_not_sent_singles(single_set, context_set):
        """Return only the context_set that has the element in the single set
        >>> single_set = set([1,2])
        >>> context_set = set([Context(value=1.0, cohorts=[1])])
        >>> r = ContextHistory.filter_not_sent_singles(single_set, context_set)
        >>> compare_contexts_and_cohorts(r, [[1]])
        True
        """
        result = set()
        for c in context_set:
            l = list(c.get_cohorts_as_set())
            assert(len(l) == 1)
            if l[0] in single_set:
                result.add(c)
        return result

    def calculate_output_for_singles(self, new_singles, inputs, timestamp=0):
        """
        >>> h = ContextHistory()
        >>> new_contexts =set([Context(value=1.0, cohorts=[1]), Context(value=2.0, cohorts=[2])])
        >>> r = h.calculate_output_for_singles(new_contexts, {1:set([Context(value=1.0, cohorts=[1])])})
        >>> 2 not in r
        True
        >>> # From single contexts 1 and 2, only 2 is the new information
        >>> compare_contexts_and_cohorts(r[1], [[2]])
        True
        """
        # check new inputs first
        singles_as_set = set()
        for c in new_singles:
            singles_as_set = singles_as_set.union(c.get_cohorts_as_set())
        # Check the inputs
        result = {}
        for i in inputs:
            # {1: set([context ... } -> 1:... multiple single contexts
            contexts = inputs[i]
            # set([... only for index i
            for context in contexts:
                # When multiple single contexts are coming
                if context.is_single():
                    if i in result:
                        result[i] = result[i].union(context.get_cohorts_as_set())
                    else:
                        result[i] = context.get_cohorts_as_set()
                else:
                    result[i] = set()

        # Check all the previous aggregates that was sent
        try:
            container = self.context_history[timestamp]
            for i in container.sent_singles:
                sent_set = container.sent_singles[i]
                if i in result: # If index i already sent aggregates before
                    result[i] = result[i].union(sent_set)
                else:
                    result[i] = sent_set
        except KeyError: # no context_history[timestamp]
            pass

                # Finally, send the dictionary {1:Context ...} only when there is something to send
        final_result = {}
        for i in result:
            # from the new cohorts remove all the elements sent or received just now
            result[i] = singles_as_set - result[i]
            if result[i]: # remove {1:set([])...}
                not_sent_singles = ContextHistory.filter_not_sent_singles(result[i], new_singles)
                final_result[i] = not_sent_singles

        return final_result

    def calculate_output(self, contexts, inputs, timestamp=0):
        """Given a set of contexts filtered and inputs, calculate the output directory

        >>> h = ContextHistory()
        >>> contexts =set([Context(value=1.0, cohorts=[1]), Context(value=2.0, cohorts=[2]), Context(value=3.0, cohorts=[3,4,5,6])])
        >>> inputs={1:set([Context(value=1.0, cohorts=[1])])}
        >>> r = h.calculate_output(contexts=contexts, inputs=inputs)
        >>> compare_contexts_and_cohorts(r[1], [[2],[3,4,5,6]])
        True
        """
        singles = set()
        for c in contexts:
            if c.is_single():
                singles.add(c)
            else:
                aggregate = c

        single_results = self.calculate_output_for_singles(singles, inputs, timestamp)
        aggregate_results = self.calculate_output_for_aggregates(aggregate, inputs, timestamp)
        final_result = {}
        for s in single_results:
            final_result[s] = single_results[s]
        for a in aggregate_results:
            if a in final_result:
                final_result[a].add(aggregate_results[a])
            else:
                final_result[a] = set([aggregate_results[a]])
        return final_result

if __name__ == "__main__":
    import doctest
    doctest.testmod()

