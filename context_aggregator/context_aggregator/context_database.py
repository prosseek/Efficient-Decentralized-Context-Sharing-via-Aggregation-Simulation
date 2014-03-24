"""context database

TODO: timestamp processing is missing
"""

from context.context import Context
from utils_same import *
from utils_print import *

class ContextDatabase(object):
    """database class"""
    class Container(object):
        def __init__(self):
            self.singles = set()
            self.aggregates = set()

    def __init__(self):
        self.timestamp = {}

    def __str__(self):
        return self.to_string(timestamp=-1, display_mode=0) # print out the most recent one

    def to_string(self, timestamp=None, display_mode=0):
        """

        >>> cd = ContextDatabase()
        >>> s = set([Context(value=1.0, cohorts=[0])])
        >>> a = set([Context(value=2.0, cohorts=[1,2,5])])
        >>> cd.set(s, a, timestamp=0)
        >>> s = set([Context(value=1.0, cohorts=[1], hopcount=-2, timestamp=1)])
        >>> a = set([Context(value=2.0, cohorts=[1,3,4], timestamp=1)])
        >>> cd.set(s, a, timestamp=1)
        >>> print cd.to_string(timestamp=-1)
        1s:[(1.00,[1],-2,1)]
        1a:[(2.00,[1,3,4],0,1)]
        >>> print cd.to_string(timestamp=0)
        0s:[(1.00,[0],0,0)]
        0a:[(2.00,[1,2,5],0,0)]
        >>> print cd.to_string()
        0s:[(1.00,[0],0,0)]
        0a:[(2.00,[1,2,5],0,0)]
        1s:[(1.00,[1],-2,1)]
        1a:[(2.00,[1,3,4],0,1)]
        >>> print cd.to_string(timestamp=-1, display_mode=1)
        1s:[1:]
        1a:[1,3,4:2]
        >>> print cd.to_string(timestamp=0, display_mode=-1)
        0s:[0]
        0a:[1,2,5]
        """
        sorted_timestamp_keys = sorted(self.timestamp)
        if timestamp is None: # print all the time stamp
            result = ""
            for key in sorted_timestamp_keys:
                result += self.to_string(key, display_mode)
                result += "\n"
            return result[0:len(result)-1] # remove the last '\n'

        elif timestamp == -1:
            if len(sorted_timestamp_keys) >= 1:
                return self.to_string(sorted_timestamp_keys[-1], display_mode)
            else:
                return "()"
        else:
            try:
                c = self.timestamp[timestamp]
                result = container_to_string(c, display_mode=display_mode).split('\n')
                return str(timestamp) + "s:" + result[0] + "\n" + str(timestamp) + "a:" + result[1]

            except IndexError:
                return "()"

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


