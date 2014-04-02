import unittest
import sys
import os


from utils import *

class TestSpeedDrop(unittest.TestCase):
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

        [4, 12, 8.833333333333334] <- aggr
        [6, 11, 8.351851851851851] <- aggr with marked
        [5, 8, 6.37037037037037]   <- single

        -> drop 3%

        [5, 9, 7.351851851851852] <- avg
        [6, 9, 7.185185185185185]
        [5, 8, 6.481481481481482]

        -> drop 8%

        [5, 10, 7.611111111111111]
        [6, 14, 10.092592592592593]
        [5, 8, 6.592592592592593]

        -> drop 33%

        [7, 12, 9.851851851851851]
        [5, 12, 9.0]
        [6, 10, 7.87037037037037]

        -> drop 50%

        [6, 17, 11.703703703703704]
        [8, 13, 10.777777777777779]
        [8, 11, 9.38888888888889]
        """
        self.run_to_get_speed_data("real_world_intel_10_drop")


    def test_speed_real_world_intel_6(self):
        """Accuracy for real world intel 6

        [9, 16, 13.037037037037036]
        [8, 17, 12.37037037037037]
        [10, 15, 12.88888888888889]

        -> drop 3%

        [9, 18, 12.333333333333334]
        [10, 19, 15.185185185185185]
        [10, 15, 13.148148148148149]

        -> drop 8%

        [9, 15, 11.407407407407407]
        [10, 17, 12.148148148148149]
        [11, 20, 15.277777777777779]

        -> drop 33%

        [10, 25, 18.796296296296298]
        [10, 24, 16.574074074074073]
        [10, 22, 15.944444444444445]

        -> drop 50%

        [1, 18, 10.166666666666666]
        [3, 17, 10.314814814814815]
        [2, 19, 12.277777777777779]

        """
        self.run_to_get_speed_data("real_world_intel_6_drop")


if __name__ == "__main__":
    unittest.main(verbosity=2)