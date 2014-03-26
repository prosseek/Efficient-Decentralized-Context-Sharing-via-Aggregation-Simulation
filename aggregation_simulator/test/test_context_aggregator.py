import unittest
import sys
import os
import re
import shutil

from context_aggregator.context_aggregator import ContextAggregator

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

root_directory = os.path.dirname(os.path.abspath(__file__)) + "/tmp/"
test_name = "test1"
base_directory = os.path.join(root_directory, test_name)
# The directory where the results are stored in file

from execute_file import Host, execution_file_output
from aggregation_simulator.sample_data import SampleData

sample = SampleData()
sample_file = os.path.join(base_directory, "sample.txt")
sample.read(sample_file)

class TestContextAggregator(unittest.TestCase):
    def setUp(self):
        pass

    def test_with_aggregation(self):
        h0 = Host(0)
        h1 = Host(1)
        h2 = Host(2)
        hosts = [h0, h1, h2]
        neighbors = {0:[1], 1:[0,2], 2:[1]}

        test_kind = "aggregation"
        test_directory = os.path.join(base_directory, test_kind)
        config = {"sample":sample, "test_directory":test_directory}
        execution_file_output(hosts=hosts, neighbors=neighbors, config=config)

    def test_with_singles_only(self):
        h0 = Host(0)
        h1 = Host(1)
        h2 = Host(2)
        hosts = [h0, h1, h2]
        neighbors = {0:[1], 1:[0,2], 2:[1]}

        test_kind = "singles_only"
        test_directory = os.path.join(base_directory, test_kind)
        config = {"sample":sample, "test_directory":test_directory, ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE}
        execution_file_output(hosts=hosts, neighbors=neighbors, config=config)

if __name__ == "__main__":
    unittest.main(verbosity=2)