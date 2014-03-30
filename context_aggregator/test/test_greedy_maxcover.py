import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from test_maxcover import *
from context_aggregator.greedy_maxcover import GreedyMaxCover

class TestGreedyMaxcover(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_greedy_maxcover(self):
        m = GreedyMaxCover()
        result = m.solve(world1)
        self.assertTrue(MaxCover.length_of_total_elements(result) == 34)

if __name__ == "__main__":
    unittest.main(verbosity=2)