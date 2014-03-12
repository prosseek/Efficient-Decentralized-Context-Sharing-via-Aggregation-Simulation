__author__ = 'smcho'

def same(v1, v2):
    t1 = type(v1)
    t2 = type(v2)

    if t1 is list and t2 is list:
        return same_list(v1, v2)
    if t1 is dict and t2 is dict:
        return same_dict(v1, v2)
    else:
        return v1 == v2


def same_dict(dict1, dict2):
    """same dictionary

    # Same element means same dictionary
    >>> d1 = {"a":1, "b":2, "c":[1,2,3]}
    >>> d2 = {"c":[1,2,3], "b":2, "a":1}
    >>> same_dict(d1, d2)
    True

    # Same reference means same dictionary
    >>> d1 = {"a":1, "b":2, "c":[1,2,3]}
    >>> d2 = d1
    >>> same_dict(d1, d2)
    True

    >>> d1 = {"a":1, "b":2, "c":[1,2,3]}
    >>> d2 = {"a":1, "c":[1,2,3]}
    >>> same_dict(d1, d2)
    False

    """
    if dict1 == dict2: return True
    if dict1.keys() != dict2.keys(): return False
    for k in dict1.keys():
        v1 = dict1[k]
        v2 = dict2[k]
        if not same(v1, v2): return False
    return True


def same_list(list1, list2):
    """Determine if list c1 and c2 are the same

    >>> set2 = [[1,2], [1,2,3], [2,3,4]]
    >>> set2p = [[2,1], [2,3,4], [2,1,3]]
    >>> same_list(set2, set2p)
    True

    >>> set2 = [set([1,2]), set([1,2,3]), set([2,3,4])]
    >>> set2p = [set([2,1]), set([2,3,4]), set([2,1,3])]
    >>> same_list(set2, set2p)
    True

    >>> a = [1,2,3,4,5]
    >>> b = [1,2,3,4,5]
    >>> same_list(a,b)
    True

    """

    try:
        l1 = set(map(frozenset, list1))
        l2 = set(map(frozenset, list2))
    except TypeError:
        l1 = list1
        l2 = list2

    return l1 == l2

if __name__ == "__main__":
    import doctest
    doctest.testmod()