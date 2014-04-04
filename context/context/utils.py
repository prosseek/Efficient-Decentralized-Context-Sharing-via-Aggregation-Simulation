r"""context.utils is a module for context operations

1. set is major data structure that works as an intermediate format
2. for integer we use unsigned 8 bytes integer (unsigned long long, Q)
3. we have a routine to/from int <-> bytearray
4. we have a routine to/from bytearray <-> set
5. other routines from/to set <-> int is implemented based on 3 and 4

"""
import struct

#MAXIMUM_INTEGER_BYTES=8

#
# utilities that can be used other routins
#

def get_number_of_one_from_number(value, number_of_bytes = 8):
    """Returns the number of 1 in a value
    assumes that the value is integer with 8 bytes (unsigned long long int)

    >>> get_number_of_one_from_number(2**3-1)
    3
    >>> get_number_of_one_from_number(2**8-1)
    8
    >>> get_number_of_one_from_number(2**16-1)
    16
    >>> int(get_number_of_one_from_number(2**32-1)) # return value is 32L, so make it integer
    32
    >>> int(get_number_of_one_from_number(2**(8*8)-1))
    64
    """
    count = 0
    for i in range(number_of_bytes*8):
        count += (value >> i) & 1
    return count
    
def get_number_of_one_from_set(value):
    """Returns the number of elements in a set
    This is equivalent to calculate the 1s in a long typed data, or in a bytearray
    
    >>> get_number_of_one_from_set(set([0,1,2,3]))
    4
    >>> get_number_of_one_from_set(set([]))
    0
    """

    if value is None: return 0
    return len(value)
    
def get_number_of_one_from_bytearray(value):
    """Returns the number of 1's in a byte array
    
    >>> get_number_of_one_from_bytearray(long2bytearray(7))
    3
    >>> get_number_of_one_from_bytearray(long2bytearray(568152328328))
    10
    """
    if value is None: return 0

    count = 0
    
    for i in value:
        count += get_number_of_one_from_number(i, number_of_bytes = 1)
    return count
    
def get_number_of_one(value):
    """Returns the numbe of one regardless of input type
    
    >>> get_number_of_one(4.5)
    Traceback (most recent call last):
    ...
    TypeError: not supported type
    """
    t = type(value)
    if t in [long, int]:
        return get_number_of_one_from_number(value)
    elif t is [bytearray]:
        return get_number_of_one_from_bytearray(value)
    elif t is [set]:
        return get_number_of_one_from_set(value)
    else:
        raise TypeError("not supported type")

def byte2set(value, offset = 0):
    """Returns a set from 1 byte data (0 - 255)

    Args:
        value (int) : range 0 - 255
        offset (int) : the offset value added to the result

    >>> byte2set(7) == set([0, 1, 2])
    True
    >>> byte2set(255) == set([0, 1, 2, 3, 4, 5, 6, 7])
    True
    >>> byte2set(256)
    Traceback (most recent call last):
    ...
    AssertionError: value 256
    >>> byte2set(7, offset=6) == set([6, 7, 8])
    True
    """

    assert 0 <= value < 256, "value %d" % value

    result = set()
    for i in range(8):
        if (value >> i) & 1:
            result.add(i + offset)
    return result

#
# bytearray to/from set
#

def bytearray2set(value):
    """Returns a set from bytearry
    >>> bytearray2set(bytearray([7])) == set([0, 1, 2])
    True
    >>> bytearray2set(bytearray([7,7])) == set([0, 1, 2, 8, 9, 10])
    True
    >>> bytearray2set(bytearray([7,7,7])) == set([0, 1, 2, 8, 9, 10, 16, 17, 18])
    True
    """
    assert value is not None

    result = set()
    for e, i in enumerate(value):
        r = byte2set(i, 8*e)
        result |= r

    return result


def set2bytearray(value):
    """Returns a bytearray from input set

    Algorithm ::

        19 = 8*2 + 3, so the 2nd byte's 3rd bit should be set
        bytearray[2] |= (1 >> 3)

    >>> set2bytearray(set([0]))
    bytearray(b'\\x01')
    >>> set2bytearray(set([0,1,2]))
    bytearray(b'\\x07')
    >>> set2bytearray(set([0, 3, 4, 11, 12, 14, 16, 18, 19]))
    bytearray(b'\\x19X\\r')
    >>> bytearray2set(set2bytearray(set([0, 3, 4, 11, 12, 14, 16, 18, 19]))) == set([0, 3, 4, 11, 12, 14, 16, 18, 19])
    True
    >>> # No empty set allwed
    >>> set2bytearray(set([]))
    Traceback (most recent call last):
        ...
    AssertionError: Empty set not allowed
    """
    assert value != set([]), "Empty set not allowed"

    max_byte_size = (max(value) / 8) + 1
    result = bytearray(max_byte_size)
    for i in value:
        shift = i % 8
        index = i / 8
        result[index] |= (1 << shift)
    return result

#
# long to/from bytearray
#

def long2bytearray(value):
    """Returns a bytearray from unsigned long long with 8 bytes (Q) and little endian(<)

    >>> long2bytearray(12345)
    bytearray(b'90\\x00\\x00\\x00\\x00\\x00\\x00')
    >>> long2bytearray(7)
    bytearray(b'\\x07\\x00\\x00\\x00\\x00\\x00\\x00\\x00')
    >>> long2bytearray(874521)
    bytearray(b'\\x19X\\r\\x00\\x00\\x00\\x00\\x00')
    """
    return bytearray(struct.pack("<Q", value))


def bytearray2long(value):
    """Returns a long value from bytearray

    >>> bytearray2long(bytearray([7]))
    7
    >>> bytearray2long(bytearray([0,1]))
    256
    >>> bytearray2long(bytearray([7,7,7]))
    460551
    """
    result = 0
    for e, i in enumerate(value):
        r = i
        #print r
        r <<= 8*e
        result += r
    return result

#
# long to/from set
#

def long2set(value):
    """Returns set from long value

    >>> r = long2set(7)
    >>> sorted(list(r))
    [0, 1, 2]
    """
    r = long2bytearray(value)
    return bytearray2set(r)

def set2long(value):
    """
    >>> set2long(set([1,16,8]))
    65794
    """
    r = set2bytearray(value)
    return bytearray2long(r)

#
# Operations
#

def cohort_type_as_set(cohort):
    """Cohorts from bytearray/int/set to set

    >>> r = cohort_type_as_set(set([1,2,3]))
    >>> sorted(list(r))
    [1, 2, 3]
    >>> cohort_type_as_set(65794) == set([1, 8, 16])
    True
    """
    t = type(cohort)

    assert t in [int, long, bytearray, set]

    if t in [int, long]:
        ch = long2set(cohort)
    elif t in [bytearray]:
        ch = bytearray2set(cohort)
    else:
        ch = cohort

    return ch

def cohort_type_as_bytearray(cohort):
    """Cohorts from bytearray/int/set to set

    >>> bytearray2set(cohort_type_as_bytearray(set([1,2,3]))) == set([1, 2, 3])
    True
    >>> bytearray2set(cohort_type_as_bytearray(65794)) == set([1, 8, 16])
    True
    """
    t = type(cohort)
    # [2014/03/14] - list is added for cohort conversion process
    # This is for utility (made my life easier)
    assert t in [int, list, long, bytearray, set], "wrong type %s" % t

    if t in [int, long]:
        ch = long2bytearray(cohort)
    elif t in [set]:
        ch = set2bytearray(cohort)
    elif t in [list]:
        ch = set2bytearray(set(cohort))
    else:
        ch = cohort

    return ch

def add(cohort1, cohort2):
    """Returns the additon of c1 and c2

    >>> add(set([1,2,3]), set([1,4,5]))
    >>> add(set([1,2,3]), set([4,5])) == set([1,2,3,4,5])
    True
    """
    ch1 = cohort_type_as_set(cohort1)
    ch2 = cohort_type_as_set(cohort2)

    # addition of two cohorts has meaning when they are exclusive

    if ch1 & ch2:
        return None
    else:
        return ch1 | ch2

def sub(cohort1, cohort2):
    """Returns the additon of c1 and c2

    >>> sub(set([1,2,3]), set([1,4,5]))
    >>> sub(set([1,2,3,4,5]), set([4,5])) == set([1,2,3])
    True
    >>> sub(set([1,2,3,4,5]), set([1,2,3,4,5]))
    set([])
    >>> sub(set([1,2,3]), set([1,2,3,4,5]))
    """
    ch1 = cohort_type_as_set(cohort1)
    ch2 = cohort_type_as_set(cohort2)

    if ch1 >= ch2:
        return ch1 - ch2
    else:
        return None

    # addition of two cohorts has meaning when they are exclusive

    if ch1 & ch2:
        return None
    else:
        return ch1 | ch2

if __name__ == "__main__":
    import doctest
    doctest.testmod()
