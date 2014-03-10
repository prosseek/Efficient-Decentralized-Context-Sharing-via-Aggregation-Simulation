r"""Module Context -- the representation of contexts in Grapevine middleware
"""

import sys
import os

from .utils import *

class Context(object):
    r"""Context is a tuple of (value, cohorts, time_stamp, hop_count (Tau))
    """
    def __init__(self, value = None, cohorts = None, time_stamp = None, hop_count = 0):
        r"""Context constructor.
        
        All the parameters can be None or 0. 
        This is OK, because we can only take care of the single and aggregated contexts.

        When value is not None, cohorts should **not** be None
        
        >>> c = Context()
        >>> assert c.value is None and c.cohorts is None
        >>> a = Context(value=1.0, cohorts=set([0,1,2]))
        >>> a.cohorts
        bytearray(b'\x07')
        >>> a = Context(value=1.0, cohorts=set([1, 8, 16]))
        >>> a.cohorts
        bytearray(b'\x02\x01\x01')
        >>> bytearray2long(a.cohorts)
        65794
        """
        self.value = value
        if value is not None:
            assert cohorts is not None, "value %4.2f, cohorts %s" % (value, cohorts)
            cohorts = cohort_type_as_bytearray(cohorts)

        self.cohorts = cohorts
        self.time_stamp = time_stamp
        self.cohorts = cohorts
        self.hop_count = hop_count
        
    def __eq__(self, other):
        """Checks if two contexts are the same

        >>> c1 = Context(1, cohorts=set([0]))
        >>> c2 = Context(1, cohorts=set([0]))
        >>> assert c1 == c2
        """
        if other is None: return False
        if id(self) == id(other): return True
        if self.value == other.value and \
           self.cohorts == other.cohorts and \
           self.time_stamp == other.time_stamp and \
           self.hop_count == other.hop_count: 
            return True
        return False
        
    def __ne__(self, other):
        """
        >>> c1 = Context(1, cohorts=set([0]))
        >>> c2 = Context(1, cohorts=set([1]))
        >>> assert c1 != c2
        """
        return not self.__eq__(other)
        
    def __str__(self):
        """returns the string format of a string

        >>> print Context(value=1, cohorts=7)
        v(1.00):c(set([0, 1, 2]))
        """
        if self.cohorts is not None:
            cohorts = bytearray2set(self.cohorts)
        else:
            cohorts = ""

        result = "v(%4.2f):c(%s)" % (self.value, cohorts) # , self.value())
        return result

    def __add__(self, other):
        """context addition: it works only when the two contexts have no shared cohorts

        >>> a = Context(value=1.0, cohorts=set([0]))
        >>> b = Context(value=2.0, cohorts=set([1]))

        """
        pass

if __name__ == "__main__": # and __package__ is None:
    import doctest
    doctest.testmod()

    #     
    # def __len__(self):
    #     if cohorts is None: return 0
    #     
    #     
    # def getIdSet(self):
    #     return set([self.getId()])
    #     
    # def getIds(self):
    #     return self.getIdSet()
    #     
    # def sameWithoutId(self, other):
    #     if other is None: return False
    #     if self.v == other.v and \
    #        self.hopcount == other.hopcount and \
    #        self.timeStamp == other.timeStamp:
    #        return True
    #     return False
    #     
    # def checkTypeAndSet(self, v):
    #     if type(v) is Value:
    #         self.v = v
    #     else:
    #         self.v = Value(v)
    # 
    # def setValue(self, v):
    #     self.checkTypeAndSet(v)
    #     
    # def getValue(self):
    #     return self.v
    #     
    # def value(self):
    #     return self.v.getValue()
    #     
    # def increaseHopcount(self):
    #     self.hopcount += 1
    # 
    # def decreaseHopcount(self):
    #     self.hopcount -= 1;
    #     
    # def setHopcount(self, hopcount):
    #     self.hopcount = hopcount
    #     
    # def getHopcount(self):
    #     return self.hopcount
    #     
    # def getId(self):
    #     return self.id
    # 
    # def setId(self, id):
    #     self.id = id
    
