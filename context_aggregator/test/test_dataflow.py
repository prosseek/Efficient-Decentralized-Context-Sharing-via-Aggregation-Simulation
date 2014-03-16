import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.dataflow import DataFlow
from context.context import *
from utils import *
from context_aggregator.utils import *

c0 = Context(value=0.0, cohorts=[0])
c1 = Context(value=1.0, cohorts=[1])
c2 = Context(value=2.0, cohorts=[2])
c3 = Context(value=3.0, cohorts=[3])
c4 = Context(value=4.0, cohorts=[4])
c5 = Context(value=5.0, cohorts=[5])

c7 = Context(value=7.0, cohorts=[7])
c8 = Context(value=8.0, cohorts=[8])

g01 = Context(value=avg([c0, c1]), cohorts=[0,1])
g012 = Context(value=avg([c0, c1, c2]), cohorts=[0,1,2])
g345 = Context(value=avg([c3, c4, c5]), cohorts=[3,4,5])
g01 = Context(value=avg([c0, c1]), cohorts=[0,1])
g34 = Context(value=avg([c3, c4]), cohorts=[3,4])
g3478 = Context(value=avg([c3, c4, c7, c8]), cohorts=[3,4,7,8])

class TestDataFlow(unittest.TestCase):
    def setUp(self):
        # The input parameter should be host
        pass

    def test_run1(self):
        """Only [4,5] is prime
        All the others are singles
        """
        d = DataFlow()
        d.receive_data(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        d.receive_data(2, set([Context(value=2.0, cohorts=[0])]))
        d.set_database(set([Context(value=1.0, cohorts=[0,1,2,3,4,5]), Context(value=2.0, cohorts=[1])]), set([Context(value=1.0, cohorts=[2,3])]))
        d.run()
        self.assertTrue(compare_contexts_and_cohorts(d.get_singles(), [[0],[1],[2],[3]]))
        self.assertTrue(compare_contexts_and_cohorts(d.get_primes(), [[4,5]]))

if __name__ == "__main__":
    unittest.main(verbosity=2)