"""filtered context database

"""
import copy
from utils import *

from disaggregator import Disaggregator
from maxcover import MaxCover

import gc

class FilteredContextDatabase(object):
    """database class"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.singles = set()
        self.primes = set()
        self.non_primes = set()
        self.selected_non_primes = set()

    def update(self, singles, primes, non_primes, selected_non_primes):
        self.singles = singles
        self.primes = primes
        self.non_primes = non_primes
        self.selected_non_primes = selected_non_primes

    def get_singles(self):
        return self.singles

    def get_primes(self):
        return self.primes

    def get_non_primes(self):
        return self.non_primes

    def get_selected_non_primes(self):
        return self.selected_non_primes

if __name__ == "__main__":
    import doctest
    doctest.testmod()


