import unittest
import sys
import os
from utils import make_ready_for_one_file_simulation

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from aggregation_simulator.utils_configuration import get_test_files_directory, get_configuration
from aggregation_simulator.network import Network
from aggregation_async_simulator import run_simulation
from context_aggregator.utils_same import same

test_name1 = "test_network0"
d = os.path.join(get_test_files_directory(), test_name1)
network_file_path1 = os.path.join(d, test_name1 + ".txt")
simulation_root_dir = get_configuration("config.cfg", "TestDirectory", "simple_test_root_dir")

network = Network()
network.read(network_file_path1)
dot_file_path = os.path.join(d, network_file_path1 + ".dot")

#
# Code duplication from utils.py
#
def get_test_network(condition, network_name):
    d = get_test_files_directory()
    network_file = os.path.join(d, "%s/%s/%s.txt" % (condition, network_name, network_name))
    network = Network()
    network.read(network_file)
    return network

def runit(simulation_root_dir, network_file_path, sample_file_path, condition, test_sub_name, disconnection_rate = 0.0, drop_rate=0.0, threshold=sys.maxint):
    network_dir = make_ready_for_one_file_simulation(simulation_root_dir=simulation_root_dir,
                                                     network_file_path=network_file_path,
                                                     sample_file_path=sample_file_path,
                                                     remove_existing_files=False)
    run_simulation.run_simulation(network_dir=network_dir,
                   condition=condition,
                   test_sub_name=test_sub_name,
                   disconnection_rate=disconnection_rate,
                   drop_rate=drop_rate,
                   threshold=threshold)

class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def test_with_aggr(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path1,
            "sample_file_path":None,
            "condition":"async",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0
        }
        return runit(**params)

if __name__ == "__main__":
    # http://stackoverflow.com/questions/1068246/python-unittest-how-to-run-only-part-of-a-test_for_real_world-file
    # selected_tests = unittest.TestSuite()
    # selected_tests.addTest(TestDotFile)
    # unittest.TextTestRunner().run(selected_tests)
    unittest.main(verbosity=2)