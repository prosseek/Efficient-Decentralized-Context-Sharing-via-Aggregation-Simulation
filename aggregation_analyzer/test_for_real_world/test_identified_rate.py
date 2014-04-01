import unittest
import sys
import os


from utils import *

class TestIdentifiedRate(unittest.TestCase):
    def setUp(self):
        pass

    #
    # Calculate received data
    #
    def run_to_get_identified_data(self, name, test_only_normal = False):
        def get_results_and_print(condition, kind):
            conditions = {"condition":condition, "name":name, "kind":kind} #, "timestamp":0}
            results = first_host_values_from_key(conditions, "Identified rate")
            print avg_lists(results)
            results = last_host_values_from_key(conditions, "Identified rate")
            print avg_lists(results)

        get_results_and_print("normal", "aggregates")
        if not test_only_normal: get_results_and_print("marked_sample", "aggregates")
        get_results_and_print("normal", "singles")

    def test_identified_real_world_intel_10(self):
        """Size for real world intel 10

        # for aggregation, identified rate changes from 1/54 to 50/54 on average
        # but for single it stays 15/54
        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [92.59388888888888, 50, 54, 28.429629629629616, 15, 54]

        # for marked aggregation, identified rate changes from 1/54 to 50/54 on average
        # but for single, we have one more 15/54
        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [92.73092592592594, 50, 54, 29.698148148148153, 16, 54]

        # single ultimately becomes 100%
        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [100.0, 54, 54, 100.0, 54, 54]
        """
        self.run_to_get_identified_data("real_world_intel_10")


    def test_identified_real_world_intel_6(self):
        """Accuracy for real world intel 6

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [95.50944444444445, 51, 54, 16.356111111111108, 8, 54]
        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [92.11351851851859, 49, 54, 19.239074074074075, 10, 54]
        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [100.0, 54, 54, 100.0, 54, 54]
        """
        self.run_to_get_identified_data("real_world_intel_6")


if __name__ == "__main__":
    unittest.main(verbosity=2)