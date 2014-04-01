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

disconnection_rate = 0.5

class TestNetworkDisconnection(unittest.TestCase):
    def setUp(self):
        pass

    def test_with_file_aggregation(self):
        host_ids = network.get_host_ids() # [h0, h1, h2]
        hosts = []
        for h in host_ids:
            hosts.append(Host(h))
        neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

        test_directory, sample = make_ready_for_test("normal","test_network1_drop","aggregates")

        config = {"hosts":hosts, "neighbors":neighbors,\
                  "test_directory":test_directory, "sample":sample, \
                  ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE,\
                  "disconnection_rate":disconnection_rate
            }

        simulation = AggregationSimulator.run(config=config)

    def test_with_file_singles_only(self):
        host_ids = network.get_host_ids() # [h0, h1, h2]
        hosts = []
        for h in host_ids:
            hosts.append(Host(h))
        neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

        test_directory, sample = make_ready_for_test("normal","test_network1_drop","singles")

        config = {"hosts":hosts, "neighbors":neighbors,\
                  "test_directory":test_directory, "sample":sample, \
                  ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE,\
                  "disconnection_rate":disconnection_rate
            }
        simulation = AggregationSimulator.run(config=config)

    def test_with_file_aggregation_marked_sample(self):
        host_ids = network.get_host_ids() # [h0, h1, h2]
        hosts = []
        for h in host_ids:
            hosts.append(Host(h))
        neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

        test_directory, sample = make_ready_for_test("marked_sample","test_network1_drop","aggregates")

        config = {"hosts":hosts, "neighbors":neighbors,\
                  "test_directory":test_directory, "sample":sample, \
                  ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE,\
                  "disconnection_rate":disconnection_rate
            }

        simulation = AggregationSimulator.run(config=config)


if __name__ == "__main__":
    # http://stackoverflow.com/questions/1068246/python-unittest-how-to-run-only-part-of-a-test_for_real_world-file
    # selected_tests = unittest.TestSuite()
    # selected_tests.addTest(TestDotFile)
    # unittest.TextTestRunner().run(selected_tests)
    unittest.main(verbosity=2)