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

from utils import *

from context.context import Context

from input import Input
from context_database import ContextDatabase
from assorted_context_database import AssortedContextDatabase
from output import Output
from context_history import ContextHistory
from copy import copy

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
            if "max_tau" in config: self.max_tau = config["max_tau"]
            if "propagation_mode" in config: self.propagation_mode = config["propagation_mode"]

        # inner data structure
        self.input = Input()
        self.context_database = ContextDatabase()
        self.assorted_context_database = AssortedContextDatabase()
        self.output_dictionary = None
        #self.output = Output()
        self.context_history = ContextHistory()

        self.new_aggregate = None
        self.filtered_singles = None

    def __reset(self):
        self.input.reset()
        self.context_database.reset()
        self.assorted_context_database.reset()
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
        #self.output.reset()

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

    def set_database(self, singles, aggregates, timestamp = 0):
        """TODO: update information based on the time stamp
        """
        self.context_database.set(singles, aggregates)

    def get_database_singles(self, timestamp=0):
        return self.context_database.get_singles(timestamp)

    def get_database_aggregates(self, timestamp=0):
        return self.context_database.get_aggregates(timestamp)

    def get_singles(self, timestamp=0):
        return self.assorted_context_database.get_singles(timestamp)

    def get_primes(self, timestamp=0):
        return self.assorted_context_database.get_primes(timestamp)

    def get_non_primes(self, timestamp=0):
        return self.assorted_context_database.get_non_primes(timestamp)

    def get_selected_non_primes(self, timestamp=0):
        return self.assorted_context_database.get_selected_non_primes(timestamp)

    # def get_output(self):
    #     return self.output

    def get_new_aggregate(self):
        return self.new_aggregate

    def get_filtered_singles(self):
        return self.filtered_singles

    def create_current_aggregate(self, contexts, timestamp=0):
        """Given contexts (a list of a set of contexts, create a context that collects all
        the information in them)

        Things to consider: we pack the single context with Context.SPECIAL_CONTEXT (let's say it as x), because
        1. We can recover the aggregate without the x, whenever x is available.
        2. We can cover larger aggregate even when x is lost (or unavailable with any reason).

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

        c = Context(value=value, cohorts=elements, hop_count=Context.AGGREGATED_CONTEXT, timestamp=timestamp)
        return c

    def get_output(self):
        return self.output_dictionary

    #
    # Filter
    #
    def filter_singles(self, singles):
        results = set()
        for s in singles:
            if s.hop_count == Context.SPECIAL_CONTEXT or 0 <= s.hop_count <= self.max_tau:
                results.add(s)
        return results

    def run(self, timestamp=0):
        """when input data has received information, it processes the data to generate the output

        In this example, when [0,1,2][0][1] is given as a input, and [[2,3,4,5][5,6],[7,8]] is already stored as contexts
        1. [0][1] -> [2] is identified
        2. [3,4,5],[5,6],[7,8] is now a new aggregates
        3. [7,8] is a prime
        4. [3,4,5],[5,6] is non_prime
        5. [3,4,5] is selected_non_prime
        6. new aggregates has [0,1,2,3,4,5,7,8] as elements

        >>> d = DataFlow(config={"propagation_mode": DataFlow.AGGREGATION_MODE, "max_tau": 1})
        >>> d.initialize() # Always execute initialize before newly receive data
        >>> # Emulating receive data from neighbors
        >>> d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        >>> d.receive_data(2, set([Context(value=2.0, cohorts=[0])]))
        >>> d.receive_data(3, set([Context(value=3.0, cohorts=[1])]))
        >>> d.receive_data(4, set([Context(value=7.0, cohorts=[9], hop_count=Context.SPECIAL_CONTEXT)]))
        >>> # Emulating accumulated contexts
        >>> context_db = set([Context(value=1.0, cohorts=[2,4,5,3]),Context(value=1.0, cohorts=[5,6]),Context(value=7.0, cohorts=[7,8])])
        >>> d.set_database(singles=set([]), aggregates=context_db, timestamp=10)
        >>> d.run(timestamp=10)
        >>> # Emulating newly found singles and aggregates from database
        >>> compare_contexts_and_cohorts(d.get_database_singles(), [[0],[1],[2],[9]])
        True
        >>> compare_contexts_and_cohorts(d.get_database_aggregates(),[[7,8],[3,4,5],[6,5]])
        True
        >>> # Emulating the disaggregation process
        >>> compare_contexts_and_cohorts(d.get_singles(), [[0],[1],[2],[9]])
        True
        >>> compare_contexts_and_cohorts(d.get_primes(), [[7,8]])
        True
        >>> compare_contexts_and_cohorts(d.get_non_primes(), [[3,4,5], [5,6]])
        True
        >>> compare_contexts_and_cohorts(d.get_selected_non_primes(), [[3,4,5]])
        True
        >>> ### Check the new aggregate has correct elements
        >>> d.get_new_aggregate().get_cohorts_as_set() == set([0,1,2,3,4,5,7,8,9])
        True
        >>> compare_contexts_and_cohorts(d.get_filtered_singles(), [[0],[1],[9]])
        True
        >>> r = d.get_output()
        >>> compare_contexts_and_cohorts(r[1], [[0,1,2,3,4,5,7,8,9],[0],[1],[9]])
        True
        >>> compare_contexts_and_cohorts(r[2], [[0,1,2,3,4,5,7,8,9],[1],[9]])
        True
        >>> compare_contexts_and_cohorts(r[3], [[0,1,2,3,4,5,7,8,9],[0],[9]])
        True
        >>> compare_contexts_and_cohorts(r[4], [[0,1,2,3,4,5,7,8,9],[0],[1]])
        True
        """

        # 1. DISAGGREGATES
        input_contexts = self.get_received_data()

        db_singles = self.get_database_singles()
        union_contexts = input_contexts.union(db_singles)

        if self.propagation_mode == DataFlow.AGGREGATION_MODE:
            db_aggregates = self.get_database_aggregates()
            union_contexts = union_contexts.union(db_aggregates)

            d = Disaggregator(union_contexts)
            combined_singles, combined_aggregates = d.run()
        else:
            combined_singles = union_contexts
            combined_aggregates = set()

        self.set_database(combined_singles, combined_aggregates, timestamp=timestamp)

        # ASSORT
        primes = set()
        non_primes = set()
        selected_non_primes = set()
        if self.propagation_mode == DataFlow.AGGREGATION_MODE:
            if combined_aggregates:
                primes, non_primes = get_prime(combined_aggregates)
                if non_primes:
                    m = MaxCover()
                    selected_non_primes = m.run(non_primes)
                self.new_aggregate = self.create_current_aggregate([combined_singles, primes, selected_non_primes])

        self.assorted_context_database.set(combined_singles, primes, non_primes, selected_non_primes)

        # Only filtered singles are the candidates
        self.filtered_singles = self.filter_singles(combined_singles)

        # Send candidates are one of the two
        # 1. self.new_aggregate
        # 2. self.filtered_singles

        # Given input_contextsR
        # history.

        contexts = copy(self.filtered_singles)
        contexts.add(self.new_aggregate)
        input_dictionary = self.input.get_dictionary()
        self.output_dictionary = self.context_history.calculate_output(contexts, input_dictionary, timestamp=timestamp)
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()


