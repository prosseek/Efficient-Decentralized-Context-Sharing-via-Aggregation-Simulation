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

from context.context import Context

from input import Input
from context_database import ContextDatabase
from filtered_context_database import FilteredContextDatabase
from output import Output
from context_history import ContextHistory

from disaggregator import Disaggregator
from maxcover import MaxCover

import gc

class DataFlow(object):
    """database class"""

    #
    # Initialization and Reset
    #
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

    #
    # Input
    #
    def get_received_data(self, node_index = None):
        """Returns the received data from node_index

        >>> d = DataFlow()
        >>> d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        >>> d.receive_data(2, set([Context(value=2.0, cohorts=[0])]))
        >>> compare_contexts_and_cohorts(d.get_received_data(), [[0,1,2],[0]])
        True
        """
        if node_index is not None:
            return self.input[node_index]

        result = set()
        for i in self.input.get_senders():
            result |= self.input[i]

        return result

    def receive_data(self, node_index, contexts):
        """
        >>> d = DataFlow()
        >>> # two contexts are received
        >>> r = d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2]), Context(value=1.0, cohorts=[0,1,3])]))
        >>> compare_contexts_and_cohorts(d.get_received_data(1), [[0,1,2],[0,1,3]])
        True
        """
        self.input[node_index] = contexts

    def run(self):
        """when input data has received information, it processes the data to generate the output

        >>> d = DataFlow()
        >>> d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        >>> d.receive_data(2, set([Context(value=2.0, cohorts=[0])]))
        >>> d.run()
        """

        # 1. collect all the data received from other hosts
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()


