import unittest
import sys
import os
import sys

test_for_real_world = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + "test_for_real_world"
sys.path.insert(0, test_for_real_world)

from utils import *

class TestSizeDisconnection(unittest.TestCase):
    def setUp(self):
        pass

    #
    # Calculate received data
    #
    def run_to_get_received_data(self, name, test_only_normal = False):
        def get_results_and_print(condition, kind):
            conditions = {"condition":condition, "name":name, "kind":kind} #, "timestamp":0}
            results = sum_host_values_from_key(conditions, "Received")
            print sum_lists(results)
            results = sum_host_values_from_key(conditions, "Sent")
            print sum_lists(results)

        get_results_and_print("normal", "aggregates")
        if not test_only_normal: get_results_and_print("marked_sample","aggregates")
        get_results_and_print("normal", "singles")

    def test_size_test1(self):
        """
        [42, 14, 28]

        [54, 26, 28]

        [56, 56, 0]

        -> 3% drop

        -> 8% drop

        -> 33% drop

        -> 50% drop

        [17, 9, 8]

        [21, 12, 9]

        [42, 42, 0]

        """
        self.run_to_get_received_data("test_network1")

if __name__ == "__main__":
    unittest.main(verbosity=2)
from utils import *

class TestSizeDisconnection(unittest.TestCase):
    def setUp(self):
        pass

    #
    # Calculate received data
    #
    def run_to_get_received_data(self, name, test_only_normal = False):
        def get_results_and_print(condition, kind):
            conditions = {"condition":condition, "name":name, "kind":kind} #, "timestamp":0}
            results = sum_host_values_from_key(conditions, "Received")
            print sum_lists(results)
            results = sum_host_values_from_key(conditions, "Sent")
            print sum_lists(results)

        get_results_and_print("normal", "aggregates")
        if not test_only_normal: get_results_and_print("marked_sample","aggregates")
        get_results_and_print("normal", "singles")

    def test_size_test1(self):
        """
        [42, 14, 28]

        [54, 26, 28]

        [56, 56, 0]

        -> 3% drop

        -> 8% drop

        -> 33% drop

        -> 50% drop

        [17, 9, 8]

        [21, 12, 9]

        [42, 42, 0]

        """
        self.run_to_get_received_data("test_network1")

if __name__ == "__main__":
    unittest.main(verbosity=2)