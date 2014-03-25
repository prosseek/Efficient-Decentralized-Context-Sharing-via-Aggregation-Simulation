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
They are time independent, as they can be recovered anytime from the timestamp dependent data structure.

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
from utils_same import *

from context.context import Context

from input import Input
from output import Output
from context_database import ContextDatabase
from assorted_context_database import AssortedContextDatabase
from context_history import ContextHistory
from copy import copy

from disaggregator import Disaggregator
from maxcover import MaxCover
from output_selector import OutputSelector
from utils_configuration import  process_default_values

import gc

class ContextAggregator(object):
    """database class"""
    AGGREGATION_MODE = 0
    SINGLE_ONLY_MODE = 1

    MAX_TAU = "max_tau"
    PM = "propagation_mode"
    defaults = {MAX_TAU:0, PM:AGGREGATION_MODE}

    def is_single_only_mode(self):
        return self.configuration(ContextAggregator.PM) == ContextAggregator.SINGLE_ONLY_MODE

    def is_aggregation_mode(self):
        return self.configuration(ContextAggregator.PM) == ContextAggregator.AGGREGATION_MODE
    #
    # Initialization and Reset
    #

    def __init__(self, id = -1, config = None):
        self.id = id
        self.set_config(config)

        # inner data structure
        self.input = Input()
        self.context_database = ContextDatabase()
        self.assorted_context_database = AssortedContextDatabase()
        self.output = Output()
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

    #
    # Sample
    #
    def get_sample(self):
        return self.configuration("sample")

    def get_sample_data(self):
        sample = self.get_sample()
        if sample is None:
            return None # sampled_value = -2 # default value is -1
        return sample[self.id]

    #
    # Input
    #
    def get_input_dictionary(self):
        return self.input.dictionary

    def initalize_before_iteration(self):
        """initialization is needed for starting execution of dataflow
        """
        self.input.reset()

    #
    # Configuration methods
    #

    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = process_default_values(config, ContextAggregator.defaults)
        return self.config

    def get_current_sample(self):
        return self.current_sample

    def configuration(self, key):
        if key in self.config:
            return self.config[key]
        else:
            return None

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
        return self.context_database.get_singles(timestamp)
        #return self.assorted_context_database.get_singles(timestamp)

    def get_aggregates(self, timestamp=0):
        return self.context_database.get_aggregates(timestamp)

    def get_primes(self, timestamp=0):
        return self.assorted_context_database.get_primes(timestamp)

    def get_non_primes(self, timestamp=0):
        return self.assorted_context_database.get_non_primes(timestamp)

    def get_selected_non_primes(self, timestamp=0):
        return self.assorted_context_database.get_selected_non_primes(timestamp)

    def get_new_aggregate(self):
        return self.new_aggregate

    def get_filtered_singles(self):
        return self.filtered_singles

    def create_new_aggregate(self, contexts, timestamp=0):
        """Given contexts (a list of a set of contexts, create a context that collects all
        the information in them)

        Things to consider: we pack the single context with Context.SPECIAL_CONTEXT (let's say it as x), because
        1. We can recover the aggregate without the x, whenever x is available.
        2. We can cover larger aggregate even when x is lost (or unavailable with any reason).

        >>> d = ContextAggregator()
        >>> s1 = set([Context(value=1.0, cohorts=[0])])
        >>> c1 = set([Context(value=1.0, cohorts=[1,2])])
        >>> c = d.create_new_aggregate([c1,s1])
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

    #
    # Filter
    #
    def filter_singles(self, singles):
        """Out of many input/stored singles, filter out the singles to send
        based on configuration.

        """
        results = set()

        if self.is_aggregation_mode():
            for s in singles:
                if s.hopcount == Context.SPECIAL_CONTEXT or 0 <= s.hopcount <= self.configuration(ContextAggregator.MAX_TAU):
                    results.add(s)
                if self.configuration("propagate_recovered_singles"):
                    if s.hopcount == Context.RECOVERED_CONTEXT:
                        context = copy(s)
                        context.hopcount = 0
                        results.add(context)
        elif self.is_single_only_mode():
            for s in singles:
                results.add(s)

        return results

    def run_dataflow(self, neighbors=None, timestamp=0):
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

        Return value: dictionary that stores the standard form

        * For 1: [0][1][9] and [1..9] is sent. [2] is not propagated

        >>> d = ContextAggregator(config={ContextAggregator.PM: ContextAggregator.AGGREGATION_MODE, ContextAggregator.MAX_TAU: 1})
        >>> # Emulating receive data from neighbors
        >>> d.receive(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        >>> d.receive(2, set([Context(value=2.0, cohorts=[0])]))
        >>> d.receive(3, set([Context(value=3.0, cohorts=[1])]))
        >>> d.receive(4, set([Context(value=7.0, cohorts=[9], hopcount=Context.SPECIAL_CONTEXT)]))
        >>> # Emulating accumulated contexts
        >>> context_db = set([Context(value=1.0, cohorts=[2,4,5,3]),Context(value=1.0, cohorts=[5,6]),Context(value=7.0, cohorts=[7,8])])
        >>> d.set_database(singles=set([]), aggregates=context_db, timestamp=10)
        >>> d.context_history.set(dictionary={}, timestamp=10)
        >>> r = d.run_dataflow(timestamp=10)
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
        """

        # 1. DISAGGREGATES
        input_contexts = self.get_received_data()

        db_singles = self.get_database_singles(timestamp)
        union_contexts = input_contexts.union(db_singles)

        if self.is_aggregation_mode(): # self.configuration(ContextAggregator.PM) == ContextAggregator.AGGREGATION_MODE:
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
        if self.is_aggregation_mode(): # if self.configuration(ContextAggregator.PM) == ContextAggregator.AGGREGATION_MODE:
            if combined_aggregates:
                primes, non_primes = get_prime(combined_aggregates)
                if non_primes:
                    m = MaxCover()
                    selected_non_primes = m.run(non_primes)
            self.new_aggregate = self.create_new_aggregate(contexts=[combined_singles, primes, selected_non_primes], timestamp=timestamp)
            aggregates = contexts_to_standard({self.new_aggregate})
        else:
            aggregates = [[],[]]
        self.assorted_context_database.set(combined_singles, primes, non_primes, selected_non_primes, timestamp)

        # Only filtered singles are the candidates
        self.filtered_singles = self.filter_singles(combined_singles)

        # OutputSelector requires all the data format as standard
        singles = contexts_to_standard(self.filtered_singles)
        new_info = add_standards(singles, aggregates)
        inputs_in_standard_form = {}
        for key, value in self.input.get_dictionary().items():
            inputs_in_standard_form[key] = contexts_to_standard(value)
        history = self.context_history.get(timestamp)

        # TODO:
        # For the convention, None is returned when nothing is found in Container, and this
        # causes an error condition.
        # However, for testing code, this value can be None, so make this code for by passing the error
        if history is None: history = {}
        selector = OutputSelector(inputs=inputs_in_standard_form, context_history=history, new_info=new_info, neighbors=neighbors)
        result = selector.run()

        # result is a {} in standard form
        return result

    def is_this_new_timestamp(self, timestamp=0):
        """Checks if this is the start of timestamp

        >>> c = ContextAggregator()
        >>> c.is_this_new_timestamp()
        True
        """

        if timestamp not in self.context_database.timestamp: return True
        else:
            return self.context_database.timestamp[timestamp] == {}

    def sample(self, timestamp=0):
        """Sampling means read (acuquire) data at timestamp, and create a single context out of the data
        """
        samples = self.get_sample_data()

        if samples is None:
            return -1
        else:
            #samples = self.config["sample"][self.id]
            length = len(samples)
            if length > timestamp:
                sampled_value = samples[timestamp]
            else:
                sampled_value = -1

        self.current_sample = sampled_value
        return sampled_value

    def get_received_data(self, from_node = None):
        """Returns the received data from node_index

        >>> d = ContextAggregator()
        >>> d.receive(1, {Context(value=1.0, cohorts=[0,1,2]), Context(value=4.0, cohorts=[3], hopcount = 1)})
        >>> d.receive(2, {Context(value=2.0, cohorts=[0], hopcount=1), Context(value=4.0, cohorts=[4], hopcount = 10)})
        >>> r = d.get_received_data()
        >>> r = contexts_to_standard(r)
        >>> same(r, [[0,3,4], [0,1,2]])
        True
        """
        if from_node is not None:
            return self.input[from_node]

        result = set()
        for i in self.input.get_senders():
            result |= self.input[i]

        return result

    #######################################################
    # API
    #######################################################

    def is_nothing_to_send(self):
        output_dictionary = self.output.dictionary
        for o, v in output_dictionary.items():
            if v != [[],[]]: return False
        return True

    def send(self, neighbor = None, timestamp=0):
        """

        1. update the history
        2. returns contexts in Context object

        >>> c0 = ContextAggregator(0)
        >>> r = c0.process_to_set_output(neighbors=[1], timestamp = 0)
        >>> same(r, {1: [[0], []]})
        True
        >>> c1 = ContextAggregator(1)
        >>> r = c1.process_to_set_output(neighbors=[0], timestamp = 0)
        >>> same(r, {0: [[1], []]})
        True
        >>> r0 = c0.send(timestamp=0)
        >>> same(contexts_to_standard(r0[1]), [[0], []])
        True
        >>> r1 = c1.send(neighbor=0, timestamp=0)
        >>> same(contexts_to_standard(r1[0]), [[1], []])
        True
        """

        result = {}
        output_dictionary = self.output.dictionary
        if neighbor is None:
            for o in output_dictionary:
                single_contexts = self.output.generate_single_contexts(o=o, single_contexts=self.get_database_singles(timestamp))
                aggregate_context = self.output.generate_aggregate_contexts(o=o, aggregate_contexts=self.new_aggregate)
                result[o] = single_contexts | aggregate_context
                self.context_history.add_to_history(node_number=o, value=output_dictionary[o], timestamp=timestamp)
        else:
            assert type(neighbor) in [int, long]
            assert neighbor in output_dictionary
            # TODO
            # Duplication of code
            o = neighbor
            single_contexts = self.output.generate_single_contexts(o=o, single_contexts=self.get_database_singles(timestamp))
            aggregate_context = self.output.generate_aggregate_contexts(o=o, aggregate_contexts=self.new_aggregate)
            result[o] = single_contexts | aggregate_context
            self.context_history.add_to_history(node_number=o, value=output_dictionary[o], timestamp=timestamp)

        return result

    def receive(self, from_node, contexts, timestamp=0):
        """receive_data
        1. Stores the information who sent what
        2. Increase the hopcount when the context is a single context

        >>> d = ContextAggregator()
        >>> # two contexts are received
        >>> r = d.receive(1, {Context(value=1.0, cohorts=[0,1,2]), Context(value=1.0, cohorts=[0,1,3])})
        >>> same(d.get_received_data(1), [[0,1,2],[0,1,3]])
        True
        >>>
        """
        contexts = Context.increase_hop_count(contexts)
        self.input[from_node] = contexts

        received_info = contexts_to_standard(contexts)
        self.context_history.add_to_history(node_number=from_node, value=received_info, timestamp=timestamp)

    def process_to_set_output(self, neighbors=None, timestamp=0):
        """Process method is a generalized code for propagating contexts.

        Input:
            * neighbors : a dictionary that maps id -> standard contexts
            * timestamp : currrent timestamp

        Output:
            * output dictionary: a dictionary that maps id -> standard contexts

        1. When it is the first time of the propagation at timestamp, it samples the data
        2. When it is not the first, it invokes the run() method

        >>> a = ContextAggregator(1) # id == 1
        >>> same(a.process_to_set_output(neighbors=[10,20,30]), {10: [[1], []], 20: [[1], []], 30: [[1], []]})
        True
        >>> same(contexts_to_standard(a.get_database_singles()), [[1],[]])
        True
        >>> same(a.get_database_aggregates(), [])
        True
        >>> a.get_input_dictionary() == {}
        True
        """
        if self.is_this_new_timestamp(timestamp):
            sampled_data = self.sample(timestamp)
            context = Context(value=sampled_data, cohorts=[self.id], hopcount=0, timestamp=timestamp)
            self.set_database(singles=[context], aggregates=[], timestamp=timestamp)

            # store the context in the history and process
            result = {}
            for h in neighbors:
                result[h] = [[self.id],[]]
        else:
            result = self.run_dataflow(neighbors=neighbors, timestamp=timestamp)

        self.output.set_dictionary(result)

        # WARNING! Don't forget the input is cleared after the process_to_set_output() call
        self.initalize_before_iteration()
        return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()
