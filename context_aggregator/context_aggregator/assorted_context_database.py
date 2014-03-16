"""filtered context database

"""
import copy
from utils import *

from disaggregator import Disaggregator
from maxcover import MaxCover
from context.context import Context

import gc

class AssortedContextDatabase(object):
    """database class"""

    class Container(object):
        def __init__(self):
            self.singles = set()
            self.primes = set()
            self.non_primes = set()
            self.selected_non_primes = set()

    def __init__(self):
        self.reset()

    def reset(self):
        self.timestamp = {}

    def set(self, singles, primes, non_primes, selected_non_primes, timestamp=0):
        """

        >>> f = AssortedContextDatabase()
        >>> s = set([Context(value=1.0, cohorts=[0])])
        >>> p = set([Context(value=2.0, cohorts=[1,2,3])])
        >>> np = set([Context(value=3.0, cohorts=[4,5]), Context(value=5.0, cohorts=[5,6,7])])
        >>> snp = set([Context(value=5.0, cohorts=[5,6,7])])
        >>> f.set(s, p, np, snp)
        >>> compare_contexts_and_cohorts(f.get_singles(), [[0]])
        True
        >>> compare_contexts_and_cohorts(f.get_primes(), [[1,2,3]])
        True
        >>> compare_contexts_and_cohorts(f.get_non_primes(), [[4,5], [5,6,7]])
        True
        >>> compare_contexts_and_cohorts(f.get_selected_non_primes(), [[5,6,7]])
        True
        """
        if timestamp not in self.timestamp:
            self.timestamp[timestamp] = AssortedContextDatabase.Container()
        self.timestamp[timestamp].singles = singles
        self.timestamp[timestamp].primes = primes
        self.timestamp[timestamp].non_primes = non_primes
        self.timestamp[timestamp].selected_non_primes = selected_non_primes

    def get_singles(self, timestamp=0):
        c = self.timestamp[timestamp]
        return c.singles

    def get_primes(self, timestamp=0):
        c = self.timestamp[timestamp]
        return c.primes

    def get_non_primes(self, timestamp=0):
        c = self.timestamp[timestamp]
        return c.non_primes

    def get_selected_non_primes(self, timestamp=0):
        c = self.timestamp[timestamp]
        return c.selected_non_primes

if __name__ == "__main__":
    import doctest
    doctest.testmod()

