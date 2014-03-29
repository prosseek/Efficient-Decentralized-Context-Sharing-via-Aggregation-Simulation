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
from aggregation_simulator.utils import make_ready_for_test

from aggregation_simulator.network import Network
from context_aggregator.utils_same import same
from context_aggregator.context_aggregator import ContextAggregator
#from aggregation_simulator.aggregation_simulator import Host, execution_file_output
from aggregation_simulator.sample import Sample

d = get_test_files_directory()
network_file = os.path.join(d, "normal/test_network1/test_network1.txt")
network = Network()
network.read(network_file)
dot_file_path = os.path.join(d, network_file + ".dot")

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
        network = Network()
        network.read(network_file)
        network.dot_gen(dot_file_path)

    def test_with_file_aggregation(self):
        host_ids = network.get_host_ids() # [h0, h1, h2]
        hosts = []
        for h in host_ids:
            hosts.append(Host(h))
        neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

        test_directory, sample = make_ready_for_test("normal","test_network1","aggregate")

        config = {"hosts":hosts, "neighbors":neighbors,\
                  "test_directory":test_directory, "sample":sample, \
                  ContextAggregator.PM:ContextAggregator.AGGREGATION_MODE}

        simulation = AggregationSimulator.run(config=config)

    def test_with_file_singles_only(self):
        host_ids = network.get_host_ids() # [h0, h1, h2]
        hosts = []
        for h in host_ids:
            hosts.append(Host(h))
        neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

        test_directory, sample = make_ready_for_test("normal","test_network1","singles")

        config = {"hosts":hosts, "neighbors":neighbors,\
                  "test_directory":test_directory, "sample":sample, \
                  ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE}
        simulation = AggregationSimulator.run(config=config)

    def test_with_file_aggregation_marked_sample(self):
        host_ids = network.get_host_ids() # [h0, h1, h2]
        hosts = []
        for h in host_ids:
            hosts.append(Host(h))
        neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

        test_directory, sample = make_ready_for_test("marked_sample","test_network1","aggregate")

        config = {"hosts":hosts, "neighbors":neighbors,\
                  "test_directory":test_directory, "sample":sample, \
                  ContextAggregator.PM:ContextAggregator.AGGREGATION_MODE}

        simulation = AggregationSimulator.run(config=config)

if __name__ == "__main__":
    unittest.main(verbosity=2)