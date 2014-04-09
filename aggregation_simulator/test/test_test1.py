import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.context_aggregator import ContextAggregator
from aggregation_simulator.utils_configuration import *
from aggregation_simulator.host import Host
from aggregation_simulator.aggregation_simulator import AggregationSimulator
from aggregation_simulator.utils import *

class TestContextAggregator(unittest.TestCase):
    def setUp(self):
        pass

    # def test_with_aggregation(self):
    #     h0 = Host(0)
    #     h1 = Host(1)
    #     h2 = Host(2)
    #     hosts = [h0, h1, h2]
    #     neighbors = {0:[1], 1:[0,2], 2:[1]}
    #
    #     test_files_directory = get_test_files_directory()
    #     test_directory, sample = make_ready_for_test(test_files_directory,"normal","test1","aggregate")
    #
    #     config = {"hosts":hosts, "neighbors":neighbors,\
    #               "test_directory":test_directory, "sample":sample, \
    #               ContextAggregator.PM:ContextAggregator.AGGREGATION_MODE}
    #
    #     simulation = AggregationSimulator.run(config=config)
    #
    # def test_with_singles_only(self):
    #     h0 = Host(0)
    #     h1 = Host(1)
    #     h2 = Host(2)
    #     hosts = [h0, h1, h2]
    #     neighbors = {0:[1], 1:[0,2], 2:[1]}
    #
    #     test_files_directory = get_test_files_directory()
    #     test_directory, sample = make_ready_for_test(test_files_directory, "normal","test1","singles")
    #     config = {"hosts":hosts, "neighbors":neighbors,\
    #               "test_directory":test_directory, "sample":sample, \
    #               ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE}
    #
    #     simulation = AggregationSimulator.run(config=config, timestamp=0)

if __name__ == "__main__":
    unittest.main(verbosity=2)