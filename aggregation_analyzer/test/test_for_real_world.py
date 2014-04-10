import unittest
import sys
import os

from aggregation_analyzer.read_reports import ReadReports
from aggregation_analyzer.utils_location import *
from aggregation_analyzer.get_statistics import GetStatistics


class TestForRealWorld(unittest.TestCase):
    def setUp(self):
        pass

    def get(self, network_dir, condition, auto_read = True, use_cache = True):
        d = ReadReports(network_dir, auto_read, use_cache)
        s = GetStatistics(d)
        print s.get_size(condition)
        print s.get_accuracy(condition)
        print s.get_identified_rate(condition)
        print s.get_speed(condition)
        print s.get_cohorts(condition)

    # *******************

    def test_intel6(self):
        network_dir = os.path.join(get_intel_test_dir(), "real_world_intel_6")
        condition = 'normal'
        self.get(network_dir, condition, use_cache = False)
        #(([5975, 5975, 0], [5975, 5975, 0]), ([2031, 176, 1855], [2031, 176, 1855]))
        #([100.0, 100.0], [99.84166666666667, 98.1933333333334])
        #([100.0, 54, 54, 100.0, 54, 54], [94.95944444444443, 51, 54, 16.459814814814813, 8, 54])
        #([12.88888888888889, 10, 15], [15.296296296296296, 12, 18])
        #([0.0, 0, 0], [3.2903703703703706, 42, 13])

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

    #########################
    def test_pseudo70(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_70")
        condition = 'normal'
        self.get(network_dir, condition)
        #(([28537, 28537, 0], [28537, 28537, 0]), ([6385, 436, 5949], [6385, 436, 5949]))
        #([100.0, 100.0], [99.7032, 95.90099999999995])
        #([100.0, 100, 100, 100.0, 100, 100], [69.31, 69, 100, 9.7, 9, 100])
        #([11.31, 8, 14], [18.82, 16, 23])
        #([0.0, 0, 0], [5.7249, 59, 10])

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