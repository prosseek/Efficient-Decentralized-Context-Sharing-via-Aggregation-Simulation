"""context database

Context database stores **all** the necessary information for processing contexts.
It has

1. InputDictionary
2. ContextDatabase
3. FilteredContextDatabase
4. OutputDictionary
5. ContextHistory

Refrence
--------
`Context Aggregation <http://wiki.rubichev/contextAggregation/design/>`_
"""

import copy
from utils import *
from input import Input
from context_database import ContextDatabase
from filtered_context_database import FilteredContextDatabase
from output import Output
from context_history import ContextHistory

from disaggregator import Disaggregator
from maxcover import MaxCover

import gc

class ContextProcessor(object):
    """database class"""

    def __init__(self, contexts = None):
        self.input = Input()
        self.context_database = ContextDatabase()
        self.filtered_context_database = FilteredContextDatabase()
        self.output = Output()
        self.context_history = ContextHistory()

    def __reset(self):
        self.input.reset()
        self.context_database.reset()
        self.filtered_context_database.reset()
        self.output.reset()
        self.context_history.reset()

    def reset(self):
        """
        """
        self.__reset()
        gc.collect()

if __name__ == "__main__":
    import doctest
    doctest.testmod()


