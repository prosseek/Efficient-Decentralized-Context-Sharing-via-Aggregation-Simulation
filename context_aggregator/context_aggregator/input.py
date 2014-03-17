"""input

"""

from context.context import Context
from inputoutput import InputOutput

class Input(InputOutput):
    """database class

    >>> i = Input()
    >>> i[10] = Context(value=1.0, cohorts=[1,2,3])
    >>> i[10].value
    1.0
    >>> i[20] # None will be returned
    >>> i.reset()
    """

    def __init__(self):
        self.dictionary = {}

    def get_dictionary(self):
        return self.dictionary

    def get_senders(self):
        """

        >>> c = Input()
        >>> c[1] = Context(value=1.0, cohorts=[0,1,2])
        >>> c[2] = Context(value=1.0, cohorts=[0,1,2,4])
        >>> set(c.get_senders()) == set([1,2])
        True
        """
        return self.dictionary.keys()

if __name__ == "__main__":
    import doctest
    doctest.testmod()


