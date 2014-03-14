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
    AGGREGATION_MODE = 0
    SINGLE_ONLY_MODE = 1
    #
    # Initialization and Reset
    #
    def __init__(self, config = None):
        self.propagation_mode = DataFlow.AGGREGATION_MODE
        self.max_tau = 1

        if config is not None:
            if config["max_tau"]: self.max_tau = config["max_tau"]
            if config["propagation_mode"]: self.propagation_mode = config["propagation_mode"]

        # inner data structure
        self.input = Input()
        self.context_database = ContextDatabase()
        self.filtered_context_database = FilteredContextDatabase()
        self.output = Output()
        self.context_history = ContextHistory()


        self.new_aggregate = None

    def __reset(self):
        self.input.reset()
        self.context_database.reset()
        self.filtered_context_database.reset()
        self.output.reset()
        self.context_history.reset()

    def reset(self):
        """reset is for garbage collection in multiple data simulation.
        This is done for releasing memory for another simulation.
        """
        self.__reset()
        gc.collect()

    def initialize(self):
        """initialization is needed for starting execution of dataflow
        """
        self.input.reset()
        self.output.reset()

    #
    # Input
    #
    def get_received_data(self, node_index = None):
        """Returns the received data from node_index

        >>> d = DataFlow()
        >>> d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2]), Context(value=4.0, cohorts=[3], hop_count = 1)]))
        >>> d.receive_data(2, set([Context(value=2.0, cohorts=[0], hop_count=1), Context(value=4.0, cohorts=[4], hop_count = 10)]))
        >>> compare_contexts_and_cohorts(d.get_received_data(), [[0,1,2],[0],[3],[4]])
        True
        """
        if node_index is not None:
            return self.input[node_index]

        result = set()
        for i in self.input.get_senders():
            result = result.union(self.input[i])

        return result

    def receive_data(self, node_index, contexts):
        """receive_data
        1. Stores the information who sent what
        2. Increase the hop_count when the context is a single context

        >>> d = DataFlow()
        >>> # two contexts are received
        >>> r = d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2]), Context(value=1.0, cohorts=[0,1,3])]))
        >>> compare_contexts_and_cohorts(d.get_received_data(1), [[0,1,2],[0,1,3]])
        True
        >>>
        """
        contexts = Context.increase_hop_count(contexts)
        self.input[node_index] = contexts

    #
    # Database
    #

    def update_database(self, singles, aggregates, timestamp = None):
        """TODO: update information based on the time stamp
        """
        self.context_database.set(singles, aggregates)

    def get_database_singles(self):
        return self.context_database.get_singles()

    def get_database_aggregates(self):
        return self.context_database.get_aggregates()

    def get_singles(self):
        return self.filtered_context_database.get_singles()

    def get_primes(self):
        return self.filtered_context_database.get_primes()

    def get_non_primes(self):
        return self.filtered_context_database.get_non_primes()

    def get_selected_non_primes(self):
        return self.filtered_context_database.get_selected_non_primes()

    def get_output(self):
        return self.output

    def get_new_aggregate(self):
        return self.new_aggregate

    def create_current_aggregate(self, contexts):
        """Given contexts (a list of a set of contexts, create a context that collects all
        the information in them

        >>> d = DataFlow()
        >>> s1 = set([Context(value=1.0, cohorts=[0])])
        >>> c1 = set([Context(value=1.0, cohorts=[1,2])])
        >>> c = d.create_current_aggregate([c1,s1])
        >>> c.value
        1.0
        >>> c.get_cohorts_as_set() == set([0,1,2])
        True
        """
        sum = 0.0
        elements = set()
        for context_set in contexts:
            for c in context_set:
                sum += c.value * len(c)
                elements = elements.union(c.get_cohorts_as_set())
        value = sum / len(elements)
        #TODO: Timestamp should be adjusted
        c = Context(value=value, cohorts=elements, hop_count=Context.AGGREGATED_CONTEXT, time_stamp = None)
        return c

    def run(self):
        """when input data has received information, it processes the data to generate the output

        In this example, when [0,1,2][0][1] is given as a input, and [[2,3,4,5][5,6],[7,8]] is already stored as contexts
        1. [0][1] -> [2] is identified
        2. [3,4,5],[5,6],[7,8] is now a new aggregates
        3. [7,8] is a prime
        4. [3,4,5],[5,6] is non_prime
        5. [3,4,5] is selected_non_prime
        6. new aggregates has [0,1,2,3,4,5,7,8] as elements

        >>> d = DataFlow()
        >>> d.initialize() # Always execute initialize before newly receive data
        >>> # Emulating receive data from neighbors
        >>> d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        >>> d.receive_data(2, set([Context(value=2.0, cohorts=[0])]))
        >>> d.receive_data(3, set([Context(value=3.0, cohorts=[1])]))
        >>> # Emulating accumulated contexts
        >>> d.update_database(set([]), set([Context(value=1.0, cohorts=[2,4,5,3]),Context(value=1.0, cohorts=[5,6]),Context(value=7.0, cohorts=[7,8])]))
        >>> d.run()
        >>> # Emulating newly found singles and aggregates from database
        >>> compare_contexts_and_cohorts(d.get_database_singles(), [[0],[1],[2]])
        True
        >>> compare_contexts_and_cohorts(d.get_database_aggregates(),[[7,8],[3,4,5],[6,5]])
        True
        >>> # Emulating the disaggregation process
        >>> compare_contexts_and_cohorts(d.get_singles(), [[0],[1],[2]])
        True
        >>> compare_contexts_and_cohorts(d.get_primes(), [[7,8]])
        True
        >>> compare_contexts_and_cohorts(d.get_non_primes(), [[3,4,5], [5,6]])
        True
        >>> compare_contexts_and_cohorts(d.get_selected_non_primes(), [[3,4,5]])
        True
        >>> ### Check the new aggregate has correct elements
        >>> d.get_new_aggregate().get_cohorts_as_set() == set([0,1,2,3,4,5,7,8])
        True
        >>> # All the out has the same context

        True
        """
        # >>> r = d.get_output()
        # >>> compare_contexts_and_cohorts(r[1], [[0,1,2,3,4,5,7,8]])
        # True
        # >>> compare_contexts_and_cohorts(r[2], [[0,1,2,3,4,5,7,8]])
        # True
        # >>> compare_contexts_and_cohorts(r[3], [[0,1,2,3,4,5,7,8]])

        # 1. collect all the data received from other hosts
        input_contexts = self.get_received_data()
        db_aggregates = self.get_database_aggregates()
        db_singles = self.get_database_singles()

        input_contexts = input_contexts.union(db_aggregates)
        input_contexts = input_contexts.union(db_singles)

        d = Disaggregator(input_contexts)
        result_singles, result_aggregates = d.run()
        self.update_database(result_singles, result_aggregates)

        primes = set()
        non_primes = set()
        selected_non_primes = set()
        if result_aggregates:
            # get primes
            primes, non_primes = get_prime(result_aggregates)
            # get maximum

            if non_primes:
                m = MaxCover()
                #maxcover_dictionary = get_maxcover_dictionary(non_primes)
                selected_non_primes = m.run(non_primes)

        self.filtered_context_database.update(result_singles, primes, non_primes, selected_non_primes)
        self.new_aggregate = self.create_current_aggregate([result_singles, primes, selected_non_primes])

        if self.context_history.is_new_info_and_set(self.new_aggregate):
            # ask context history what to send to each neighbor node
            self.output = self.context_history.calculate_output(self.new_aggregate, self.get_received_data())


if __name__ == "__main__":
    import doctest
    doctest.testmod()


