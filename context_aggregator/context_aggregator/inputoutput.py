"""output

"""

from context.context import Context
from utils_standard import contexts_to_standard
from utils import is_empty_dictionary

class InputOutput(object):
    """database class"""

    def __init__(self):
        self.reset()

    def get_dictionary(self):
        return self.dictionary

    def set_dictionary(self, dictionary):
        self.dictionary = dictionary

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
        >>> c[1] = {Context(value=1.0, cohorts=[0,1,2])}
        >>> con = list(c[1])[0]
        >>> con.value == 1.0 and con.get_cohorts_as_set() == set([0,2,1])
        True
        """
        self.dictionary[key] = value

    def to_string(self):
        result = {}
        for i, value in self.dictionary.items():
            result[i] = contexts_to_standard(value)
        if is_empty_dictionary(result): return "{}"
        return str(result)

    def get_senders(self):
        """

        >>> c = InputOutput()
        >>> c[1] = {Context(value=1.0, cohorts=[0,1,2])}
        >>> c[2] = {Context(value=1.0, cohorts=[0,1,2,4])}
        >>> set(c.get_senders()) == set([1,2])
        True
        """
        return self.dictionary.keys()

    def get_number_of_contexts(self):
        """

        >>> c = InputOutput()
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

    def get_in_standard_from(self):
        """

        >>> c = InputOutput()
        >>> c[1] = {Context(value=1.0, cohorts=[0])}
        >>> c[2] = {Context(value=1.0, cohorts=[0,1,2,4])}
        >>> c.get_in_standard() == {1: [[0], []], 2: [[], [0, 1, 2, 4]]}
        True
        """
        results = {}
        for key, value in self.dictionary.items():
            results[key] = contexts_to_standard(value)
        return results

if __name__ == "__main__":
    import doctest
    doctest.testmod()