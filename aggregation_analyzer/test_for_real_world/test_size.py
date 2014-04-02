import unittest
import sys
import os


from utils import *

class TestSize(unittest.TestCase):
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

    def test_size_real_world_intel_10(self):
        """Size for real world intel 10

        [2358, 438, 1920]
        [2674, 743, 1931]
        [17188, 17188, 0]
        """
        self.run_to_get_received_data("real_world_intel_10")


    def test_size_real_world_intel_6(self):
        """Size for real world intel 6

        [1668, 176, 1492]
        [1800, 283, 1517]
        [5975, 5975, 0]
        """
        self.run_to_get_received_data("real_world_intel_6")


if __name__ == "__main__":
    unittest.main(verbosity=2)