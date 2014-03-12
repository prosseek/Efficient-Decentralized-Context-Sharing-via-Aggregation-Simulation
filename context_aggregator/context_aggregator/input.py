"""input

"""
import copy
from utils import *

from disaggregator import Disaggregator
from maxcover import MaxCover

import gc

class Input(object):
    """database class"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.input_dictionary = {}

    def __getitem__(self, key):
        """

        >>> i = Input()
        >>> # Return returned when there is no corresponding element -> KeyError
        >>> i[3]
        """
        try:
            return self.input_dictionary[key]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        """

        >>> c = Input()
        >>> c[1] = context.Context(value=1.0, cohorts=[0,1,2])
        >>> context = c[1]
        >>> context.value == 1.0 and context.get_cohorts_as_set() == set([0,2,1])
        True
        """
        self.input_dictionary[key] = value
    #
    # def set_context_database(self):
    #     pass
    #
    # def reset_input_dictionary(self):
    #     self.input_dictionary = {}

if __name__ == "__main__":
    import doctest
    doctest.testmod()


