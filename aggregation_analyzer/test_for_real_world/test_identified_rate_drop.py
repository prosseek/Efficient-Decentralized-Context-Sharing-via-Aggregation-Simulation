import unittest
import sys
import os


from utils import *

class TestIdentifiedRateDrop(unittest.TestCase):
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

        -> 3% drop

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [90.39722222222227, 48, 54, 30.212222222222227, 16, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [92.31962962962969, 49, 54, 30.659259259259265, 16, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [100.0, 54, 54, 100.0, 54, 54]

        --> 8% drop rate

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [90.87777777777782, 49, 54, 29.183888888888895, 15, 54]
        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [89.4748148148149, 48, 54, 29.218148148148156, 15, 54]
        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [100.0, 54, 54, 100.0, 54, 54]

        --> 33% drop rate

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [99.58851851851853, 53, 54, 19.890185185185185, 10, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [81.9624074074074, 44, 54, 18.209444444444447, 9, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [99.76, 53, 54, 99.76, 53, 54]

        --> 50% drop rate

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [74.41611111111112, 40, 54, 15.157037037037036, 8, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [84.67166666666668, 45, 54, 15.26018518518518, 8, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [98.93685185185186, 53, 54, 98.93685185185186, 53, 54]
        """
        self.run_to_get_identified_data("real_world_intel_10_drop")


    def test_identified_real_world_intel_6(self):
        """Accuracy for real world intel 6

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [95.50944444444445, 51, 54, 16.356111111111108, 8, 54]
        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [92.11351851851859, 49, 54, 19.239074074074075, 10, 54]
        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [100.0, 54, 54, 100.0, 54, 54]

        -> 3% drop

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [90.15907407407411, 48, 54, 17.866851851851848, 9, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [99.6912962962963, 53, 54, 19.924629629629628, 10, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [99.96574074074073, 53, 54, 99.96574074074073, 53, 54]


        -> 8% drop

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [82.51148148148148, 44, 54, 15.602222222222215, 8, 54] --> 10 nodes info lost

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [87.7909259259259, 47, 54, 15.431296296296297, 8, 54] --> 2 more lost

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [92.62518518518525, 50, 54, 92.62518518518525, 50, 54]

        -> 33% drop

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [80.79666666666662, 43, 54, 12.071666666666667, 6, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [89.23462962962971, 48, 54, 11.317407407407407, 6, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [52.84555555555554, 28, 54, 52.84555555555554, 28, 54] --> dramatic lost

        --> 50% drop

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [36.86499999999999, 19, 54, 8.436666666666671, 4, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [42.69611111111111, 23, 54, 7.1329629629629645, 3, 54]

        [1.8499999999999985, 1, 54, 1.8499999999999985, 1, 54]
        [21.535185185185192, 11, 54, 21.535185185185192, 11, 54]
        """
        self.run_to_get_identified_data("real_world_intel_6_drop")


if __name__ == "__main__":
    unittest.main(verbosity=2)