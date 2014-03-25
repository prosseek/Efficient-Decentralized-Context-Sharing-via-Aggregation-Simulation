"""input

"""

from context.context import Context
from inputoutput import InputOutput
from utils_standard import contexts_to_standard

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

    def to_string(self):
        result = {}
        for i, value in self.dictionary.items():
            result[i] = contexts_to_standard(value)
        return str(result)

    def get_senders(self):
        """

        >>> c = Input()
        >>> c[1] = {Context(value=1.0, cohorts=[0,1,2])}
        >>> c[2] = {Context(value=1.0, cohorts=[0,1,2,4])}
        >>> set(c.get_senders()) == set([1,2])
        True
        """
        return self.dictionary.keys()

    def get_number_of_contexts(self):
        """

        >>> c = Input()
        >>> c[1] = {Context(value=1.0, cohorts=[0])}
        >>> c[2] = {Context(value=1.0, cohorts=[0,1,2,4])}
        >>> c.get_number_of_contexts() == (1,1)
        True
        """
        single_result = 0
        aggr_result = 0
        for key, values in self.dictionary.items():
            for value in values:
                if value.is_single():
                    single_result += 1
                else:
                    aggr_result += 1
        return single_result, aggr_result

if __name__ == "__main__":
    import doctest
    doctest.testmod()


