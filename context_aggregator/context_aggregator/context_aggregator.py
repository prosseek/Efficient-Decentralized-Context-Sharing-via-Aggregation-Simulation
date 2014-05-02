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
import sys
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
from greedy_maxcover import GreedyMaxCover
#from brutal_force_maxcover import MaxCover
from output_selector import OutputSelector
from utils_configuration import  process_default_values

import gc

#DEBUG = False

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

        # instance variables for debugging purposes
        self.new_aggregate = None
        self.filtered_singles = None
        self.data = None
        self.average = None

    def get_data(self):
        return self.data

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
        # [] works as an API
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

    ###################################
    # STATIC METHODS
    ###################################

    @staticmethod
    def create_new_aggregate(contexts, timestamp=0):
        """Given contexts (a list of a set of contexts, create a context that collects all
        the information in them)

        Things to consider: we pack the single context with Context.SPECIAL_CONTEXT (let's say it as x), because
        1. We can recover the aggregate without the x, whenever x is available.
        2. We can cover larger aggregate even when x is lost (or unavailable with any reason).

        >>> s1 = set([Context(value=1.0, cohorts=[0])])
        >>> c1 = set([Context(value=1.0, cohorts=[1,2])])
        >>> c = ContextAggregator.create_new_aggregate([c1,s1])
        >>> c.value
        1.0
        >>> c.get_cohorts_as_set() == set([0,1,2])
        True
        >>> c = ContextAggregator.create_new_aggregate([s1, c1, set(), set()])
        >>> c.value
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

    @staticmethod
    def remove_same_id_singles(singles):
        """

        >>> singles = {Context(value=1.0, cohorts={1}, hopcount=1), Context(value=1.0, cohorts={1}, hopcount=2), Context(value=1.0, cohorts={1}, hopcount=3)}
        >>> c = ContextAggregator.remove_same_id_singles(singles)
        >>> len(c)
        1
        >>> s = list(c)[0]
        >>> s.hopcount == 1
        True
        """
        # It can happen that the same context with a change in hopcount can exist
        singles_dictionary = {}
        for s in singles:
            key = s.get_id()
            if key not in singles_dictionary:
                singles_dictionary[key] = []
            singles_dictionary[key].append(s)

        result = set()
        for key, values in singles_dictionary.items():
            if len(values) == 1:
                result.add(values[0])
            else:
                result.add(sorted(values, key=lambda m: m.hopcount)[0])
        return result

    @staticmethod
    def remove_same_id_aggregates(aggregates):
        """

        >>> aggregates = {Context(value=1.0, cohorts={1,2,3}, hopcount=1), Context(value=1.0, cohorts={1,2,3}, hopcount=2), Context(value=1.0, cohorts={1,2,3}, hopcount=3)}
        >>> c = ContextAggregator.remove_same_id_aggregates(aggregates)
        >>> len(c)
        1
        >>> print list(c)[0]
        v(1.00):c([1,2,3]):h(1):t(0)
        """
        # It can happen that the same context with a change in hopcount can exist
        aggr_dictionary = {}
        for s in aggregates:
            key = frozenset(s.get_cohorts_as_set())
            if key in aggr_dictionary:
                hopcount = aggr_dictionary[key].hopcount
                # only the newest (smallest number) wins
                if s.hopcount < hopcount:
                    aggr_dictionary[key] = s
            else:
                aggr_dictionary[key] = s

        result = set(aggr_dictionary.values())
        return result

    @staticmethod
    def filter_singles_by_hopcount(singles, configuration):
        """Out of many input/stored singles, filter out the singles to send
        based on configuration.

        """
        max_tau = configuration(ContextAggregator.MAX_TAU)
        results = set()
        for s in singles:
            if s.hopcount == Context.SPECIAL_CONTEXT or 0 <= s.hopcount <= max_tau:
                results.add(s)
            if configuration("propagate_recovered_singles"):
                if s.hopcount == Context.RECOVERED_CONTEXT:
                    context = copy(s)
                    context.hopcount = 0
                    results.add(context)
        return results

    @staticmethod
    def sample(samples=None, timestamp=0):
        """Sampling means read (acuquire) data at timestamp, and create a single context out of the data
        """
        #samples = self.get_sample_data()

        if samples is None:
            return -1, False
        else:
            #samples = self.config["sample"][self.id]
            if type(samples) is tuple:
                # the order is important as samples are modified into a tuple to a list
                special_flags = samples[1]
                samples = samples[0] # now it's list
            else:
                special_flags = [False] * len(samples)

            length = len(samples)
            if length > timestamp:
                sampled_value = samples[timestamp]
                special_flag = special_flags[timestamp]
            else:
                special_flag = False

        #self.current_sample = sampled_value
        return sampled_value, special_flag


    @staticmethod
    def get_score(cohorts, sent_history_as_set):
        """Returns the number of elements cohorts - sent_history_as_set

        >>> a = {1,2,3,4}
        >>> b = {4,5,6,7}
        >>> ContextAggregator.get_score(a, b)
        3
        """
        return len(cohorts - sent_history_as_set)

    @staticmethod
    def get_output_from_nps(aggregates, history, neighbors):
        """Find the aggregate that has the largest set of contexts that are not sent to neighbors

        >>> a = {Context(value=1.0, cohorts=[1,2,3]), Context(value=1.0, cohorts=[1,2,3,4]), Context(value=1.0, cohorts=[1,2,3,4,5])}
        >>> h = {1:[[],[1,3]], 2:[[],[1,3]]}
        >>> neighbors = [1,2]
        >>> r = ContextAggregator.get_output_from_nps(a, h, neighbors)
        >>> same(r[1], [[],[1,2,3,4,5]])
        True
        """
        if len(aggregates) == 0: return {}
        if len(neighbors) == 0: return {}

        result = {}
        for n in neighbors:
            # get the aggregation
            sent_history_as_set = set(history[n][1])
            scores = {}
            for a in aggregates:
                cohorts = a.get_cohorts_as_set()
                key = str(list(cohorts))
                scores[key] = ContextAggregator.get_score(cohorts, sent_history_as_set)

            keys = sorted(scores, key=lambda e: -scores[e])

            # when sending only one context
            if scores[keys[0]] > 0:
                winner = eval(keys[0])
                result[n] = [[],winner]
            else:
                result[n] = [[],[]]

        return result
        #self.context_database.aggregates, self.context_history.get(timestamp), neighbors)

    ###################################
    # DATA FLOW
    ###################################

    def application_disseminate_when_above_average(self, new_aggregate, filtered_singles, timestamp, iteration):
        """Application

        Given average, compare the average with the sensor data to create and replace the single context

        Side effect: filtered_singles are modified when necessary
        """
        average = new_aggregate.value
        variation = self.get_data() - average
        percentage_variation = abs(variation)/average*100.0
        if "threshold" not in self.config:
            threshold = sys.maxint
        else:
            threshold = self.config["threshold"]

        if percentage_variation > threshold: # Threshold is 50 as now
            context = Context(value=self.get_data(), cohorts=[self.id], hopcount=Context.SPECIAL_CONTEXT, timestamp=timestamp)
            print "Weird, diesseminate myself %d %d" % (self.id, iteration)
            # it just compares the id and hopcount is ignored in comparison
            remove_if_in(context, filtered_singles)
            #
            # WARINING! Side effect here!
            #
            filtered_singles.add(context)
            # the single context in the db should be updated
            self.context_database.update_context_hopcount(self.id, Context.SPECIAL_CONTEXT)
        return filtered_singles

    def get_new_info(self, singles, filtered_singles, primes, selected_non_primes, timestamp, iteration):
        """Given singles/primes/non_primes return new_info in standard form, and newly created new_aggregates

        * singles are needed to make maximal aggregates
        * filtered_singles are needed to identify what singles are to sent

        new_aggregate is None when there is no new aggregates created
        """
        if len(singles) == 1 and primes == set() and selected_non_primes == set(): # there is only one single context
            singles = contexts_to_standard(singles)
            new_info = add_standards(singles, [[],[]]) # standard operation
            new_aggregate = None
        else:
            # from singles/primes/non_primes get new aggregated contexts
            new_aggregate = ContextAggregator.create_new_aggregate(contexts=[singles, primes, selected_non_primes], timestamp=timestamp)
            filtered_singles = self.application_disseminate_when_above_average(new_aggregate, filtered_singles, timestamp, iteration)
            # we need to generate the new_info in the form of standard
            a = contexts_to_standard({new_aggregate})
            s = contexts_to_standard(filtered_singles)
            new_info = add_standards(a, s)

        return new_info, new_aggregate

    def set_database_and_return(self, result, new_aggregates, singles, aggregates, primes, non_primes, selected_non_primes, timestamp):
        self.new_aggregate = new_aggregates
        self.set_database(singles, aggregates, timestamp=timestamp)
        self.assorted_context_database.set(singles, primes, non_primes, selected_non_primes, timestamp)
        return result, singles, aggregates, new_aggregates

    def dataflow_aggregations_mode(self, neighbors, timestamp, iteration):
        """
        """
        # 1. collect all the contexts
        input_contexts = self.get_received_data()
        db_singles = self.get_database_singles(timestamp)
        db_aggregates = self.get_database_aggregates(timestamp)
        input_singles, input_aggregates = separate_single_and_group_contexts(input_contexts)
        history = self.context_history.get(timestamp)
        inputs_in_standard_form = self.input.get_in_standard_from()

        unique_singles = ContextAggregator.remove_same_id_singles(input_singles.union(db_singles))
        unique_aggregates = ContextAggregator.remove_same_id_aggregates(input_aggregates.union(db_aggregates))

        union_contexts = unique_aggregates | unique_singles
        disaggregator = Disaggregator(union_contexts)

        # 3. Run disaggregator
        try_count = 0
        disaggregated_aggregates_set = set()

        # It tries 10 times with different disaggregation setup, and give up
        # giving up means that it does not find the output
        while True:
            try_count += 1
            if try_count > 5:
                #print "Did my best node(%d) - %d" % (self.id, try_count)
                break
            else:
                pass
                #if try_count > 1:
                #    print "(host %d) try count %d" % (self.id, try_count)

            # It's in the while loop, and it means that it tries to find different aggregation.
            # It again tries to find 10 times to find a new set of aggregation data

            attempt_count = 10
            found_new = False
            for i in range(attempt_count):

                disaggregated_singles, disaggregated_aggregates = disaggregator.run()
                if not disaggregated_aggregates:
                    found_new = True # Not technically correct, but it will not cause an error due to just breaking out
                    break
                aggregates_token = str(aggregated_contexts_to_list_of_standard(disaggregated_aggregates))
                if aggregates_token not in disaggregated_aggregates_set:
                    found_new = True
                    #if i > 0:
                    #    print "Host (%d): trying %d(th) with token %s" % (self.id, i, aggregates_token, )
                    disaggregated_aggregates_set.add(aggregates_token)
                    break

            if not found_new:
                #print "Host (%d): Not found the new aggregates history (%d)" % (self.id, len(disaggregated_aggregates_set))
                break

            # remove generated redundancies
            disaggregated_singles = ContextAggregator.remove_same_id_singles(disaggregated_singles)
            disaggregated_aggregates = ContextAggregator.remove_same_id_aggregates(disaggregated_aggregates)

            filtered_singles = ContextAggregator.filter_singles_by_hopcount(disaggregated_singles, self.configuration)

            if not disaggregated_aggregates: # no aggregates and treat the same as singles only case
                # 3. The code is the same as singles except the singles are filtered out
                primes = set()
                non_primes = set()
                selected_non_primes = set()
                param = {
                    "singles":disaggregated_singles,
                    "filtered_singles":filtered_singles,
                    "primes":primes,
                    "selected_non_primes":selected_non_primes,
                    "timestamp":timestamp,
                    "iteration":iteration
                }
                new_info, new_aggregates = self.get_new_info(**param)
                selector_result = OutputSelector(inputs=inputs_in_standard_form, context_history=history, new_info=new_info, neighbors=neighbors).run()
                return self.set_database_and_return(selector_result, new_aggregates, disaggregated_singles, disaggregated_aggregates, primes, non_primes, selected_non_primes, timestamp)

            primes, non_primes = get_prime(disaggregated_aggregates)

            if not non_primes: # only primes
                assert primes is not None, "No primes and non-primes, it's an error condition"

                non_primes = set()
                selected_non_primes = set()
                param = {
                    "singles":disaggregated_singles,
                    "filtered_singles":filtered_singles,
                    "primes":primes,
                    "selected_non_primes":selected_non_primes,
                    "timestamp":timestamp,
                    "iteration":iteration
                }
                new_info, new_aggregates = self.get_new_info(**param)
                selector_result = OutputSelector(inputs=inputs_in_standard_form, context_history=history, new_info=new_info, neighbors=neighbors).run()
                res_val = self.set_database_and_return(selector_result, new_aggregates, disaggregated_singles, disaggregated_aggregates, primes, non_primes, selected_non_primes, timestamp)
                if not is_empty_dictionary(selector_result):
                    return res_val
                # try again if there is no output
                continue

            # for non-prime cases
            previous_selection = self.assorted_context_database.get_selected_non_primes(timestamp)
            selected_non_primes_list = GreedyMaxCover().run(non_primes, previous_selection)

            # the greedy max cover can return multiple candidates for the case when
            # there is nothing to send to the neighboring nodes
            for i, selected_non_primes in enumerate(selected_non_primes_list):
                param = {
                    "singles":disaggregated_singles,
                    "filtered_singles":filtered_singles,
                    "primes":primes,
                    "selected_non_primes":selected_non_primes,
                    "timestamp":timestamp,
                    "iteration":iteration
                }
                if not selected_non_primes:
                    #print "SHOOT %s" % aggregated_contexts_to_list_of_standard(selected_non_primes)
                    break

                if i > 0:
                    print "(host %d) %d try with %s" % (self.id, i, aggregated_contexts_to_list_of_standard(selected_non_primes))

                new_info, new_aggregates = self.get_new_info(**param)
                selector_result = OutputSelector(inputs=inputs_in_standard_form, context_history=history, new_info=new_info, neighbors=neighbors).run()
                res_val = self.set_database_and_return(selector_result, new_aggregates, disaggregated_singles, disaggregated_aggregates, primes, non_primes, selected_non_primes, timestamp)

                if not is_empty_dictionary(selector_result):
                    return res_val

            # try to send the NP that has the largest unsent data
            result = ContextAggregator.get_output_from_nps(self.context_database.get_aggregates(timestamp), self.context_history.get(timestamp), neighbors)
            if result:
                return result, disaggregated_singles, disaggregated_aggregates, new_aggregates

        # with all my efforts, no output found just return none
        return self.set_database_and_return(dict(), new_aggregates, disaggregated_singles, disaggregated_aggregates, primes, non_primes, selected_non_primes, timestamp)

    def dataflow_singles_mode(self, neighbors, timestamp, iteration):
        """
        Assumption: 1. there exist input_contexts
        """
        # 1. collect all the contexts
        input_contexts = self.get_received_data()
        db_singles = self.get_database_singles(timestamp)
        inputs_in_standard_form = self.input.get_in_standard_from()
        history = self.context_history.get(timestamp)

        # 2. union, remove the redundancies
        combined_singles = ContextAggregator.remove_same_id_singles(input_contexts.union(db_singles))

        # 3. Run the selector with proper inputs
        new_info = contexts_to_standard(combined_singles)

        selector_result = OutputSelector(inputs=inputs_in_standard_form, context_history=history, new_info=new_info, neighbors=neighbors).run()
        return self.set_database_and_return(
            result = selector_result,
            new_aggregates = None,
            singles = combined_singles,
            aggregates = set(), primes = set(), non_primes = set(), selected_non_primes = set(), timestamp = timestamp)

    def is_this_new_timestamp(self, timestamp=0):
        """Checks if this is the start of timestamp, initially context database has {} in it,
        when it has any kind of data, it implies it's not new timestamp anymore

        >>> c = ContextAggregator()
        >>> c.is_this_new_timestamp()
        True
        >>> c.set_database(set(), set())
        >>> c.is_this_new_timestamp()
        False
        """

        if timestamp not in self.context_database.timestamp: return True
        else:
            return self.context_database.timestamp[timestamp] == {}

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

    def available_input_contexts(self):
        """Returns the received data from node_index
        >>> d = ContextAggregator()
        >>> d.receive(1, {Context(value=1.0, cohorts=[0,1,2]), Context(value=4.0, cohorts=[3], hopcount = 1)})
        >>> d.receive(2, {Context(value=2.0, cohorts=[0], hopcount=1), Context(value=4.0, cohorts=[4], hopcount = 10)})
        >>> d.available_input_contexts()
        True
        >>> d = ContextAggregator()
        >>> d.available_input_contexts()
        False
        """
        return len(self.get_received_data()) > 0

    ###################################
    # API
    ###################################

    def is_nothing_to_send(self):
        return is_empty_dictionary(self.output.dictionary)


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
        # if neighbor is None:
        #     for o in output_dictionary:
        #         single_contexts = self.output.generate_single_contexts(o=o, single_contexts=self.get_database_singles(timestamp))
        #         aggregate_context = self.output.generate_aggregate_contexts(o=o, aggregate_contexts={self.new_aggregate} | self.get_database_aggregates(timestamp))
        #         result[o] = single_contexts | aggregate_context
        #         self.context_history.add_to_history(node_number=o, value=output_dictionary[o], timestamp=timestamp)
        # else:
        assert type(neighbor) in [int, long]
        assert neighbor in output_dictionary
        #assert self.new_aggregate is not None, "aggregate is None"

        # TODO
        # Duplication of code
        o = neighbor
        single_contexts = self.output.generate_single_contexts(o=o, single_contexts=self.get_database_singles(timestamp))
        #print self.get_database_aggregates(timestamp)

        if not self.new_aggregate:
            new_aggregate = set()
        else:
            new_aggregate = {self.new_aggregate}
        aggregate_context = self.output.generate_aggregate_contexts(o=o, aggregate_contexts= (new_aggregate  | self.get_database_aggregates(timestamp)))
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

    def process_to_set_output(self, neighbors=None, timestamp=0, iteration=0):
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
            sampled_data, special_flag = ContextAggregator.sample(self.get_sample_data(), timestamp)
            # store the sampled data for comparison purposes
            self.data = sampled_data

            hopcount = 0
            if special_flag:
                hopcount = Context.SPECIAL_CONTEXT
            context = Context(value=sampled_data, cohorts=[self.id], hopcount=hopcount, timestamp=timestamp)
            self.set_database(singles={context}, aggregates=set(), timestamp=timestamp)

            # store the context in the history and process
            result = {}
            for h in neighbors:
                result[h] = [[self.id],[]]
        else:
            # process the early return
            result = {}
            if self.available_input_contexts(): # input_contexts: # if there is no inputs
                if self.is_aggregation_mode():
                    result, combined_singles, combined_aggregates, new_aggregates = self.dataflow_aggregations_mode(neighbors, timestamp, iteration)
                else:
                    result, combined_singles, combined_aggregates, new_aggregates = self.dataflow_singles_mode(neighbors, timestamp, iteration)

        # this also reset the actual_sent_dictionary
        self.output.set_dictionary(result)

        # WARNING! Don't forget the input is cleared after the process_to_set_output() call
        self.initalize_before_iteration()
        return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()
