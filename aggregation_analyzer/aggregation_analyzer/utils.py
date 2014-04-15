import math

import copy

#from aggregation_analyzer.read_reports import
from aggregation_analyzer.utils_location import *

def avg(l):
    """
    >>> l = [1,2,3]
    >>> avg(l) == 2.0
    True
    """
    return 1.0*sum(l)/len(l)

### TODO
### same name in utils_report
def simple_dict_to_list(dictionary):
    """
    >>> x = {'a':10, 'b':20}
    >>> simple_dict_to_list(x) == [10,20]
    True
    """
    return [dictionary[key] for key in sorted(dictionary.keys())]

def recover_to_list(input):
    """
    >>> input = ' [?(1), ?(2), ?(3), ?(4), ?(5), 6.00, 7.00, 5.00(*)]'
    >>> recover_to_list(input) == ['?(1)', '?(2)', '?(3)', '?(4)', '?(5)', 6.0, 7.0, '5.00(*)']
    True
    """
    pos1 = input.index('[')
    pos2 = input.index(']')
    r = input[pos1+1:pos2]
    results = []
    for val in r.split(','):
        if val.startswith('?'):
            results.append(val)
        elif val.startswith(' ?'):
            results.append(val[1:])
        elif val.endswith('(*)'):
            results.append(val)
        else:
            results.append(float(val))
    return results

def get_index_with_true(input):
    """This is the routine to find the *real* communication speed:
    True means that there is no input/ouput (no communication); in some cases the communication temporarily
    stops to start again.

    This example stops after 6 steps
    >>> input = [False, False, False, False, False, False, True, True, True]
    >>> get_index_with_true(input)
    6
    >>> input = [False, False, False, False, False, False, False, True, True]
    >>> get_index_with_true(input)
    7
    >>> input = [False, True, False, False, False, False, False, True, True]
    >>> get_index_with_true(input)
    7
    """
    reversed_input = copy.copy(input)
    reversed_input.reverse()
    result = -1
    for i, value in enumerate(reversed_input):
        if value == False:
            result = i
            break
    if result == -1: raise RuntimeError("Input error: all values are True %s" % input)
    return len(input) - i

def sum_lists_column(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,3],[1,2,3]]
    >>> sum_lists_column(input) == [3,6,9]
    True
    """
    return map(sum, zip(*input))

def avg_lists_column(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,3],[1,2,3]]
    >>> avg_lists_column(input) == [1,2,3]
    True
    >>> input = [([1,2], [3,4],[5,6]), ([7,8],[9,10],[11,6])]
    >>> avg_lists_column(input) ==  ([4, 5], [6, 7], [8, 6])
    True
    """
    # input checking
    assert len(input), "Error, there is no input"
    if len(input) == 1: return input

    t = type(input[0])

    if t is list:
        r = map(sum, zip(*input))
        length = len(input)
        return map(lambda m: m/length, r)
    else:
        assert t is tuple, "wrong input %s and type (%s)" % (input, t)
        y = zip(*input)
        r = [avg_lists_column(i) for i in y]
        return tuple(r)

def max_lists_column(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,5],[7,2,3]]
    >>> max_lists_column(input) == [7,2,5]
    True
    """
    r = map(lambda m: max(m), zip(*input))
    return r

def min_lists_column(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,5],[7,2,3]]
    >>> min_lists_column(input) == [1,2,3]
    True
    """
    r = map(lambda m: min(m), zip(*input))
    return r

def last_lists(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,3],[1,2,3]]
    >>> last_lists(input) == [3,3,3]
    True
    """
    return map(lambda m: m[-1], input)

def starts_with(name, keys):
    """

    >>> keys = ["abc", "def", "xyz"]
    >>> print starts_with("abcdef", keys)
    abc
    >>> starts_with("k", keys)
    """
    for key in keys:
        #if key.startswith(name): return key
        if name.startswith(key): return key
    return None

def can_be_integer(value):
    """
    >>> can_be_integer(3.5)
    False
    >>> can_be_integer(3.0)
    True
    >>> can_be_integer(3.000000000000001)
    False
    """
    assert type(value) is float, "Only float type of input is allowed, type is wrong %s" % type(value)
    int_value = int(value)
    if value - int_value == 0.0: return True
    return False

def get_xy(value):
    """Given value as a number, find the x*y == value where x = y

    >>> get_xy(25) == [5,5]
    True
    >>> get_xy(40) == [8,5]
    True
    >>> get_xy(41) == [41,1]
    True
    >>> get_xy(20) == [5,4]
    True
    """
    def _get_xy(value, x):
        if x == 0:
            return None
        else:
            y = 1.0*value/x
            if can_be_integer(y): return sorted((x, int(y)), key=lambda e:-e)
            else:
                return _get_xy(value, x-1)

    assert value > 0, "The value should be positive integer %d is not allowed" % value
    x = int(math.sqrt(value))
    if x == 1: return (1, value)
    return _get_xy(value, x)

def _get_approx_xy(value, x, y, margin):
    if x > 10000: return None
    elif abs(x - y) <= margin:
        return (value, x, y)
    else:
        x1, y1 = get_xy(value + 1)
        return _get_approx_xy(value + 1, x1, y1, margin)

def get_approx_xy(value, margin = 1):
    """
    >>> get_approx_xy(53, margin=1)
    (56, 8, 7)
    >>> get_approx_xy(57, margin=1)
    (64, 8, 8)
    >>> get_approx_xy(57, margin=2)
    (63, 9, 7)
    >>> get_approx_xy(57, margin=5)
    (60, 10, 6)
    >>> get_approx_xy(98, margin=3)
    (99, 11, 9)
    """
    (x, y) = get_xy(value)
    return _get_approx_xy(value, x, y, margin)


if __name__ == "__main__":
    import doctest
    doctest.testmod()