import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.disaggregator import Disaggregator
from context.context import *
from utils import *

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

class TestDisaggregator(unittest.TestCase):
    def setUp(self):
        # The input parameter should be host
        pass

    def compare(self, contexts, lists):
        l1 = []
        for c in contexts:
            l1.append(sorted(list(c.get_cohorts_as_set())))
        l2 = []
        for i in lists:
            l2.append(sorted(i))

        return sorted(l1) == sorted(l2)

    def test_run1(self):
        """
        simple case with one single and group context
        """
        d = Disaggregator([c0, g012])
        singles, groups = d.run()
        self.assertTrue(len(singles) == 1)
        self.assertTrue(self.compare(singles, [[0]]))
        self.assertTrue(len(groups) == 1)
        self.assertTrue(self.compare(groups, [[1,2]]))

    def test_run2(self):
        """
        simple case with one single and group context
        """
        d = Disaggregator([c0, g012, g01])
        singles, groups = d.run()
        self.assertTrue(len(singles) == 3)
        self.assertTrue(self.compare(singles, [[0],[1],[2]]))
        self.assertTrue(len(groups) == 0)

    def test_run3(self):
        """
        simple case with one single and group context
        """
        d = Disaggregator([c0, g345])
        singles, groups = d.run()
        self.assertTrue(len(singles) == 1)
        self.assertTrue(self.compare(singles, [[0]]))
        self.assertTrue(len(groups) == 1)
        self.assertTrue(self.compare(groups, [[3,4,5]]))

    def test_run4(self):
        """
        simple case with one single and group context
        """
        d = Disaggregator([g01, g012, g345, g34])
        singles, groups = d.run()
        self.assertTrue(len(singles) == 2)
        self.assertTrue(self.compare(singles, [[2],[5]]))
        self.assertTrue(len(groups) == 2)
        self.assertTrue(self.compare(groups, [[0,1],[3,4]]))

        d = Disaggregator([c0,c1,c2,c3,c4,g012,g345,g01,g34])
        singles, groups = d.run()
        self.assertTrue(self.compare(singles, [[0],[1],[2],[3],[4],[5]]))
        self.assertTrue(self.compare(groups, []))

        d = Disaggregator([c0,c1,c2,c3,c4,g012,g345,g01,g34, g3478])
        singles, groups = d.run()
        self.assertTrue(self.compare(singles, [[0],[1],[2],[3],[4],[5]]))
        self.assertTrue(self.compare(groups, [[7,8]]))

    def test_run5(self):
        d = Disaggregator([c0,c1,g01,g012])
        singles, groups = d.run()
        self.assertTrue(self.compare(singles, [[0],[1],[2]]))
        self.assertTrue(self.compare(groups, []))

if __name__ == "__main__":
    unittest.main(verbosity=2)