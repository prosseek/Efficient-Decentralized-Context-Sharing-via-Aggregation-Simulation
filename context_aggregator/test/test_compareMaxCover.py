import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from test_maxcover import *
from context_aggregator.greedy_maxcover import GreedyMaxCover

data1 = [[9, 54], [8, 10], [20, 21, 47], [31, 32, 34], [14, 49, 50], [48, 51, 52], [13, 15, 19], [11, 12, 13], [15, 16, 19], [34, 36, 37], [21, 48, 49, 52], [19, 20, 21, 53], [31, 32, 38, 39], [9, 10, 11, 12, 16], [19, 20, 21, 49, 50], [28, 29, 30, 31, 32], [23, 25, 42, 46, 53], [23, 25, 42, 46, 47], [26, 27, 28, 29, 30, 53], [28, 29, 30, 36, 37, 38, 39, 40, 43], [26, 27, 28, 29, 30, 36, 37, 38, 39], [26, 27, 28, 29, 30, 40, 41, 43, 44, 45]]
# SNP:[[8, 10], [9, 54], [11, 12, 13], [48, 51, 52], [14, 49, 50], [15, 16, 19], [20, 21, 47], [31, 32, 34], [23, 25, 42, 46, 53], [26, 27, 28, 29, 30, 40, 41, 43, 44, 45]]

world1 = [[47, 48], [37, 39], [24, 46], [48, 54], [15, 18], [30, 37], [38, 40], [20, 21, 22], [9, 11, 54],
         [32, 34, 36], [13, 14, 16, 19],[8, 10, 11, 13], [8, 10, 52, 53], [11, 13, 49, 50, 51],
         [30, 34, 36, 41, 43], [9, 12, 14, 52, 53], [49, 50, 51, 52, 53], [26, 27, 28, 30, 41, 43],
         [24, 26, 27, 28, 30, 38], [26, 27, 28, 30, 32, 34], [12, 13, 14, 48, 49, 50, 51],
         [18, 19, 24, 26, 27, 28, 30], [21, 22, 24, 26, 27, 28, 30, 39]]
selection1 = [[15, 18], [24, 46], [37, 39], [47, 48], [38, 40], [9, 11, 54], [32, 34, 36], [20, 21, 22], [13, 14, 16, 19], [49, 50, 51, 52, 53], [26, 27, 28, 30, 41, 43]]

world2 = [[18, 19], [47, 48], [8, 10, 11, 13], [8, 9, 10, 11, 52, 53, 54],
          [9, 14, 15, 16, 52, 53, 54], [9, 12, 14, 15, 18, 52, 53], [9, 12, 14, 48, 49, 50, 51, 52, 53, 54]]

class TestCompareMaxCover(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_compare1(self):
        #
        input = [[34, 36, 37], [48, 51, 52], [31, 32, 34], [31, 32, 38, 39], [21, 48, 49, 52], [28, 29, 30, 31, 32], [9, 26, 27, 28, 29, 30, 53, 54], [26, 27, 28, 29, 30, 36, 37, 38, 39], [28, 29, 30, 36, 37, 38, 39, 40, 43], [26, 27, 28, 29, 30, 40, 41, 43, 44, 45]]
        m = GreedyMaxCover()
        result1 = m.solve(input)
        #print MaxCover.length_of_total_elements(result)
        #print result # 15
        #self.assertTrue(MaxCover.length_of_total_elements(result) == 34)

        m = BrutalForceMaxCover()
        result2 = m.solve_list_input(input)
        #print MaxCover.length_of_total_elements(result)
        #print result2
        #self.assertTrue(MaxCover.length_of_total_elements(result) == 34)

        self.assertEqual(result1, result2)

    def test_compare2(self):
        m = GreedyMaxCover()
        result1 = m.solve(data1)
        print MaxCover.length_of_total_elements(data1)
        print MaxCover.length_of_total_elements(result1)
        #self.assertTrue(MaxCover.length_of_total_elements(result) == 34)

        # m = BrutalForceMaxCover()
        # result2 = m.run_list_input(data1)
        # result1 == result2
        #self.assertTrue(MaxCover.length_of_total_elements(result) == 34)

if __name__ == "__main__":
    unittest.main(verbosity=2)