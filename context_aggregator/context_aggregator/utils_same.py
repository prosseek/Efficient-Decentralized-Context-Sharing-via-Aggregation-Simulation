"""Aggregation utility

standard format
===============

1. A list with two list elements
2. The list element is sorted and not duplicated
3. The first element is a set of single contexts
4. The second element is the element in an aggregated context

Contexts
========
We define contexts as

1. A set of single or aggregate contexts
2. There is only zero or one aggregate context
3. There can be zero or multiple single contexts

"""
from utils_is import *

def same(v1, v2):
    """
    This is abstract method that just compares everything.

    >>> x = [[1,2],[3,4]]
    >>> y = [set([1,2]), set([3,4])]
    >>> same(x,y)
    False

    >>> x = [[1,2],[3,4]]
    >>> y = set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=1.0, cohorts=[3,4])])
    >>> same(x,y)
    True
    >>> same(y,x)
    True

    >>> x = [[(1,-2),(2,3)],[3,4]]
    >>> y = set([Context(value=1.0, cohorts=[1], hopcount=-2), Context(value=1.0, cohorts=[2], hopcount=3), Context(value=1.0, cohorts=[3,4])])
    >>> same(x,y)
    True
    >>> same(y,x)
    True

    >>> x = [[1,2],[3,4]]
    >>> y = set([Context(value=1.0, cohorts=[1,2]), Context(value=1.0, cohorts=[3,4])])
    >>> same(x,y)
    True
    >>> same(y,x)
    True

    >>> x = [[1,2]]
    >>> y = set([Context(value=1.0, cohorts=[1,2])])
    >>> same(x,y)
    True
    >>> same(y,x)
    True

    >>> x = [[],[1,2]]
    >>> y = set([Context(value=1.0, cohorts=[1,2])])
    >>> same(x,y)
    True
    >>> same(y,x)
    True

    >>> r = {Context(value=0.0, cohorts={0}), Context(value=0.0, cohorts={1})}
    >>> same({Context(value=0.0, cohorts={0}), Context(value=0.0, cohorts={1})}, r)
    True
    """
    t1 = type(v1)
    t2 = type(v2)

    # WARING!
    # The ordering is important!
    #
    # 1. We need to use same() for checking equivalence between a set of aggregates and a list of list,
    #    for example: set([Context([1,2,3]), Context([4,5,6])]) == [[1,2,3],[4,5,6]]
    # 2. However, the standard format happens to have the same set of contexts and a list of list format.
    # 3. As a result, we need to check if the set of contexts is set of aggregates first, because
    #    for the standard, there should be only one aggregate.
    # 4. set([Context([1,2,3])]) == [[1,2,3]] <-- This is a set of aggregate checking
    #    set([Context([1,2,3])]) == [[], [1,2,3]] <-- this is standard type checking

    if id(v1) == id(v2): return True
    # if len(v1) != len(v2): return False

    if is_set_of_aggregates(v1) and is_list_list(v2):
        return same_contexts_and_list(v1, v2)

    if is_set_of_aggregates(v2) and is_list_list(v1):
        return same_contexts_and_list(v2, v1)

    if is_standard(v1) and is_contexts(v2):
        return v1 == contexts_to_standard(v2)
    if is_standard(v2) and is_contexts(v1):
        return v2 == contexts_to_standard(v1)

    if is_standard2(v1) and is_contexts(v2):
        return v1 == contexts_to_standard2(v2)
    if is_standard2(v2) and is_contexts(v1):
        return v2 == contexts_to_standard2(v1)

    if t1 is list and t2 is list:
        return same_list(v1, v2)
    if t1 is dict and t2 is dict:
        return same_dict(v1, v2)
    if t1 is set and t2 is set:
        if type(list(v1)[0]) is Context and type(list(v2)[0]) is Context:
            c1 = contexts_to_standard2(v1)
            c2 = contexts_to_standard2(v2)
            return c1 == c2

    return v1 == v2


def same_list(list1, list2):
    """Determine if list c1 and c2 are the same

    >>> s1 = [[1,2]]
    >>> s2 = [set([1,2])]
    >>> same_list(s1, s2)
    False

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

    >>> a = [Context(value=1.0, cohorts=[1,2,3]), Context(value=2.0, cohorts=[2,3,4])]
    >>> b = [[1,2,3],[2,3,4]]
    >>> same_list(a,b)
    True
    """
    if len(list1) != len(list2): return False
    if len(list1) == 0: return True

    t1 = type(list1[0])
    t2 = type(list2[0])

    if t1 is Context and t2 is list:
        list1 = [list(m.get_cohorts_as_set()) for m in list1]
        t1 = type(list1[0])

    if t2 is Context and t1 is list:
        list2 = [list(m.get_cohorts_as_set()) for m in list2]
        t2 = type(list2[0])

    if t1 != t2: return False

    # >>> map(frozenset, [1,2])
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    # TypeError: 'int' object is not iterable
    try:
        l1 = set(map(frozenset, list1))
        l2 = set(map(frozenset, list2))
    except TypeError:
        l1 = sorted(list1)
        l2 = sorted(list2)

    return l1 == l2

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

    >>> d1 = {1: [2,3], 2:[1,3], 3:[1,2]}
    >>> d2 = {2: [3, 1], 3: [2, 1], 1: [2, 3]}
    >>> same_dict(d1, d2)
    True

    """
    if dict1 == dict2: return True
    if sorted(dict1.keys()) != sorted(dict2.keys()): return False
    for k in dict1.keys():
        v1 = dict1[k]
        v2 = dict2[k]
        if not same(v1, v2): return False
    return True

def same_contexts_and_list(contexts, lists):
    """
    >>> g1 = Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = Context(value=2.0, cohorts=set([6,7,8]))
    >>> same_contexts_and_list(set([g1,g2,g3]), [[3, 4, 5],[7, 8, 6],[0, 1, 2]])
    True
    """
    result1 = set()
    result2 = set()
    for c in contexts:
        result1.add(frozenset(c.get_cohorts_as_set()))
    for c in lists:
        result2.add(frozenset(c))

    return result1 == result2

if __name__ == "__main__": # and __package__ is None:
    import doctest
    doctest.testmod()
