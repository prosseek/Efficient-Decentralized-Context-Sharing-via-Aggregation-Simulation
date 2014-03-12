"""context history

"""

class ContextHistory(object):
    """database class"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.context_history = {}

    def __getitem__(self, key):
        """

        >>> o = ContextHistory()
        >>> # Return returned when there is no corresponding element -> KeyError
        >>> o[3]
        """
        try:
            return self.context_history[key]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        """

        >>> c = ContextHistory()
        >>> c[1] = context.Context(value=1.0, cohorts=[0,1,2])
        >>> context = c[1]
        >>> context.value == 1.0 and context.get_cohorts_as_set() == set([0,2,1])
        True
        """
        self.context_history[key] = value

if __name__ == "__main__":
    import doctest
    doctest.testmod()


