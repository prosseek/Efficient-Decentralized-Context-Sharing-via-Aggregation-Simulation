import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.context_history import ContextHistory
from context.context import Context
from utils import *
from context_aggregator.utils import *

class TestContextHistory(unittest.TestCase):

    def setUp(self):
        pass

    def test_calculate_output_for_aggregates1(self):
        """
        When new_aggregate exists, but there is no input or whatever, ther output should be {}, because
        it doesn't have neighbor information.
        """
        h = ContextHistory()
        new_aggregate = Context(value=1.0, cohorts=[1,2,3])
        self.assertTrue(h.calculate_output_for_aggregates(new_aggregate, {}) == {})
        new_aggregate = Context(value=1.0, cohorts=[1,2,3])
        self.assertTrue(h.calculate_output_for_aggregates(new_aggregate, {1:set([Context(value=1.0, cohorts=[1,2,3])])}) == {})

    def test_calculate_output_for_aggregates2(self):
        """
        When the new info is [1,2], and when the same info is received from node 1 but not 2,
        the information is sent only to node 2
        """
        h = ContextHistory()
        new_aggregate = Context(value=1.0, cohorts=[1,2])
        r = h.calculate_output_for_aggregates(new_aggregate, {1:set([Context(value=1.0, cohorts=[1,2])]), 2:set([Context(value=1.0, cohorts=[2,3])])})
        self.assertTrue(1 not in r)
        self.assertTrue(r[2].get_cohorts_as_set() == set([1,2]))

    def test_calculate_output_for_aggregates3(self):
        """
        When the new info is [1,2,3], but it only previously sent [1,2] to 1 and 2 before
        the information is sent to 2 and 3
        """
        h = ContextHistory()
        new_aggregate = Context(value=1.0, cohorts=[1,2,3])
        h.set_sent_aggregate(1, [1,2])
        h.set_sent_aggregate(2, [1,2])
        r = h.calculate_output_for_aggregates(new_aggregate, {})
        self.assertTrue(r[1].get_cohorts_as_set() == set([1,2,3]))
        self.assertTrue(r[2].get_cohorts_as_set() == set([1,2,3]))

    def test_calculate_output_for_singles1(self):
        """
        When the new info is [1,2,3], but it only previously sent [1,2] to 1 and 2 before
        the information is sent to 2 and 3
        """
        h = ContextHistory()
        new_singles = set([Context(value=1.0, cohorts=[3]), Context(value=1.0, cohorts=[4])])
        h.set_sent_singles(1, [1,2])
        h.set_sent_singles(2, [1,2])
        r = h.calculate_output_for_singles(new_singles, {})
        self.assertTrue(same(r[1], [[3,4],[]]))
        self.assertTrue(same(r[2], [[3,4],[]]))

    def test_calculate_output_for_singles2(self):
        """
        When the new info is [1,2,3], but it only previously sent [1,2] to 1 and 2 before
        the information is sent to 2 and 3
        """
        h = ContextHistory()
        new_singles = set([Context(value=1.0, cohorts=[3]), Context(value=1.0, cohorts=[4])])
        h.set_sent_singles(1, [1,2])
        h.set_sent_singles(2, [1,2])
        # 3 is already received, so only send the 4
        r = h.calculate_output_for_singles(new_singles, {1:set([Context(value=1.0, cohorts=[3])]), 2:set([Context(value=1.0, cohorts=[3])])})
        self.assertTrue(same(r[1], [[4],[]]))
        self.assertTrue(same(r[2], [[4],[]]))

    def test_calculate_output_for_singles2(self):
        """
        When the new info is [1,2,3], but it only previously sent [1,2] to 1 and 2 before
        the information is sent to 2 and 3
        """
        h = ContextHistory()
        new_singles = set([Context(value=1.0, cohorts=[3]), Context(value=1.0, cohorts=[4])])
        h.set_sent_singles(1, [1,4])
        h.set_sent_singles(2, [1,4])
        # 3 is already received, so only send the 4
        r = h.calculate_output_for_singles(new_singles, {1:set([Context(value=1.0, cohorts=[3])]), 2:set([Context(value=1.0, cohorts=[3])])})
        self.assertTrue(1 not in r)
        self.assertTrue(2 not in r)


    def test_calculate_output1(self):
        h = ContextHistory()
        h.sent(1, [[1],[2],[3,4]])
        contexts =set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=2.0, cohorts=[3]), Context(value=1.0, cohorts=[4]), \
                       Context(value=3.0, cohorts=[5,6,7,8])])
        inputs={1:set([Context(value=1.0, cohorts=[3])])}
        r = h.calculate_output(contexts=contexts, inputs=inputs)
        self.assertTrue(same(r[1], [[4],[5,6,7,8]]))

    def test_calculate_output2(self):
        h = ContextHistory()
        h.sent(1, [[1],[2],[3,4]])
        contexts =set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=2.0, cohorts=[3]), Context(value=1.0, cohorts=[4]), \
                       Context(value=3.0, cohorts=[5,6,7,8])])
        inputs={2:set([Context(value=1.0, cohorts=[2])])}
        r = h.calculate_output(contexts=contexts, inputs=inputs)
        self.assertTrue(same(r[1], [[3,4],[5,6,7,8]]))
        self.assertTrue(same(r[2], [[1,3,4],[5,6,7,8]]))

if __name__ == "__main__":
    unittest.main(verbosity=2)