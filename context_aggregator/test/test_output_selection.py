import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.context_history import ContextHistory
from context_aggregator.output_selector import OutputSelector
from context_aggregator.utils_same import *

class TestOutputSelection(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_when_neighbor_is_None(self):
        inputs = {0:[[1,2,3],[3,4,5]], 1:[[1,2],[3,4,5,6]]}
        input = [[4,5],[3,4,5,6,7]]
        h =ContextHistory()
        h.set_history(1, input)
        h.set_history(3, input)
        new_info = [[1,2,3,4,5],[3,4,5,6,7,8]]
        o = OutputSelector(inputs=inputs, context_history=h, new_info=new_info)
        r = o.run()
        self.assertTrue(same(r, {0: [[4, 5], [3, 4, 5, 6, 7, 8]], 3: [[1, 2, 3], [3, 4, 5, 6, 7, 8]], 1: [[3], [3, 4, 5, 6, 7, 8]]}))


if __name__ == "__main__":
    unittest.main(verbosity=2)