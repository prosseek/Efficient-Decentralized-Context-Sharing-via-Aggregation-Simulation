import unittest
import sys
import os


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

    def test_size_real_world_intel_10(self):
        """Size for real world intel 10

        -> 3% drop

        -> 8% drop

        -> 33% drop

        -> 50% drop

        """
        self.run_to_get_received_data("real_world_intel_10_drop")


    def test_size_real_world_intel_6(self):
        """Size for real world intel 6

        [1668, 176, 1492]
        [1800, 283, 1517]
        [5975, 5975, 0]

        --> drop rate 3%

        [1650, 275, 1375] > receive
        [1694, 284, 1410] > sent

        [1855, 274, 1581] > receive
        [1909, 283, 1626] > sent

        [5845, 5845, 0] -> receive
        [6015, 6015, 0] -> sent


        --> drop rate 8%

        [1422, 263, 1159] > receive
        [1530, 285, 1245] > sent

        [1541, 266, 1275] > receive
        [1669, 286, 1383] > sent

        [5191, 5191, 0] > receive
        [5674, 5674, 0] > sent

        --> drop rate 33%

        [836, 160, 676]
        [1293, 252, 1041]
        [943, 147, 796]
        [1407, 222, 1185]
        [2466, 2466, 0]
        [3718, 3718, 0]

        --> drop rate 50%

        [426, 153, 273]
        [824, 276, 548]
        [436, 100, 336]
        [847, 186, 661]
        [854, 854, 0]
        [1604, 1604, 0]

        """
        self.run_to_get_received_data("real_world_intel_6_drop")


if __name__ == "__main__":
    unittest.main(verbosity=2)