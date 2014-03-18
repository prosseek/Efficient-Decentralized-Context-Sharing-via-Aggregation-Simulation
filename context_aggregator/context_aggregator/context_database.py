"""context database

TODO: timestamp processing is missing
"""

from context.context import Context
from utils import *

class ContextDatabase(object):

    class Container(object):
        def __init__(self):
            self.singles = set()
            self.aggregates = set()

        # def append_singles(self, singles):
        #     self.singles = self.singles.union(singles)
        #
        # def append_aggregates(self, aggregates):
        #     self.aggregates = self.aggregates.union(aggregates)

    """database class"""

    def __init__(self):
        self.timestamp = {}

    def reset(self):

        self.singles = None
        self.aggregates = None

    def set(self, singles, aggregates, timestamp=0):
        """

        >>> cd = ContextDatabase()
        >>> s = set([Context(value=1.0, cohorts=[0])])
        >>> a = set([Context(value=2.0, cohorts=[1,2])])
        >>> cd.set(s, a)
        >>> same(cd.get_aggregates(), [[],[1,2]])
        True
        >>> same(cd.get_singles(), [[0],[]])
        True
        """
        if timestamp not in self.timestamp:
            self.timestamp[timestamp] = ContextDatabase.Container()
        self.timestamp[timestamp].singles = singles
        self.timestamp[timestamp].aggregates = aggregates

    def get_singles(self, timestamp=0):
        return self.timestamp[timestamp].singles

    def get_aggregates(self, timestamp=0):
        return self.timestamp[timestamp].aggregates

if __name__ == "__main__":
    import doctest
    doctest.testmod()


