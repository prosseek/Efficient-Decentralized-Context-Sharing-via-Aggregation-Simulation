import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from test_maxcover import *
from context_aggregator.greedy_maxcover import GreedyMaxCover

world2 = [[18, 19], [47, 48], [8, 10, 11, 13], [8, 9, 10, 11, 52, 53, 54],
          [9, 14, 15, 16, 52, 53, 54], [9, 12, 14, 15, 18, 52, 53], [9, 12, 14, 48, 49, 50, 51, 52, 53, 54]]

class TestGreedyMaxcover(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_greedy_maxcover_from_world1(self):
        m = GreedyMaxCover()
        result = m.solve(world1)
        self.assertTrue(MaxCover.length_of_total_elements(result) == 34)

    def test_greedy_maxcover_from_world2(self):
        m = GreedyMaxCover()
        result = m.solve(world2)
        print MaxCover.length_of_total_elements(result)
        #self.assertTrue(MaxCover.length_of_total_elements(result) == 34)

if __name__ == "__main__":
    unittest.main(verbosity=2)