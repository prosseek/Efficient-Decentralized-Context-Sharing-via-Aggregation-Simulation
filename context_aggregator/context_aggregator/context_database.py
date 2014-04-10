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
                return "(ERRROR)"

    def reset(self):

        self.singles = {}
        self.aggregates = {}

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
        assert type(singles) is set
        assert type(aggregates) is set

        if timestamp not in self.timestamp:
           self.timestamp[timestamp] = ContextDatabase.Container()

        self.timestamp[timestamp].singles =  singles

        #for s in singles:
        #   self.timestamp[timestamp].singles.add(s)

        self.timestamp[timestamp].aggregates =  aggregates

        # for a in aggregates:
        #    self.timestamp[timestamp].aggregates.add(a)

    def get_singles(self, timestamp=0):
        """When timestamp is negative number, it returns the newest timestamp
        """
        if timestamp < 0: timestamp = self.get_last_timestamp()
        return self.timestamp[timestamp].singles

    def get_single_from_id(self, id, timestamp=0):
        """
        >>> cd = ContextDatabase()
        >>> s = set([Context(value=1.0, cohorts=[3])])
        >>> a = set([Context(value=2.0, cohorts=[1,2])])
        >>> cd.set(s, a)
        >>> cd.get_single_from_id(3).get_id() == 3
        True
        """
        singles = self.get_singles(timestamp)
        for s in singles:
            if s.get_id() == id: return s
        return None

    def get_aggregates(self, timestamp=0):
        """
        >>> cd = ContextDatabase()
        >>> s ={Context(value=1.0, cohorts=[0])}
        >>> a ={Context(value=2.0, cohorts=[1,2])}
        >>> cd.set(s, a, 0)
        >>> r = cd.get_aggregates()
        >>> len(r) == 1 and type(r) is set
        True
        >>> cd = ContextDatabase()
        >>> cd.set([],[],0)
        >>> cd.get_aggregates()
        """
        if timestamp < 0: timestamp = self.get_last_timestamp()
        return self.timestamp[timestamp].aggregates

    def get_last_timestamp(self):
        """
        >>> last_timestamp = 123
        >>> cd = ContextDatabase()
        >>> s ={Context(value=1.0, cohorts=[0])}
        >>> a ={Context(value=2.0, cohorts=[1,2])}
        >>> cd.set(s, a, 0)
        >>> s ={Context(value=1.0, cohorts=[1])}
        >>> a ={Context(value=2.0, cohorts=[1,2,3])}
        >>> cd.set(s, a, last_timestamp)
        >>> cd.get_last_timestamp() == last_timestamp
        True
        """
        # timestamp is negative, so get the newest timestamp
        return sorted(self.timestamp.keys(), reverse=True)[0]

    def update_context_hopcount(self, id, value):
        """
        >>> cd = ContextDatabase()
        >>> s ={Context(value=1.0, cohorts=[3])}
        >>> a ={Context(value=2.0, cohorts=[1,2])}
        >>> cd.set(s, a, 0)
        >>> cd.update_context_hopcount(3, Context.SPECIAL_CONTEXT)
        >>> cd.get_single_from_id(3).hopcount == Context.SPECIAL_CONTEXT
        True
        """
        single = self.get_single_from_id(id)
        if single is not None:
            single.hopcount = value

if __name__ == "__main__":
    import doctest
    doctest.testmod()


