import unittest
import sys
import os


from utils import *

class TestAccuracy(unittest.TestCase):
    def setUp(self):
        pass

    #
    # Calculate received data
    #
    def run_to_get_accuracy_data(self, name, test_only_normal = False):
        def get_results_and_print(condition, kind):
            conditions = {"condition":condition, "name":name, "kind":kind} #, "timestamp":0}
            results = first_host_values_from_key(conditions, "% precision")
            print avg_lists(results)
            results = last_host_values_from_key(conditions, "% precision")
            print avg_lists(results)

        get_results_and_print("normal", "aggregates")
        if not test_only_normal: get_results_and_print("marked_sample", "aggregates")
        get_results_and_print("normal", "singles")

    def test_accuracy_real_world_intel_10(self):
        """Size for real world intel 10

        # aggr start and end
        [96.06888888888892, 94.59185185185184]
        [99.60351851851858, 98.3924074074074]
        # aggr (marked) start and end
        [96.06888888888892, 94.59185185185184]
        [99.6457407407408, 98.50351851851856]
        # single start and end
        [96.06888888888892, 94.59185185185184]
        [100.0, 100.0]
        """
        self.run_to_get_accuracy_data("real_world_intel_10")


    def test_accuracy_real_world_intel_6(self):
        """Accuracy for real world intel 6

        [96.06888888888892, 94.59185185185184]
        [99.84629629629634, 98.35388888888889]
        # aggr (marked) start and end
        [96.06888888888892, 94.59185185185184]
        [99.68666666666674, 98.32055555555553]
        # single start and end
        [96.06888888888892, 94.59185185185184]
        [100.0, 100.0]
        """
        self.run_to_get_accuracy_data("real_world_intel_6")


if __name__ == "__main__":
    unittest.main(verbosity=2)