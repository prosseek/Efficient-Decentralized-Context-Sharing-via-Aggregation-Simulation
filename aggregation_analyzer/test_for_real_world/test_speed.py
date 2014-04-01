import unittest
import sys
import os


from utils import *

class TestSpeed(unittest.TestCase):
    def setUp(self):
        pass

    #
    # Calculate received data
    #
    def run_to_get_speed_data(self, name, test_only_normal = False):
        def get_results_and_print(condition, kind):
            conditions = {"condition":condition, "name":name, "kind":kind} #, "timestamp":0}
            results = last_non_null_host_values_from_key(conditions)
            print [min(results), max(results), 1.0*sum(results)/len(results)]

        get_results_and_print("normal", "aggregates")
        if not test_only_normal: get_results_and_print("marked_sample", "aggregates")
        get_results_and_print("normal", "singles")

    def test_speed_real_world_intel_10(self):
        """Average speed for real world intel 10
        speed is defined by the average number of iterations for propagation of all the new values
        min/max/average

        [4, 12, 8.833333333333334]
        [6, 11, 8.351851851851851]
        [5, 8, 6.37037037037037]
        """
        self.run_to_get_speed_data("real_world_intel_10")


    def test_speed_real_world_intel_6(self):
        """Accuracy for real world intel 6

        [9, 16, 13.037037037037036]
        [8, 17, 12.37037037037037]
        [10, 15, 12.88888888888889]
        """
        self.run_to_get_speed_data("real_world_intel_6")


if __name__ == "__main__":
    unittest.main(verbosity=2)