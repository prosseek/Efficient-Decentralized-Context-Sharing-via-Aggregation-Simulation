"""filtered context database

"""
import copy
from utils import *

from disaggregator import Disaggregator
from maxcover import MaxCover

import gc

class FilteredContextDatabase(object):
    """database class"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.filtered_context_database = {}

if __name__ == "__main__":
    import doctest
    doctest.testmod()


