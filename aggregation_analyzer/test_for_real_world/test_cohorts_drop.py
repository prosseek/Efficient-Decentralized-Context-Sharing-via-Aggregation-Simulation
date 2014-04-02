import unittest
import sys
import os


from utils import *

class TestCohortsDrop(unittest.TestCase):
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
        [3.1988888888888876, 39, 12]
        [5.22, 50, 18] --> max
        [2.22, 25, 9]  --> min

        --> 3%
        # aggr
        [3.3609259259259243, 39, 12]
        [6.67, 47, 17]
        [2.24, 29, 6]

        # aggr with marked data
        [3.3031481481481495, 43, 13]
        [6.0, 50, 19]
        [2.26, 34, 7]

        --> 33%

        [6.281666666666666, 37, 6] larger average cohorts number due to the lost number of aggregates
        [14.33, 46, 9]
        [3.89, 17, 3]

        [5.488333333333333, 42, 8]
        [8.0, 50, 12]
        [3.42, 21, 4]

        --> 50%
        [5.729814814814815, 15, 2]
        [29.0, 32, 5]
        [0.0, 0, 0]

        [5.189444444444445, 19, 3]
        [11.5, 31, 7]
        [2.0, 2, 1]
        """
        self.run_to_get_cohorts_data("real_world_intel_10_drop")


    def test_cohorts_real_world_intel_10(self):
        """Cohorts for real world intel 6

        [3.2781481481481487, 42, 13]
        [3.1988888888888876, 39, 12]

        -> 3% drop

        # aggr
        [3.3609259259259243, 39, 12] -> avg
        [6.67, 47, 17] -> max
        [2.24, 29, 6] -> min

        # aggr with marked data
        [3.3031481481481495, 43, 13]
        [6.0, 50, 19]
        [2.26, 34, 7]

        -> 33% drop

        [6.281666666666666, 37, 6]
        [14.33, 46, 9]
        [3.89, 17, 3]

        [5.488333333333333, 42, 8]
        [8.0, 50, 12]
        [3.42, 21, 4]

        -> 50% drop

        [5.729814814814815, 15, 2]
        [29.0, 32, 5]
        [0.0, 0, 0]

        [5.189444444444445, 19, 3]
        [11.5, 31, 7]
        [2.0, 2, 1]
        """
        self.run_to_get_cohorts_data("real_world_intel_6_drop")


if __name__ == "__main__":
    unittest.main(verbosity=2)