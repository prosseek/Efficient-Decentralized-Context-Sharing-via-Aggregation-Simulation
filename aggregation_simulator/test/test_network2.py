import unittest
import sys
import os
from utils import *

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from aggregation_simulator.utils_configuration import *
from aggregation_simulator.network import Network
from context_aggregator.utils_same import same

d = os.path.join(get_test_files_directory(), "test_network2")
test_name = "test_network2"
network_file_path = os.path.join(d, test_name + ".txt")
simulation_root_dir = get_configuration("config.cfg", "TestDirectory", "simple_test_root_dir")

network = Network()
network.read(network_file_path)
dot_file_path = os.path.join(d, network_file_path + ".dot")

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
        network.read(network_file_path)
        network.dot_gen(dot_file_path)

    def test_with_aggr(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path,
            "sample_file_path":None,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0
        }
        return runit(**params)

    def test_with_single(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path,
            "sample_file_path":None,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0
        }
        return runit(**params)

    # def test_with_aggr_marked(self):
    #     return runit("marked_sample", test_file_name, "aggregates", disconnection_rate=disconnection_rate,drop_rate=drop_rate)
    #
    # def test_with_single_marked(self):
    #     return runit("marked_sample", test_file_name, "singles", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

if __name__ == "__main__":
    # http://stackoverflow.com/questions/1068246/python-unittest-how-to-run-only-part-of-a-test_for_real_world-file
    # selected_tests = unittest.TestSuite()
    # selected_tests.addTest(TestDotFile)
    # unittest.TextTestRunner().run(selected_tests)
    unittest.main(verbosity=2)