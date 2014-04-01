import unittest
import sys
import os


from utils import *

class TestCohorts(unittest.TestCase):
    def setUp(self):
        pass

    #
    # Calculate received data
    #
    def run_to_get_cohorts_data(self, name, test_only_normal = False):
        def get_results_and_print(condition, kind):
            conditions = {"condition":condition, "name":name, "kind":kind} #, "timestamp":0}
            results = first_host_values_from_key(conditions, "Average number of cohorts")
            print avg_lists(results)
            results = last_host_values_from_key(conditions, "Average number of cohorts")
            print avg_lists(results)
            print max_lists(results)
            print min_lists(results)

        get_results_and_print("normal", "aggregates")
        if not test_only_normal: get_results_and_print("marked_sample", "aggregates")
        get_results_and_print("normal", "singles")

    def test_cohorts_real_world_intel_10(self):
        """Cohorts for real world intel 10

        # aggr start 0 upto 3.27 elements on average per one cohort
        [0.0, 0, 0]
        [3.2781481481481487, 42, 13]
        [4.27, 49, 17] --> max
        [2.29, 35, 11] --> min

        # with marked sample, the number reduces a little bit.
        [0.0, 0, 0]
        [3.1988888888888876, 39, 12]
        [5.22, 50, 18] --> max
        [2.22, 25, 9]  --> min

        # There is no cohort in singles
        [0.0, 0, 0]
        [0.0, 0, 0]
        """
        self.run_to_get_cohorts_data("real_world_intel_10")


    def test_cohorts_real_world_intel_10(self):
        """Cohorts for real world intel 6

        [0.0, 0, 0]
        [3.2781481481481487, 42, 13]
        [0.0, 0, 0]
        [3.1988888888888876, 39, 12]
        [0.0, 0, 0]
        [0.0, 0, 0]
        """
        self.run_to_get_cohorts_data("real_world_intel_6")


if __name__ == "__main__":
    unittest.main(verbosity=2)