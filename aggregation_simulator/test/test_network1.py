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

d = get_test_files_directory()
network_file = os.path.join(d, "normal/test_network1/test_network1.txt")
network = Network()
network.read(network_file)
dot_file_path = os.path.join(d, network_file + ".dot")

test_file_name = "test_network1_drop"
disconnection_rate = 0.5
drop_rate = 0.0

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

    def test_with_aggr(self):
        return runit("normal", test_file_name, "aggregates", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

    def test_with_single(self):
        return runit("normal", test_file_name, "singles", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

    def test_with_aggr_marked(self):
        return runit("marked_sample", test_file_name, "aggregates", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

    def test_with_single_marked(self):
        return runit("marked_sample", test_file_name, "singles", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

if __name__ == "__main__":
    # http://stackoverflow.com/questions/1068246/python-unittest-how-to-run-only-part-of-a-test_for_real_world-file
    # selected_tests = unittest.TestSuite()
    # selected_tests.addTest(TestDotFile)
    # unittest.TextTestRunner().run(selected_tests)
    unittest.main(verbosity=2)