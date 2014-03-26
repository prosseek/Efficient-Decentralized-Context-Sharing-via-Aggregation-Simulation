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
from aggregation_simulator.sample_data import SampleData
from aggregation_simulator.utils_report import report_generate

root_directory = os.path.dirname(os.path.abspath(__file__)) + "/tmp/"
test_name = "test_network1"
base_directory = os.path.join(root_directory, test_name)

class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def test_read(self):
        """
        Tests if the algorithm works fine
        """
        network_file = os.path.join(base_directory, "network.txt")

        network = Network()
        network.read(network_file)

        self.assertTrue(same({1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 6], 8: [7]},
                             network.get_network()))

if __name__ == "__main__":
    unittest.main(verbosity=2)