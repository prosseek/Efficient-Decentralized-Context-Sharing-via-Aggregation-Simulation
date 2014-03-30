import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.context_aggregator import ContextAggregator
from context.context import *
from utils import *
from context_aggregator.utils_same import *

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

class TestDataflow(unittest.TestCase):
    def setUp(self):
        # The input parameter should be host
        pass

    def test_run1(self):
        """Only [4,5] is prime
        All the others are singles
        """
        d = ContextAggregator()
        d.receive(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        d.receive(2, set([Context(value=2.0, cohorts=[0])]))
        d.set_database(set([Context(value=1.0, cohorts=[0,1,2,3,4,5]), Context(value=2.0, cohorts=[1])]), set([Context(value=1.0, cohorts=[2,3])]))
        d.run_dataflow()
        self.assertTrue(same(d.get_singles(), [[0,1,2,3],[]]))
        self.assertTrue(same(d.get_primes(), [[],[4,5]]))

    def test_run2(self):
        """Test case the same as doctest"""
        d = ContextAggregator(config={"propagation_mode": ContextAggregator.AGGREGATION_MODE, "max_tau": 1})
        #.initialize() # Always execute initialize before newly receive data
        # Emulating receive data from neighbors
        d.receive(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        d.receive(2, set([Context(value=2.0, cohorts=[0])]))
        d.receive(3, set([Context(value=3.0, cohorts=[1])]))
        d.receive(4, set([Context(value=7.0, cohorts=[9], hopcount=Context.SPECIAL_CONTEXT)]))
        # Emulating accumulated contexts
        context_db = set([Context(value=1.0, cohorts=[2,4,5,3]),Context(value=1.0, cohorts=[5,6]),Context(value=7.0, cohorts=[7,8])])
        d.set_database(singles=set([]), aggregates=context_db, timestamp=10)
        d.run_dataflow(timestamp=10)
        # Emulating newly found singles and aggregates from database
        self.assertTrue(same(d.get_database_singles(timestamp=10), [[0,1,2,9],[]]))
        self.assertTrue(same(d.get_database_aggregates(timestamp=10),[[7,8],[3,4,5],[6,5]]))
        # Emulating the disaggregation process
        self.assertTrue(same(d.get_singles(timestamp=10), [[0,1,2,9],[]]))
        self.assertTrue(same(d.get_primes(timestamp=10), [[],[7,8]]))
        self.assertTrue(same(d.get_non_primes(timestamp=10), [[3,4,5], [5,6]]))
        self.assertTrue(same(contexts_to_standard(d.get_selected_non_primes(timestamp=10)), [[],[3,4,5]]))
        self.assertTrue(d.get_new_aggregate().get_cohorts_as_set() == set([0,1,2,3,4,5,7,8,9]))
        self.assertTrue(same(d.get_filtered_singles(), [[0,1,9],[]]))

    def test_run3(self):
        """Doctest case with propage recovered singles"""
        d = ContextAggregator(config={"propagation_mode": ContextAggregator.AGGREGATION_MODE, "max_tau": 1, "propagate_recovered_singles": True})
        #d.initialize() # Always execute initialize before newly receive data
        # Emulating receive data from neighbors
        d.receive(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        d.receive(2, set([Context(value=2.0, cohorts=[0])]))
        d.receive(3, set([Context(value=3.0, cohorts=[1])]))
        d.receive(4, set([Context(value=7.0, cohorts=[9], hopcount=Context.SPECIAL_CONTEXT)]))
        # Emulating accumulated contexts
        context_db = set([Context(value=1.0, cohorts=[2,4,5,3]),Context(value=1.0, cohorts=[5,6]),Context(value=7.0, cohorts=[7,8])])
        d.set_database(singles=set([]), aggregates=context_db, timestamp=10)
        d.run_dataflow(timestamp=10)
        # Emulating newly found singles and aggregates from database
        self.assertTrue(same(d.get_database_singles(timestamp=10), [[0,1,2,9],[]]))
        self.assertTrue(same(d.get_database_aggregates(timestamp=10),[[7,8],[3,4,5],[6,5]]))
        # Emulating the disaggregation process
        self.assertTrue(same(d.get_singles(timestamp=10), [[0,1,2,9],[]]))
        self.assertTrue(same(d.get_primes(timestamp=10), [[7,8]]))
        self.assertTrue(same(d.get_non_primes(timestamp=10), [[3,4,5], [5,6]]))
        self.assertTrue(same(d.get_selected_non_primes(timestamp=10), [[3,4,5]]))
        self.assertTrue(d.get_new_aggregate().get_cohorts_as_set() == set([0,1,2,3,4,5,7,8,9]))
        self.assertTrue(same(d.get_filtered_singles(), [[0,1,2,9],[]]))

    def test_run4(self):
        """Doctest case with propage recovered singles, and propage with max_tau == 0 """
        d = ContextAggregator(config={"propagation_mode": ContextAggregator.AGGREGATION_MODE, "max_tau": 0, "propagate_recovered_singles": True})
        #d.initialize() # Always execute initialize before newly receive data
        # Emulating receive data from neighbors
        d.receive(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        d.receive(2, set([Context(value=2.0, cohorts=[0])]))
        d.receive(3, set([Context(value=3.0, cohorts=[1])]))
        d.receive(4, set([Context(value=7.0, cohorts=[9], hopcount=Context.SPECIAL_CONTEXT)]))
        # Emulating accumulated contexts
        context_db = set([Context(value=1.0, cohorts=[2,4,5,3]),Context(value=1.0, cohorts=[5,6]),Context(value=7.0, cohorts=[7,8])])
        d.set_database(singles=set([]), aggregates=context_db, timestamp=10)
        d.run_dataflow(timestamp=10)
        # Emulating newly found singles and aggregates from database
        self.assertTrue(same(d.get_database_singles(timestamp=10), [[0,1,2,9],[]]))
        self.assertTrue(same(d.get_database_aggregates(timestamp=10),[[7,8],[3,4,5],[6,5]]))
        # Emulating the disaggregation process
        self.assertTrue(same(d.get_singles(timestamp=10), [[0,1,2,9],[]]))
        self.assertTrue(same(d.get_primes(timestamp=10), [[],[7,8]]))
        self.assertTrue(same(d.get_non_primes(timestamp=10), [[3,4,5], [5,6]]))
        self.assertTrue(same(contexts_to_standard(d.get_selected_non_primes(timestamp=10)), [[],[3,4,5]]))
        self.assertTrue(d.get_new_aggregate().get_cohorts_as_set() == set([0,1,2,3,4,5,7,8,9]))
        self.assertTrue(same(d.get_filtered_singles(), [[2,9],[]]))

    def test_run5(self):
        """Doctest case with propage recovered singles, and propage with max_tau == 0 """
        d = ContextAggregator(config={"propagation_mode": ContextAggregator.AGGREGATION_MODE, "max_tau": 0, "propagate_recovered_singles": False})
        #d.initialize() # Always execute initialize before newly receive data
        # Emulating receive data from neighbors
        d.receive(1, set([Context(value=1.0, cohorts=[0,1,2])]))
        d.receive(2, set([Context(value=2.0, cohorts=[0])]))
        d.receive(3, set([Context(value=3.0, cohorts=[1])]))
        d.receive(4, set([Context(value=7.0, cohorts=[9], hopcount=Context.SPECIAL_CONTEXT)]))
        # Emulating accumulated contexts
        context_db = set([Context(value=1.0, cohorts=[2,4,5,3]),Context(value=1.0, cohorts=[5,6]),Context(value=7.0, cohorts=[7,8])])
        d.set_database(singles=set([]), aggregates=context_db, timestamp=10)
        d.run_dataflow(timestamp=10)
        # Emulating newly found singles and aggregates from database
        self.assertTrue(same(d.get_database_singles(timestamp=10), [[0,1,2,9],[]]))
        self.assertTrue(same(d.get_database_aggregates(timestamp=10),[[7,8],[3,4,5],[6,5]]))
        # Emulating the disaggregation process
        self.assertTrue(same(d.get_singles(timestamp=10), [[0,1,2,9],[]]))
        self.assertTrue(same(d.get_primes(timestamp=10), [[],[7,8]]))
        self.assertTrue(same(d.get_non_primes(timestamp=10), [[3,4,5], [5,6]]))
        self.assertTrue(same(contexts_to_standard(d.get_selected_non_primes(timestamp=10)), [[],[3,4,5]]))
        self.assertTrue(d.get_new_aggregate().get_cohorts_as_set() == set([0,1,2,3,4,5,7,8,9]))
        self.assertTrue(same(d.get_filtered_singles(), [[9],[]]))

if __name__ == "__main__":
    unittest.main(verbosity=2)