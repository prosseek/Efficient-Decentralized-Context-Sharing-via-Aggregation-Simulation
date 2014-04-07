import math

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