"""output

"""

from inputoutput import InputOutput

class Output(InputOutput):
    """database class"""

    """database class

    >>> i = Output()
    >>> i[10] = Context(value=1.0, cohorts=[1,2,3])
    >>> i[10].value
    1.0
    >>> i[20] # None will be returned
    >>> i.reset()
    """

    def __init__(self):
        self.dictionary = {}

if __name__ == "__main__":
    import doctest
    doctest.testmod()


