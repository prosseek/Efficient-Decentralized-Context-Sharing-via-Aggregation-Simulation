"""context history

Takes care of anything related to context history sent and received

"""

from context.context import Context

class ContextHistory(object):
    """database class"""

    def __init__(self):
        self.reset()
        self.old_context = None

    def reset(self):
        self.context_history = {}

    def get(self, key, timestamp=0):
        """

        >>> o = ContextHistory()
        >>> # Return returned when there is no corresponding element -> KeyError
        >>> o.get(3)
        """
        try:
            return self.context_history[timestamp][key]
        except KeyError:
            return None

    def update(self, key, value, timestamp=0):
        """

        >>> c = ContextHistory()
        >>> c.update(1, Context(value=1.0, cohorts=[0,1,2]))
        >>> context = c.get(1)
        >>> context.value == 1.0 and context.get_cohorts_as_set() == set([0,2,1])
        True
        """
        if timestamp not in self.context_history:
            self.context_history[timestamp] = {}
        self.context_history[timestamp][key] = value

    #
    # Utility
    #
    def set_old_context(self, context):
        self.old_context = context

    def is_new_info_and_set(self, context):
        if self.is_new_info(context):
            self.set_old_context(context)
            return True
        return False

    def is_new_info(self, context):
        """Check if context has new information

        #TODO - check also the time tag

        >>> h = ContextHistory()
        >>> h.set_old_context(Context(value=1.0, cohorts=[1,2,3]))
        >>> h.is_new_info(Context(value=1.0, cohorts=[1,2,3]))
        False
        >>> h.is_new_info(None)
        Traceback (most recent call last):
            ...
        AssertionError
        >>> h.is_new_info(Context())
        Traceback (most recent call last):
            ...
        AssertionError
        >>> h.is_new_info(Context(value=2.0, cohorts=[1,2,3,4]))
        True
        >>> h.is_new_info(Context(value=2.0, cohorts=[2,3,4,5,6,7]))
        False
        >>> h.is_new_info(Context(value=2.0, cohorts=[2,3]))
        False
        """
        assert context is not None
        s = context.get_cohorts_as_set()
        assert s != set([])

        if self.old_context is None:
            return True
        o = self.old_context.get_cohorts_as_set()

        if s > o:
            self.old_context = context
            return True
        return False

    def calculate_output(self, new_aggregates, inputs, timestamp=0):
        """
        Input:
            new_aggregates: newly generated aggregate
            inputs: a dictionary of "input:set of contexts",
        calculate what neighbors should be sent what a set of contexts
        >>> h = ContextHistory()
        >>> new_aggregate = Context(value=1.0, cohorts=[1,2,3])
        >>> h.calculate_output(new_aggregate, None)
        """
        # history_at_timestamp = self.context_history[timestamp]
        # if history_at_timestamp is None:
        #     # there is no sent history
        #     return {}
        # for key, values in .items():
        #     # i is a dictionary of "node:a set of context"
        #     print key
        #     print values
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()


