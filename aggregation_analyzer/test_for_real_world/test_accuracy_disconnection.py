import unittest
import sys
import os


from utils import *

class TestAccuracyDisconnection(unittest.TestCase):
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

        -> Disconnection rate 3%

        -> Disconnection rate 8%

        -> Disconnection rate 33%

        -> Disconnection rate 50%
        [96.06888888888892, 94.59185185185184]
        [99.84425925925925, 98.26425925925929]

        [96.06888888888892, 94.59185185185184]
        [99.59629629629625, 98.01425925925926]

        [96.06888888888892, 94.59185185185184]
        [100.0, 100.0] <-- ???
        """
        self.run_to_get_accuracy_data("real_world_intel_10_drop")


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

        --> 3% drop

        --> With 8% package drop rate

        --> With 33% drop

        --> 50% drop

        [96.06888888888892, 94.59185185185184]
        [98.51055555555557, 97.12055555555555]

        [96.06888888888892, 94.59185185185184]
        [98.76148148148148, 97.41722222222222]

        [96.06888888888892, 94.59185185185184]
        [99.67314814814816, 99.59537037037038]
        """
        self.run_to_get_accuracy_data("real_world_intel_6_drop")


if __name__ == "__main__":
    unittest.main(verbosity=2)