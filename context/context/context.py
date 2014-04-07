r"""Module Context -- the representation of contexts in Grapevine middleware

Standard string format
-> v(1.00):c([1,2,3]):h(1):t(0)
Standard string format (simplified version)
-> (1.00,[1,2,3],1,0)
"""

import sys
import os
import copy
import zlib
#import platform

from utils import *

class Context(object):
    r"""Context is a tuple of (value, cohorts, timestamp, hopcount (Tau))
    
    hopcount ::
    
        positive integer: the number of hops from the source
        SENSED_CONTEXT : the single context newly generated from host
        AGGREGATED_CONTEXT : aggregated context
        RECOVERED_CONTEXT : recovered context from context disaggregation
        SPECIAL_CONTEXT : special single context that should be shared by every host

    Things to know
    ==============

    1. In the initializer(__init__), cohorts can be list or set. However, in inner structure,
       the data is transformed into set().
        
    """
    SENSED_CONTEXT = 0
    AGGREGATED_CONTEXT = -1
    RECOVERED_CONTEXT = -2
    SPECIAL_CONTEXT = -3
    
    def __init__(self, value = None, cohorts = None, timestamp = 0, hopcount = 0):
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
        self.id = None
        self.value = value
        if value is not None:
            assert cohorts is not None, "value %4.2f, cohorts %s" % (value, cohorts)
            # cohorts is transformed into a set
            # This makes the testing a little bit easier as you don't need to
            # use set([...]), but [...]
            cohorts = cohort_type_as_bytearray(cohorts)

        self.timestamp = timestamp
        self.cohorts = cohorts
        self.hopcount = hopcount

    def get_id(self):
        """This method uses cache to retrieve the id.
        The id for aggregated context is Context.AGGREGATED_CONTEXT

        >>> a = Context(value=0.0, cohorts=[4])
        >>> a.get_id() == 4
        True
        """
        if self.id is not None:
            return self.id

        if self.is_single():
            id = list(self.get_cohorts_as_set())[0]
        else:
            id = Context.AGGREGATED_CONTEXT
        self.id = id
        return self.id

        
    def __eq__(self, other):
        """Checks if two contexts are the same

        >>> c1 = Context(1, cohorts=set([0,3,4]), timestamp=1, hopcount=4)
        >>> c2 = Context(1, cohorts=set([0,3,4]), timestamp=1, hopcount=4)
        >>> c1 == c2
        True

        >>> c1 = Context(1, cohorts=set([0,3]), timestamp=1, hopcount=4)
        >>> c2 = Context(1, cohorts=set([0,3,4]), timestamp=1, hopcount=4)
        >>> c1 == c2
        False

        >>> c1 = Context(1, cohorts=set([0,3,4]), timestamp=1, hopcount=3)
        >>> c2 = Context(1, cohorts=set([0,3,4]), timestamp=1, hopcount=4)
        >>> c1 == c2
        False
        """
        if other is None: return False
        if id(self) == id(other): return True
        if self.value == other.value and \
           self.cohorts == other.cohorts and \
           self.timestamp == other.timestamp and \
           self.hopcount == other.hopcount: 
            return True
        return False

    def __str__(self):
        return self.to_string()

    def to_string(self, simple=False):
        """

        A context is represented as a tuple
        (value, [cohorts], timestamp, hopcount)

        >>> c = Context(value=1.0, cohorts=[1], timestamp=0, hopcount=1)
        >>> print c.to_string()
        v(1.00):c([1]):h(1):t(0)
        >>> c = Context(value=1.0, cohorts=[1,2,3], timestamp=0, hopcount=1)
        >>> print c.to_string()
        v(1.00):c([1,2,3]):h(1):t(0)
        >>> print c.to_string(simple=True)
        (1.00,[1,2,3],1,0)
        >>> c = Context(value=1.0, cohorts={1,10,19,2,20,21,29,3,30,31,39,4,40,49,5,50,51,52,53,54,6,7,8,9})
        >>> print c.to_string(simple=True)
        (1.00,[1,2,3,4,5,6,7,8,9,10,19,20,21,29,30,31,39,40,49,50,51,52,53,54],0,0)
        """
        if self.cohorts is None:
            cohorts = set([])
        else:
            cohorts = self.get_cohorts_as_set()

        sorted_cohorts = sorted(cohorts)
        sorted_cohorts = map(str,sorted_cohorts)
        cohorts_string = ",".join(sorted_cohorts)

        if simple:
            result = "(%4.2f,[%s],%d,%d)" % (self.value, cohorts_string, self.hopcount, self.timestamp)
        else:
            result = "v(%4.2f):c([%s]):h(%d):t(%d)" % (self.value, cohorts_string, self.hopcount, self.timestamp) # , self.value())
        return result


    def equiv(self, other, ignore_value=False):
        """Check if this context is equivalent to the other context
        Equivalence means the same value and same cohorts

        >>> c1 = Context(1, cohorts=set([0,3,4]), timestamp=1, hopcount=3)
        >>> c2 = Context(1, cohorts=set([0,3,4]), timestamp=1, hopcount=4)
        >>> c1.equiv(c2)
        True

        When ignore_value is True, compare only the cohorts
        >>> c1 = Context(4, cohorts=set([0,3,4]), timestamp=1, hopcount=3)
        >>> c2 = Context(1, cohorts=set([0,3,4]), timestamp=1, hopcount=4)
        >>> c1.equiv(c2, ignore_value=True)
        True
        """
        if other is None: return False
        if self.cohorts == other.cohorts:
            if not ignore_value:
                if self.value == other.value:
                    return True
                else:
                    return False
            else:
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
        v(1.00):c([0,1,2]):h(0):t(0)
        """
        return self.to_string(simple=False)

    def __add__(self, other):
        """context addition: it works only when the two contexts have no shared cohorts.
        When shared elements exist, None is returned

        >>> a = Context(value=1.0, cohorts=set([0]))
        >>> b = Context(value=2.0, cohorts=set([1]))
        >>> c = a + b
        >>> print(c)
        v(1.50):c([0,1]):h(-1):t(0)
        """
        r = add(self.cohorts, other.cohorts)
        # when cohorts share element, return will be returned
        if r is None: return None
        
        n1 = get_number_of_one_from_bytearray(self.cohorts)
        n2 = get_number_of_one_from_bytearray(other.cohorts)
            
        value = float(n1*self.value + n2*other.value)/(n1 + n2)
        hopcount = Context.AGGREGATED_CONTEXT
        return Context(value=value, cohorts=r, hopcount=hopcount)

    def __sub__(self, other):
        """context subtraction: it works only when a > b
        When containment relationship does not exist, None is returned

        >>> a = Context(value=1.0, cohorts=set([0,1,2,3]))
        >>> b = Context(value=2.0, cohorts=set([0]))
        >>> c = a - b
        >>> print(c)
        v(0.67):c([1,2,3]):h(-1):t(0)
        >>> c.is_single()
        False

        >>> a = Context(value=1.0, cohorts=set([0,1]))
        >>> b = Context(value=2.0, cohorts=set([0]))
        >>> c = a - b
        >>> print(c)
        v(0.00):c([1]):h(-2):t(0)
        >>> c.is_single()
        True

        When a is not a subset of b, None returns
        >>> a = Context(value=1.0, cohorts=set([0,1]))
        >>> b = Context(value=2.0, cohorts=set([1,2]))
        >>> c = a - b
        >>> print c
        None

        >>> a = Context(value=1.0, cohorts=set([0,1]))
        >>> b = Context(value=2.0, cohorts=set([1,0]))
        >>> c = a - b
        >>> print c
        None

        """
        r = sub(self.cohorts, other.cohorts)
        # when cohorts share element, None will return
        if r is None: return None

        # When the two cohorts are the same, None will return
        if r == set([]): return None

        n1 = get_number_of_one_from_bytearray(self.cohorts)
        n2 = get_number_of_one_from_bytearray(other.cohorts)

        number_of_elements = n1 - n2
        value = float(n1*self.value - n2*other.value)/number_of_elements

        if number_of_elements == 1:
            hopcount = Context.RECOVERED_CONTEXT
        else:
            hopcount = Context.AGGREGATED_CONTEXT

        assert self.timestamp == other.timestamp, "%s/timestamp self(%d) vs other(%d)" % (self, self.timestamp, other.timestamp)
        return Context(value=value, cohorts=r, hopcount=hopcount, timestamp=self.timestamp)

    def __len__(self):
        """
        length of a context means the number of elements in it

        >>> c = Context(value=1.0, cohorts=set([0,1,2,3,4,5]))
        >>> len(c)
        6
        >>> c = Context()
        >>> len(c)
        0
        """
        return get_number_of_one_from_bytearray(self.cohorts)

    def __gt__(self, other):
        """c1 > c2 means elements of c1 is a superset of c2

        >>> c1 = Context(value=1.0, cohorts=set([0,1,2,3,4,5]))
        >>> c2 = Context(value=1.0, cohorts=set([0,1,2,3,4]))
        >>> c3 = Context(value=1.0, cohorts=set([1,3,4,5,6]))
        >>> c1 > c2
        True
        >>> c1 > c3
        False
        >>> # You can't compare the contexts that doens't have cohorts
        >>> c0 = Context()
        >>> c0 > c1
        Traceback (most recent call last):
           ...
            assert value is not None
        AssertionError
        """
        c1 = bytearray2set(self.cohorts)
        c2 = bytearray2set(other.cohorts)

        # We don't expect the contexts doesn't have any elements
        assert c1 != set([]) and c2 != set([])

        return c2 - c1 == set([])

    def __lt__(self, other):
        """c1 > c2 means elements of c1 is a superset of c2

        >>> c1 = Context(value=1.0, cohorts=set([0,1,2,3,4,5]))
        >>> c2 = Context(value=1.0, cohorts=set([0,1,2,3,4]))
        >>> c3 = Context(value=1.0, cohorts=set([1,3,4,5,6]))
        >>> c2 < c1
        True
        >>> c3 < c1
        False
        >>> # You can't compare the contexts that doens't have cohorts
        >>> c0 = Context()
        >>> c0 < c1
        Traceback (most recent call last):
           ...
            assert value is not None
        AssertionError
        """
        c1 = bytearray2set(self.cohorts)
        c2 = bytearray2set(other.cohorts)

        # We don't expect the contexts doesn't have any elements
        assert c1 != set([]) and c2 != set([])

        return c1 - c2 == set([])
    #
    # Utilities
    #

    def is_single(self):
        """Check if this Context is single or not

        >>> c = Context(value=1.0, cohorts=set([0]))
        >>> c.is_single()
        True
        >>> c = Context(value=1.0, cohorts=set([0,1,2]))
        >>> c.is_single()
        False
        """
        return 1 == get_number_of_one_from_bytearray(self.cohorts)

    def get_cohorts_as_set(self):
        """
        >>> c = Context(value=1.0, cohorts=set([1,2,3]))
        >>> c.get_cohorts_as_set() == set([1,2,3])
        True
        """
        return bytearray2set(self.cohorts)

    def get_cohort_as_tuple(self):
        """
        Works only with single context

        >>> c = Context(value=1.0, cohorts=set([1]), hopcount=-3)
        >>> c.get_cohort_as_tuple() == (1,-3)
        True
        >>> c = Context(value=1.0, cohorts=set([1,3,4]), hopcount=-1)
        >>> c.get_cohort_as_tuple() is None
        True
        """
        if not self.is_single(): return None
        else:
            single = bytearray2set(self.cohorts)
            return (list(single)[0], self.hopcount)

    def get_cohorts_size_in_bytes(self):
        """Returns the number of bit widths of cohorts

        >>> c = Context(value=1.0, cohorts=set([1,2,3]))
        >>> c.get_cohorts_size_in_bytes()
        1
        >>> c = Context(value=1.0, cohorts=set([1023]))
        >>> c.get_cohorts_size_in_bytes()
        128
        """
        return len(self.cohorts)

    def get_maximum_cohorts(self):
        """Returns the number of bit widths of cohorts

        >>> c = Context(value=1.0, cohorts=set([1,2,3]))
        >>> c.get_maximum_cohorts()
        7
        >>> c = Context(value=1.0, cohorts=set([1023]))
        >>> c.get_maximum_cohorts() # 1023 -> 1024/8 bytes * 8 - 1
        1023
        >>> c = Context(value=1.0, cohorts=set([0, 1024]))
        >>> c.get_maximum_cohorts()
        1031
        """
        # length of cohorts are byte size
        # *8 to get bit size
        # -1 needed as 0 is the starting number
        return (len(self.cohorts)*8 - 1)

    def get_index(self):
        """Works only for single, returns the index of a single contex

        >>> c = Context(value=1.0, cohorts=set([1]))
        >>> c.get_index()
        1
        >>> c = Context(value=1.0, cohorts=set([7]))
        >>> c.get_index()
        7
        """

        if self.is_single(): return list(self.get_cohorts_as_set())[0]
        return None

    @staticmethod
    def increase_hop_count(context):
        """

        >>> c = Context(value=1.0, cohorts=[1,2,3], hopcount = -1)
        >>> # Increase hopcount has a meaning with single context
        >>> c2 = Context.increase_hop_count(c)
        >>> c2.hopcount == c.hopcount == -1
        True
        >>> c = Context(value=1.0, cohorts=[1], hopcount=5)
        >>> # Increase hopcount has a meaning with single context
        >>> c = Context.increase_hop_count(c)
        >>> c.hopcount == 5+1
        True
        >>> c = [Context(value=1.0, cohorts=[1], hopcount=0), Context(value=1.0, cohorts=[1], hopcount=1), \
            Context(value=1.0, cohorts=[1], hopcount=2), Context(value=1.0, cohorts=[9], hopcount=Context.SPECIAL_CONTEXT)]
        >>> # Increase hopcount has a meaning with single context
        >>> c = Context.increase_hop_count(c)
        >>> c[0].hopcount == 1 and c[1].hopcount == 2 and c[2].hopcount == 3 and c[3].hopcount == Context.SPECIAL_CONTEXT
        True
        """
        if type(context) is set:
            result = set()
            for c in context:
                result.add(Context.increase_hop_count(c))
            return result

        elif type(context) is list:
            result = []
            for c in context:
                result.append(Context.increase_hop_count(c))
            return result

        elif type(context) is Context:
            if len(context) == 1 and context.hopcount >= 0:
                c = copy.deepcopy(context)
                c.hopcount = context.hopcount + 1
            else:
                c = context
            return c
        else:
            raise Exception("Only set/list of Contexts or Context is allowed")

    #
    # Serialization
    #

    def serialize(self, zipped = False):
        """

        value is stored in double (d) : 8 bytes
        hopcount is stored in signed short (h) : 2 bytes

        timestamp is stored in unsigned short (H) : 2 bytes
        The rest of the data is serialized cohorts

        >>> c = Context(value=1.0, cohorts=set([1,2,3]))
        >>> c.serialize() == '\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?\\x00\\x00\\x00\\x00\\x0e' \
            or c.serialize() == '?\\xf0\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x0e'
        True
        """

        if self.value is None:
            value = float("inf")
        else:
            value = self.value

        if self.timestamp is None:
            timestamp = 0
        else:
            timestamp = self.timestamp

        v = struct.pack('d', value)
        h = struct.pack('h', self.hopcount)
        t = struct.pack('H', timestamp)

        result = v + h + t

        if self.cohorts is not None:
            result = v + h + t + str(self.cohorts)

        if zipped:
            return zlib.compress(result)
        else:
            return result

    @staticmethod
    def deserialize(stream, zipped = False):
        """Returns a Context object from a stream

        >>> c = Context(value=1.0, cohorts=set([0,1,2]))
        >>> s = c.serialize()
        >>> c2 = Context.deserialize(s)
        >>> c == c2
        True
        >>> c = Context(value=1.0, cohorts=set([0,1,2]))
        >>> s = c.serialize(zipped=True)
        >>> c2 = Context.deserialize(s,zipped=True)
        >>> c == c2
        True
        >>> c = Context()
        >>> s = c.serialize()
        >>> c2 = Context.deserialize(s)
        >>> c == c2
        True
        """
        if zipped:
            value = zlib.decompress(stream)
        else:
            value = stream

        # result = v + h + t + str(self.cohorts)
        # first 8 byte as a value
        v = struct.unpack('d', value[0:8])[0]
        h = struct.unpack('h', value[8:10])[0]
        t = struct.unpack('H', value[10:12])[0]

        if stream[12:]:
            c = bytearray(value[12:])
        else:
            c = None

        if v == float('inf'): v = None
        #if t == 0: t = None

        return Context(value=v, hopcount=h, timestamp=t, cohorts=c)

if __name__ == "__main__": # and __package__ is None:
    import doctest
    doctest.testmod()

