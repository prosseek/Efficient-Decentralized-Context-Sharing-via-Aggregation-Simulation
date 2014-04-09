import unittest
import sys
import os

from aggregation_analyzer.read_reports import ReadReports
from aggregation_analyzer.utils_location import *
from aggregation_analyzer.get_statistics import GetStatistics


class TestForRealWorld(unittest.TestCase):
    def setUp(self):
        pass

    def get(self, network_dir, condition):
        d = ReadReports(network_dir)
        s = GetStatistics(d)
        print s.get_size(condition)
        print s.get_accuracy(condition)
        print s.get_identified_rate(condition)
        print s.get_speed(condition)
        print s.get_cohorts(condition)

    def test_intel6(self):
        network_dir = os.path.join(get_intel_test_dir(), "real_world_intel_6")
        condition = 'normal'
        self.get(network_dir, condition)
        # (([5975, 5975, 0], [5975, 5975, 0]), ([1623, 176, 1447], [1623, 176, 1447]))
        # ([100.0, 100.0], [99.60333333333335, 98.11074074074077])
        # ([100.0, 54, 54, 100.0, 54, 54], [89.67888888888898, 48, 54, 16.459629629629635, 8, 54])
        # ([12.88888888888889, 10, 15], [12.222222222222221, 8, 17])
        # ([0.0, 0, 0], [3.268148148148148, 39, 12])

    def test_intel10(self):
        network_dir = os.path.join(get_intel_test_dir(), "real_world_intel_10")
        condition = 'normal'
        self.get(network_dir, condition)
        # (([17188, 17188, 0], [17188, 17188, 0]), ([2194, 438, 1756], [2194, 438, 1756]))
        # ([100.0, 100.0], [99.66814814814815, 98.31555555555555])
        # ([100.0, 54, 54, 100.0, 54, 54], [90.70740740740744, 48, 54, 28.87518518518518, 15, 54])
        # ([6.37037037037037, 5, 8], [8.0, 5, 11])
        # ([0.0, 0, 0], [3.777962962962962, 33, 9])

    def test_pseudo30(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_30")
        condition = 'normal'
        self.get(network_dir, condition)
        # (([714559, 714559, 0], [714559, 714559, 0]), ([8044, 2252, 5792], [8044, 2252, 5792]))
        # ([100.0, 100.0], [98.51694214876028, 94.34024793388431])
        # ([100.0, 484, 484, 100.0, 484, 484], [7.926074380165298, 38, 484, 1.2761776859504115, 6, 484])
        # ([24.880165289256198, 17, 32], [8.072314049586776, 3, 20])
        # ([0.0, 0, 0], [5.856466942148763, 32, 5])
    def test_pseudo50(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_50")
        condition = 'normal'
        self.get(network_dir, condition)
        # (([17188, 17188, 0], [17188, 17188, 0]), ([2194, 438, 1756], [2194, 438, 1756]))
        # ([100.0, 100.0], [99.66814814814815, 98.31555555555555])
        # ([100.0, 54, 54, 100.0, 54, 54], [90.70740740740744, 48, 54, 28.87518518518518, 15, 54])
        # ([6.37037037037037, 5, 8], [8.0, 5, 11])
        # ([0.0, 0, 0], [3.777962962962962, 33, 9])

    #
    def test_pseudo30_th5(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_30")
        condition = 'th5'
        self.get(network_dir, condition)
    def test_pseudo50_th5(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_50")
        condition = 'th5'
        self.get(network_dir, condition)

if __name__ == "__main__":
    unittest.main(verbosity=2)