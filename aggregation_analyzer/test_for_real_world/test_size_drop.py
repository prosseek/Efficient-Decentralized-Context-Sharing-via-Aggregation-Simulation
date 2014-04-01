import unittest
import sys
import os


from utils import *

class TestSizeDrop(unittest.TestCase):
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

        -> 3% drop

        [2447, 719, 1728]
        [2533, 749, 1784]

        [2505, 720, 1785]
        [2586, 745, 1841]

        [16816, 16816, 0]
        [17322, 17322, 0]

        -> 8% drop

        [2313, 685, 1628] -> receive
        [2522, 749, 1773] -> sent

        [2482, 694, 1788] -> receive
        [2692, 752, 1940] -> sent

        [16265, 16265, 0] -> receive
        [17564, 17564, 0] -> sent

        -> 33% drop

        [1939, 528, 1411]
        [2861, 771, 2090]

        [1587, 493, 1094]
        [2409, 773, 1636]

        [12282, 12282, 0]
        [18633, 18633, 0]

        --> 50% drop

        [1294, 374, 920]
        [2669, 785, 1884]

        [1321, 390, 931]
        [2643, 790, 1853]

        [9588, 9588, 0]
        [19339, 19339, 0]
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