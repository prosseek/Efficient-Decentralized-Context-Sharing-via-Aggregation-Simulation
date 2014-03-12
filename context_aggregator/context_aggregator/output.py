"""output

"""

class Output(object):
    """database class"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.output_dictionary = {}

    def __getitem__(self, key):
        """

        >>> o = Output()
        >>> # Return returned when there is no corresponding element -> KeyError
        >>> o[3]
        """
        try:
            return self.output_dictionary[key]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        """

        >>> c = Output()
        >>> c[1] = context.Context(value=1.0, cohorts=[0,1,2])
        >>> context = c[1]
        >>> context.value == 1.0 and context.get_cohorts_as_set() == set([0,2,1])
        True
        """
        self.output_dictionary[key] = value

if __name__ == "__main__":
    import doctest
    doctest.testmod()


