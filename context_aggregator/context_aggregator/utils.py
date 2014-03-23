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
import sys
#print sys.path
from context.context import Context
from utils_standard import *
from collections import OrderedDict


def is_list_list(input):
    """Returns if the input is list of list, and there should be no empty list

    >>> input = [[1,2,3],[5,5,6]]
    >>> is_list_list(input)
    True
    >>> input = [5,5,6]
    >>> is_list_list(input)
    False
    >>> input = [[],[5,5,6]]
    >>> is_list_list(input)
    False
    """
    if type(input) is not list: return False
    for i in input:
        if type(i) is not list: return False
        if not len(i): return False
    return True

def is_contexts(input):
    """

    >>> input = set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=2.0, cohorts=[3,4])])
    >>> is_contexts(input)
    True
    >>> input = set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[1]), Context(value=2.0, cohorts=[3,4])])
    >>> is_contexts(input)
    False
    >>> input = [Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[1]), Context(value=2.0, cohorts=[3,4])]
    >>> is_contexts(input)
    False
    """
    if type(input) is not set: return False
    for c in input:
        if type(c) is not Context: return False

    result1 = contexts_to_standard(input, remove_duplication=False)
    result2 = contexts_to_standard(input, remove_duplication=True)
    return result1 == result2

def is_set_of_aggregates(input):
    """

    >>> input = set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=2.0, cohorts=[3])])
    >>> is_set_of_aggregates(input)
    False
    >>> input = set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=2.0, cohorts=[3,4])])
    >>> is_set_of_aggregates(input)
    False
    >>> input = set([Context(value=1.0, cohorts=[1,3,4]), Context(value=1.0, cohorts=[2,1,3]), Context(value=2.0, cohorts=[3,4])])
    >>> is_set_of_aggregates(input)
    True
    """
    if type(input) is not set: return False
    for c in input:
        if type(c) is not Context: return False
        if c.is_single(): return False
    return True

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
    else:
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

    """
    if len(list1) != len(list2): return False
    if len(list1) == 0: return True

    t1 = type(list1[0])
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

def get_prime(contexts):
    """get prime contexts that does not have any common element with other contexts

    >>> g1 = Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = Context(value=2.0, cohorts=set([6,7,8]))
    >>> get_prime(set([g1,g2,g3]))[0] == set([g1, g3, g2])
    True
    >>> g1 = Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = Context(value=2.0, cohorts=set([5, 6,7,8]))
    >>> get_prime(set([g1,g2,g3]))[0] == set([g1])
    True
    >>> g1 = Context(value=1.0, cohorts=set([0]))
    >>> g2 = Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = Context(value=2.0, cohorts=set([5, 6,7,8]))
    >>> get_prime(set([g1,g2,g3]))[0] == set([g1])
    True
    >>> get_prime(set([g1,g2,g3]))[1] == set([g2, g3])
    True
    """
    prime = set()
    non_prime = set()
    # Index works only with list
    contexts = list(contexts)
    for i, c in enumerate(contexts):
        cs = exclude_context(i, contexts)
        if is_prime(c, cs):
            prime.add(c)
        else:
            non_prime.add(c)
    return prime, non_prime

def exclude_context(index, contexts):
    """Exclude context among contexts

    >>> g1 = Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = Context(value=2.0, cohorts=set([6,7,8]))
    >>> set(exclude_context(0, [g1,g2,g3])) == set([g3,g2])
    True
    """
    result = set()
    for i, c in enumerate(contexts):
        if index != i:
            result.add(c)
    return result

def is_prime(context, contexts):
    """Check if context is exclusive among contexts

    >>> g1 = Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=2.0, cohorts=set([3,4,5]))
    >>> g = Context(value=2.0, cohorts=set([6,7,8]))
    >>> is_prime(g, set([g1,g2]))
    True
    >>> g1 = Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=2.0, cohorts=set([3,4,5]))
    >>> g = Context(value=2.0, cohorts=set([6,7,8,0]))
    >>> is_prime(g, set([g1,g2]))
    False
    """
    #list_contexts = list(contexts)
    for c in contexts:
        if not is_exclusive(context, c):
            return False

    return True

def is_exclusive(context1, context2):
    """Check if context1 and context2 share any common element

    >>> g1 = Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=2.0, cohorts=set([0,1,2,3]))
    >>> is_exclusive(g1, g2)
    False
    >>> g1 = Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=2.0, cohorts=set([3,4,5]))
    >>> is_exclusive(g1, g2)
    True
    """
    s1 = context1.get_cohorts_as_set()
    s2 = context2.get_cohorts_as_set()
    return s1.isdisjoint(s2)

def separate_single_and_group_contexts(contexts):
    """Separate single and group contexts from a list of contexts

    >>> g1 = Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=2.0, cohorts=set([0,1,2,3]))
    >>> s1 = Context(value=1.0, cohorts=set([0]))
    >>> s2 = Context(value=2.0, cohorts=set([1]))
    >>> s,g = separate_single_and_group_contexts(set([g1,s1,g2,s2]))
    >>> ls = list(s)
    >>> ls[0].is_single() and ls[1].is_single()
    True
    >>> lg = list(g)
    >>> lg[0].is_single() or lg[1].is_single()
    False
    """

    singles = set()
    groups = set()

    for c in contexts:
        if c.is_single():
            singles.add(c)
        else:
            groups.add(c)

    return singles, groups

def is_in(context, contexts, ignore_value=False):
    """Returns if context is a member of contexts in a sense of equivalence

    >>> s3 = Context(value=0.0, cohorts=set([3]))
    >>> g1 = Context(value=2.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=3.0, cohorts=set([0,1,2,3]))
    >>> cs = set([s3,g1,g2])
    >>> s = Context(value=1.0, cohorts=set([3]))
    >>> is_in(s, cs, ignore_value=True)
    True
    >>> is_in(s, cs, ignore_value=False)
    False
    >>> s = Context(value=1.0, cohorts=set([10]))
    >>> is_in(s, cs, ignore_value=True)
    False
    """
    for c in contexts:
        if context.equiv(c, ignore_value):
            return True
    return False

def sort(contexts):
    """Given a set, sort the set in terms of size of elements, and return a sorted list

    >>> g1 = Context(value=2.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=3.0, cohorts=set([0,1,2,3]))
    >>> g3 = Context(value=2.0, cohorts=set([0,1]))
    >>> g4 = Context(value=0.0, cohorts=set([0]))
    >>> result = sort(set([g1, g2, g3, g4]))
    >>> result[0] == g4
    True
    >>> result[1] == g3
    True
    >>> result[2] == g1
    True
    >>> result[3] == g2
    True
    """
    cs = list(contexts)
    result = sorted(cs, key=len) # cmp=lambda m,n: len(m)-len(n))
    return  result


def remove(c, cs, ignore_value=False):
    """Remove context c from a set of contexts cs
    >>> g1 = Context(value=2.0, cohorts=set([0,1,2]))
    >>> g2 = Context(value=3.0, cohorts=set([0,1,2,3]))
    >>> g3 = Context(value=2.0, cohorts=set([0,1]))
    >>> g4 = Context(value=0.0, cohorts=set([0]))
    >>> result = remove(g1, set([g1,g2,g3,g4]))
    >>> is_in(g1, result) # result = set - g1
    False
    >>> len(result)
    3
    """
    result = set()
    for i in cs:
        if not c.equiv(i, ignore_value=ignore_value):
            result.add(i)
    return result

def get_maxcover_dictionary(contexts):
    """
    d = {'A': [1, 2, 3], 'B': [3, 4], 'C': [4, 5, 6]}
    >>> i = set([Context(value=1.0, cohorts=[3,1,2]), Context(value=2.0, cohorts=[3,4]), Context(value=3.0, cohorts=[4,5,6])])
    >>> r, r_context = get_maxcover_dictionary(i)
    >>> set(map(frozenset, r.values())) == set(map(frozenset, [[1,2,3],[3,4],[4,5,6]]))
    True
    """
    result = {}
    result_map_contexts = {}
    for i, c in enumerate(contexts):
        result[i] = list(c.get_cohorts_as_set())
        result_map_contexts[i] = c
    return result, result_map_contexts

#
# to_string
#

def sort_singles(contexts):
    """
    Sort a set of single contexts into a list

    >>> i = set([Context(value=10,cohorts=[3],timestamp=5,hopcount=4),Context(value=10,cohorts=[1],timestamp=5,hopcount=4),Context(value=10,cohorts=[2],timestamp=5,hopcount=4)])
    >>> r =sort_singles(i)
    >>> list(r[0].get_cohorts_as_set())[0] == 1 and list(r[1].get_cohorts_as_set())[0] == 2 and list(r[2].get_cohorts_as_set())[0] == 3
    True
    """
    return sorted(list(contexts), key=lambda c: list(c.get_cohorts_as_set())[0])

def sort_aggregates(contexts):
    """
    Sort a set of single contexts into a list

    >>> i = set([Context(value=10,cohorts=[1,3],timestamp=5,hopcount=4),Context(value=10,cohorts=[1,2,3],timestamp=5),Context(value=10,cohorts=[1,3,2,6,7],timestamp=5)])
    >>> r =sort_aggregates(i)
    >>> list(r[0].get_cohorts_as_set()) == [1, 2, 3, 6, 7] and list(r[1].get_cohorts_as_set()) == [1, 2, 3]
    True
    >>> print r[0],r[1],r[2]
    v(10.00):c([1,2,3,6,7]):h(0):t(5) v(10.00):c([1,2,3]):h(0):t(5) v(10.00):c([1,3]):h(4):t(5)
    """
    return sorted(list(contexts), key=len, reverse=True)


if __name__ == "__main__": # and __package__ is None:
    import doctest
    doctest.testmod()
