"""output

"""

from context.context import Context

class InputOutput(object):
    """database class"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.dictionary = {}

    def __getitem__(self, key):
        """

        >>> o = InputOutput()
        >>> # Return returned when there is no corresponding element -> KeyError
        >>> o[3]
        """
        try:
            return self.dictionary[key]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        """

        >>> c = InputOutput()
        >>> c[1] = Context(value=1.0, cohorts=[0,1,2])
        >>> con = c[1]
        >>> con.value == 1.0 and con.get_cohorts_as_set() == set([0,2,1])
        True
        """
        self.dictionary[key] = value

if __name__ == "__main__":
    import doctest
    doctest.testmod()


