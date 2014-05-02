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
        d = ReadReports(network_dir, auto_read=auto_read, use_cache=use_cache)
        s = GetStatistics(d)

        #self test
        # for i in range(1, 55):
        #     dictionary = d.report['normal']['singles']['host%d' % i]
        #     last_key = sorted(dictionary.keys())[-1]
        #     print dictionary[last_key]

        print s.get_size(condition)
        print s.get_accuracy(condition)
        print s.get_identified_rate(condition)
        print s.get_speed(condition)
        print s.get_cohorts(condition)

    # *******************
    def test_intel6_tree(self):
        network_dir = os.path.join(get_intel_test_dir(), "real_world_intel_6_tree")
        condition = 'normal'
        self.get(network_dir, condition, use_cache = False)
        # (([2862, 2862, 0], [2862, 2862, 0]), ([1570, 106, 1464], [1570, 106, 1464]))
        # ([100.0, 100.0], [99.76648148148149, 98.58425925925923])
        # ([100.0, 54, 54, 100.0, 54, 54], [93.41592592592593, 50, 54, 31.61870370370371, 17, 54])
        # ([26.11111111111111, 18, 34], [23.574074074074073, 18, 25])
        # ([0.0, 0, 0], [2.672407407407407, 33, 12])


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
        self.get(network_dir, condition, use_cache = False)
        # (([28537, 28537, 0], [28537, 28537, 0]), ([6578, 436, 6142], [6578, 436, 6142]))
        # ([100.0, 100.0], [99.64469999999997, 96.00010000000002])
        # ([100.0, 100, 100, 100.0, 100, 100], [72.9, 72, 100, 10.6, 10, 100])
        # ([11.31, 8, 14], [19.2, 15, 23])
        # ([0.0, 0, 0], [5.114300000000002, 62, 12])

    def test_pseudo70_2d(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_70_2d")
        condition = 'normal'
        self.get(network_dir, condition,  use_cache = False)
        # (([13705, 13705, 0], [13705, 13705, 0]), ([5210, 254, 4956], [5210, 254, 4956]))
        # ([100.0, 100.0], [99.70270000000004, 95.97559999999994])
        # ([100.0, 100, 100, 100.0, 100, 100], [82.78, 82, 100, 7.55, 7, 100])
        # ([18.45, 13, 22], [28.64, 21, 38])
        # ([0.0, 0, 0], [3.5669999999999993, 75, 21])

    #########################

    def test_pseudo100(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_100")
        condition = 'normal'
        self.get(network_dir, condition, use_cache = False)
        # (([28537, 28537, 0], [28537, 28537, 0]), ([6578, 436, 6142], [6578, 436, 6142]))
        # ([100.0, 100.0], [99.64469999999997, 96.00010000000002])
        # ([100.0, 100, 100, 100.0, 100, 100], [72.9, 72, 100, 10.6, 10, 100])
        # ([11.31, 8, 14], [19.2, 15, 23])
        # ([0.0, 0, 0], [5.114300000000002, 62, 12])

    def test_pseudo100_2d(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_100_2d")
        condition = 'normal'
        self.get(network_dir, condition,  use_cache = False)
        # (([13705, 13705, 0], [13705, 13705, 0]), ([5210, 254, 4956], [5210, 254, 4956]))
        # ([100.0, 100.0], [99.70270000000004, 95.97559999999994])
        # ([100.0, 100, 100, 100.0, 100, 100], [82.78, 82, 100, 7.55, 7, 100])
        # ([18.45, 13, 22], [28.64, 21, 38])
        # ([0.0, 0, 0], [3.5669999999999993, 75, 21])

    def test_pseudo49_tree(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_49_tree")
        condition = 'normal'
        self.get(network_dir, condition, use_cache = False)
        # (([2352, 2352, 0], [2352, 2352, 0]), ([1065, 96, 969], [1065, 96, 969]))
        # ([100.0, 100.0], [100.0, 96.35795918367347])
        # ([100.0, 49, 49, 100.0, 49, 49], [100.0, 49, 49, 17.91, 8, 49])
        # ([18.408163265306122, 13, 23], [18.408163265306122, 13, 23])
        # ([0.0, 0, 0], [2.9073469387755098, 40, 13])

    def test_pseudo49(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_49")
        condition = 'normal'
        self.get(network_dir, condition, use_cache = False)
        #(([4116, 4116, 0], [4116, 4116, 0]), ([1664, 168, 1496], [1664, 168, 1496]))
        #([100.0, 100.0], [99.61306122448981, 95.72367346938776])
        #([100.0, 49, 49, 100.0, 49, 49], [84.8393877551021, 41, 49, 13.908979591836735, 6, 49])
        #([10.346938775510203, 7, 12], [13.73469387755102, 11, 16])
        #([0.0, 0, 0], [4.3310204081632655, 34, 8])

    def test_pseudo49_2d(self):
        network_dir = os.path.join(get_pseudo_test_dir(), "pseudo_realworld_49_2d")
        condition = 'normal'
        self.get(network_dir, condition,  use_cache = False)
        #(([2891, 2891, 0], [2891, 2891, 0]), ([1364, 118, 1246], [1364, 118, 1246]))
        #([100.0, 100.0], [99.8328571428571, 96.10999999999999])
        #([100.0, 49, 49, 100.0, 49, 49], [92.79653061224495, 45, 49, 15.658571428571435, 7, 49])
        #([12.040816326530612, 10, 13], [17.163265306122447, 14, 19])
        #([0.0, 0, 0], [3.018571428571429, 37, 12])
if __name__ == "__main__":
    unittest.main(verbosity=2)