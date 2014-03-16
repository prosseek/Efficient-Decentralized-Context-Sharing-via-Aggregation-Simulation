"""output

"""

from inputoutput import InputOutput
from utils import same

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

    def combine_outputs(self, single_dictionary, aggregate_dictionary):
        """combine two dictionaries into one

        >>> s = {"a":10, "b":20, "c":30}
        >>> a = {"a":20, "c":40, "d":50}
        >>> o = Output()
        >>> o.combine_outputs(s, a)
        >>> same(o.dictionary,{'a': set([10, 20]), 'c': set([40, 30]), 'b': set([20]), 'd': set([50])})
        True

        """
        for i in single_dictionary:
            if i not in self.dictionary:
                self.dictionary[i] = set()
            self.dictionary[i].add(single_dictionary[i])
        for i in aggregate_dictionary:
            if i not in self.dictionary:
                self.dictionary[i] = set()
            self.dictionary[i].add(aggregate_dictionary[i])

if __name__ == "__main__":
    import doctest
    doctest.testmod()


