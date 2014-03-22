"""context database

Context database stores **all** the necessary information for processing contexts.
It has the following objects

1. Input
2. ContextDatabase
3. AssortedContextDatabase
4. ContextHistory
5. OutputDictionary

For each object dataflow.py exports the API.
We have 14 APIs as of [2014/03/17]

1. initialize()
    Empty the Input, should be executed whenever new propagation is started.
2. receive_data(index, a set of contexts)
    Receive and store the data into Input from host index
3. run(timestamp)
    Executes the disaggregation and aggregation until all the data structures for timestamp is calculated and stored

After the run() is executed, we can get the results that is timestamp dependent with the API.

1. get_database_singles(timestamp)
    Returns a set of contexts recovered/received
2. get_database_aggregates(timestamp)
3. get_singles(timestamp)
    Returns the recovered and received singles so far
4. get_primes(timestamp)
    Returns the prime aggregates so far
5. get_non_primes(timestamp)
6. get_selected_non_primes(timestamp)
    Returns the non-prime and selected-non-primes

After the run() is executed, we get the temporary (timestamp independent) with the API.
They are time indepdent, as they can be recovered anytime from the timestamp depdendent data structure.

1. get_filtered_singles()
    Returns a set of filtered single contexts based on configurations
2. get_new_aggregate()
    Returns a context of newly generated aggregate.
3. get_output()
    Returns a dictionary that is going to be sent to each host

The API for other kinds of information.

1. get_configuration()
    Returns current configuration
2. reset()
    Deletes all the data structure created in the dataflow, and start garbage collection

Refrence
--------
`Context Aggregation <http://wiki.rubichev/contextAggregation/design/>`_
"""

from utils import *

from context.context import Context

from input import Input
from context_database import ContextDatabase
from assorted_context_database import AssortedContextDatabase
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
        self.propagate_recovered_single = False

        if config is not None:
            if "max_tau" in config: self.max_tau = config["max_tau"]
            if "propagation_mode" in config: self.propagation_mode = config["propagation_mode"]
            if "propagate_recovered_singles" in config: self.propagate_recovered_single = config["propagate_recovered_singles"]

        # inner data structure
        self.input = Input()
        self.context_database = ContextDatabase()
        self.assorted_context_database = AssortedContextDatabase()
        self.output_dictionary = None
        #self.output = Output()
        self.context_history = ContextHistory()

        self.new_aggregate = None
        self.filtered_singles = None

    def get_configuration(self):
        return {"max_tau": self.max_tau,
                "propagation_mode": self.propagation_mode,
                "propagate_recovered_singles": self.propagate_recovered_singles}

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
        >>> d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2]), Context(value=4.0, cohorts=[3], hopcount = 1)]))
        >>> d.receive_data(2, set([Context(value=2.0, cohorts=[0], hopcount=1), Context(value=4.0, cohorts=[4], hopcount = 10)]))
        >>> same(d.get_received_data(), [[0,3,4], [0,1,2]])
        True
        """
        if node_index is not None:
            return self.input[node_index]

        result = set()
        for i in self.input.get_senders():
            result |= self.input[i]

        return result

    def receive_data(self, node_index, contexts):
        """receive_data
        1. Stores the information who sent what
        2. Increase the hopcount when the context is a single context

        >>> d = DataFlow()
        >>> # two contexts are received
        >>> r = d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2]), Context(value=1.0, cohorts=[0,1,3])]))
        >>> same(d.get_received_data(1), [[0,1,2],[0,1,3]])
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
        self.context_database.set(singles, aggregates, timestamp)

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

        c = Context(value=value, cohorts=elements, hopcount=Context.AGGREGATED_CONTEXT, timestamp=timestamp)
        return c

    def get_output(self):
        return self.output_dictionary

    #
    # Filter
    #
    def filter_singles(self, singles):
        results = set()
        for s in singles:
            if s.hopcount == Context.SPECIAL_CONTEXT or 0 <= s.hopcount <= self.max_tau:
                results.add(s)
            if self.propagate_recovered_single:
                if s.hopcount == Context.RECOVERED_CONTEXT:
                    context = copy(s)
                    context.hopcount = 0
                    results.add(context)
        return results

    def run(self, timestamp=0):
        """when input data has received information, it processes the data to generate the output

        In this example with max_tau=1, when 1:[0,1,2], 2:[0], 3:[1] 4:[9]'(special context)
        is given as a input, and [[2,3,4,5][5,6],[7,8]] is already stored as contexts

        1. [0][1][9]' -> [2] is identified
        2. [3,4,5],[5,6],[7,8] is now a new aggregates
        3. [7,8] is a prime
        4. [3,4,5],[5,6] is non_prime
        5. [3,4,5] is selected_non_prime
        6. new aggregates has [0,1,2,3,4,5,7,8,9] as elements
        7. From filtering, [0][1][2][9]' will be propagated with [0,1,2,3,4,5,7,8,9] as an aggregate

        For output

        * For 1: [0][1][9] and [1..9] is sent. [2] is not propagated

        >>> d = DataFlow(config={"propagation_mode": DataFlow.AGGREGATION_MODE, "max_tau": 1})
        >>> d.initialize() # Always execute initialize before newly receive data
        >>> # Emulating receive data from neighbors
        >>> d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        >>> d.receive_data(2, set([Context(value=2.0, cohorts=[0])]))
        >>> d.receive_data(3, set([Context(value=3.0, cohorts=[1])]))
        >>> d.receive_data(4, set([Context(value=7.0, cohorts=[9], hopcount=Context.SPECIAL_CONTEXT)]))
        >>> # Emulating accumulated contexts
        >>> context_db = set([Context(value=1.0, cohorts=[2,4,5,3]),Context(value=1.0, cohorts=[5,6]),Context(value=7.0, cohorts=[7,8])])
        >>> d.set_database(singles=set([]), aggregates=context_db, timestamp=10)
        >>> d.run(timestamp=10)
        >>> # Emulating newly found singles and aggregates from database
        >>> same(d.get_database_singles(timestamp=10), [[0,1,2,9],[]])
        True
        >>> same(d.get_database_aggregates(timestamp=10),[[7,8],[3,4,5],[6,5]])
        True
        >>> # Emulating the disaggregation process
        >>> same(d.get_singles(timestamp=10), [[0,1,2,9],[]])
        True
        >>> same(d.get_primes(timestamp=10), [[],[7,8]])
        True
        >>> same(d.get_non_primes(timestamp=10), [[3,4,5], [5,6]])
        True
        >>> same(d.get_selected_non_primes(timestamp=10), [[],[3,4,5]])
        True
        >>> ### Check the new aggregate has correct elements
        >>> d.get_new_aggregate().get_cohorts_as_set() == set([0,1,2,3,4,5,7,8,9])
        True
        >>> same(d.get_filtered_singles(), [[0,1,9],[]])
        True
        >>> r = d.get_output()
        >>> same(r[1], [[0,1,9],[0,1,2,3,4,5,7,8,9]])
        True
        >>> same(r[2], [[1,9],[0,1,2,3,4,5,7,8,9]])
        True
        >>> same(r[3], [[0,9],[0,1,2,3,4,5,7,8,9]])
        True
        >>> same(r[4], [[0,1],[0,1,2,3,4,5,7,8,9]])
        True
        """

        # 1. DISAGGREGATES
        input_contexts = self.get_received_data()

        db_singles = self.get_database_singles(timestamp)
        union_contexts = input_contexts.union(db_singles)

        if self.propagation_mode == DataFlow.AGGREGATION_MODE:
            db_aggregates = self.get_database_aggregates(timestamp)
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

        self.assorted_context_database.set(combined_singles, primes, non_primes, selected_non_primes, timestamp)

        # Only filtered singles are the candidates
        self.filtered_singles = self.filter_singles(combined_singles)

        contexts = copy(self.filtered_singles)
        contexts.add(self.new_aggregate)
        input_dictionary = self.input.get_dictionary()
        self.output_dictionary = self.context_history.calculate_output(contexts, input_dictionary, timestamp=timestamp)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
