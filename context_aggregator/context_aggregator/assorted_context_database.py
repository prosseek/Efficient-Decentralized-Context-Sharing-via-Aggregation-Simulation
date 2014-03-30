"""filtered context database

"""
import copy
from utils_same import *

from disaggregator import Disaggregator
#from brutal_force_maxcover import MaxCover
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

    def to_string(self, timestamp):
        #assert timestamp in self.timestamp
        if timestamp not in self.timestamp:
            return "P:[], NP:[], SNP:[] (before initialization)"
        assorted = self.timestamp[timestamp]
        primes = aggregated_contexts_to_list_of_standard(assorted.primes)
        non_primes = aggregated_contexts_to_list_of_standard(assorted.non_primes)
        selected_non_primes = aggregated_contexts_to_list_of_standard(assorted.selected_non_primes)
        return "P:%s, NP:%s, SNP:%s" % (primes, non_primes, selected_non_primes)


    def set(self, singles, primes, non_primes, selected_non_primes, timestamp=0):
        """

        >>> f = AssortedContextDatabase()
        >>> s = set([Context(value=1.0, cohorts=[0])])
        >>> p = set([Context(value=2.0, cohorts=[1,2,3])])
        >>> np = set([Context(value=3.0, cohorts=[4,5]), Context(value=5.0, cohorts=[5,6,7])])
        >>> snp = set([Context(value=5.0, cohorts=[5,6,7])])
        >>> f.set(s, p, np, snp)
        >>> same(f.get_singles(), [[0],[]])
        True
        >>> same(f.get_primes(), [[],[1,2,3]])
        True
        >>> same(f.get_non_primes(), [[4,5], [5,6,7]])
        True
        >>> same(f.get_selected_non_primes(), [[],[5,6,7]])
        True
        """
        if timestamp not in self.timestamp:
            self.timestamp[timestamp] = AssortedContextDatabase.Container()
        self.timestamp[timestamp].singles = singles
        self.timestamp[timestamp].primes = primes
        self.timestamp[timestamp].non_primes = non_primes
        self.timestamp[timestamp].selected_non_primes = selected_non_primes

    def get_singles(self, timestamp=0):
        if timestamp in self.timestamp:
            c = self.timestamp[timestamp]
            return c.singles
        return set()

    def get_primes(self, timestamp=0):
        if timestamp in self.timestamp:
            c = self.timestamp[timestamp]
            return c.primes
        return set()

    def get_non_primes(self, timestamp=0):
        if timestamp in self.timestamp:
            c = self.timestamp[timestamp]
            return c.non_primes
        return set()

    def get_selected_non_primes(self, timestamp=0):
        if timestamp in self.timestamp:
            c = self.timestamp[timestamp]
            return c.selected_non_primes
        return set()

if __name__ == "__main__":
    import doctest
    doctest.testmod()


