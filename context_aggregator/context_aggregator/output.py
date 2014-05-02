"""input

"""

from inputoutput import InputOutput
from utils import get_matching_single_contexts, is_empty_dictionary, get_matching_aggregate_contexts
from utils_standard import *

class Output(InputOutput):
    """Output is a dictionary format what to send; However, it's dictionary is in standard format([[],[]]) not in
    context format. As a result, some of the methods are overridden.

    """
    def __init__(self):
        self.dictionary = {}
        self.actual_sent_dictionary = {}

    def get_singles(self, id):
        """
        >>> o = Output()
        >>> o.set_dictionary({1:[[1,2],[3,4]]})
        >>> o.get_singles(1) == [1,2]
        True
        >>> o.get_aggregates(1) == [3,4]
        """
        assert id in self.dictionary
        return self.dictionary[id][0]

    def get_aggregates(self, id):
        assert id in self.dictionary
        return self.dictionary[id][1]

    def set_dictionary(self, dictionary):
        """
        >>> o = Output()
        >>> o.set_dictionary({1:[[],[]]})
        >>> o.get_dictionary() == {}
        True
        >>> o.set_dictionary({})
        >>> o.get_dictionary() == {}
        True
        >>> o.set_dictionary({1:[[1],[]]})
        >>> o.get_dictionary() == {1:[[1],[]]}
        True
        """
        # You can set {} to the output dictionary, but as long as it's not empty the input should be in standard form
        if dictionary != {}:
            assert is_dictionary_standard(dictionary), "dictionary is not in standard form %s" % dictionary

        # When dictionary is empty, make it explicitly null
        if is_empty_dictionary(dictionary):
            dictionary = {}

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

        if is_empty_dictionary(dictionary):
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
        singles = self.get_singles(o) # dictionary[o][0]
        single_contexts = get_matching_single_contexts(single_contexts, singles)
        return single_contexts

    def generate_aggregate_contexts(self, o, aggregate_contexts):
        # print aggregate_contexts
        # This is output class, and we need to find the context that has aggregate as a cohort in it
        aggregate = self.get_aggregates(o) # returns [...]
        aggregate_contexts = get_matching_aggregate_contexts(aggregate_contexts, aggregate)
        return aggregate_contexts

    def is_empty(self):
        """
        >>> r = Output()
        >>> r.is_empty()
        True
        """
        return is_empty_dictionary(self.dictionary)

if __name__ == "__main__":
    import doctest
    doctest.testmod()


