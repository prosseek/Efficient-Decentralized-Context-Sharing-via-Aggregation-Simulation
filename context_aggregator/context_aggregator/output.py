"""input

"""

from inputoutput import InputOutput
from utils import get_matching_single_contexts, empty_dictionary

class Output(InputOutput):
    """Output is a dictionary format what to send

    However, it's dictionary is in standard format([[],[]]) not in
    context format.

    As a result, some of the methods are overridden.
    """
    def __init__(self):
        self.dictionary = {}
        self.actual_sent_dictionary = {}

    def set_dictionary(self, dictionary):
        self.dictionary = dictionary
        self.actual_sent_dictionary = {}

    def to_string(self, dictionary = None):
        """to_string for output object

        We can't use the parent's to_string, because output's element is list, when inputout's
        element is Context
        """

        if dictionary is None:
            dictionary = self.dictionary
        else:
            dictionary = self.actual_sent_dictionary

        if empty_dictionary(dictionary):
            return "{}"
        return "%s" % dictionary

    def get_number_of_contexts_from_dictionary(self, dictionary):
        """

        [[1,2,3][4,5,6]] -> only 4 not 6, as aggregated context count as 1
        """
        s = 0
        a = 0
        d = dictionary
        if d is not None:
            for key, values in d.items():
                s += len(values[0])
                a += 1 if len(values[1]) > 1 else 0
        return s,a

    def get_number_of_contexts(self):
        """

        [[1,2,3][4,5,6]] -> only 4 not 6, as aggregated context count as 1
        """
        return self.get_number_of_contexts_from_dictionary(self.dictionary)

    def get_number_of_actual_sent_contexts(self):
        return self.get_number_of_contexts_from_dictionary(self.actual_sent_dictionary)

    def generate_single_contexts(self, o, single_contexts):
        singles = self.dictionary[o][0]
        single_contexts = get_matching_single_contexts(single_contexts, singles)
        return single_contexts

    def generate_aggregate_contexts(self, o, aggregate_contexts):
        aggregate = self.dictionary[o][1]
        if aggregate:
            # aggregate should be turned into set(), so you need to convert it into list first
            aggregate = [aggregate_contexts]
        return set(aggregate)

if __name__ == "__main__":
    import doctest
    doctest.testmod()


