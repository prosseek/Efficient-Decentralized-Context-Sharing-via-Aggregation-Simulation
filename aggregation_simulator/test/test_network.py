import unittest
import sys
import os
import re
import shutil

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from aggregation_simulator.network import Network
from context_aggregator.utils_same import same
from context_aggregator.context_aggregator import ContextAggregator
from execute_file import Host, execution_file_output
from aggregation_simulator.sample_data import SampleData

root_directory = os.path.dirname(os.path.abspath(__file__)) + "/tmp/"
test_name = "test_network1"
base_directory = os.path.join(root_directory, test_name)
sample_file = os.path.join(base_directory, "sample.txt")
sample = SampleData()
sample.read(sample_file)
network_file = os.path.join(base_directory, "network.txt")
network = Network()
network.read(network_file)

class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def test_read(self):
        """
        Tests if the algorithm works fine
        """
        self.assertTrue(same({1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 6], 8: [7]},
                             network.get_network()))

    def test_get_hosts(self):
        h = network.get_host_ids()
        self.assertTrue(sorted(h) == [1,2,3,4,5,6,7,8])

    def test_dot_gen(self):
        network_file = os.path.join(base_directory, "network.txt")
        dot_file = os.path.join(base_directory, "network.dot")

        network = Network()
        network.read(network_file)
        network.dot_gen(dot_file)

    def test_with_file_aggregation(self):
        host_ids = network.get_host_ids() # [h0, h1, h2]
        hosts = []
        for h in host_ids:
            hosts.append(Host(h))
        neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

        test_kind = "aggregation"
        test_directory = os.path.join(base_directory, test_kind)
        config = {"sample":sample, "test_directory":test_directory, ContextAggregator.PM:ContextAggregator.AGGREGATION_MODE}
        execution_file_output(hosts=hosts, neighbors=neighbors, config=config)

    def test_with_file_singles_only(self):
        host_ids = network.get_host_ids() # [h0, h1, h2]
        hosts = []
        for h in host_ids:
            hosts.append(Host(h))
        neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

        test_kind = "singles_only"
        test_directory = os.path.join(base_directory, test_kind)
        config = {"sample":sample, "test_directory":test_directory, ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE}
        execution_file_output(hosts=hosts, neighbors=neighbors, config=config)

if __name__ == "__main__":
    unittest.main(verbosity=2)