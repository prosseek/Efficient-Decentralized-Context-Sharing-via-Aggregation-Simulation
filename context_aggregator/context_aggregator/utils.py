"""Aggregation utility
"""
import sys
#print sys.path
import context.context as context
from collections import OrderedDict

def same(v1, v2):
    t1 = type(v1)
    t2 = type(v2)

    if t1 is list and t2 is list:
        return same_list(v1, v2)
    if t1 is dict and t2 is dict:
        return same_dict(v1, v2)
    else:
        return v1 == v2


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

def compare_contexts_and_cohorts(contexts, lists):
    """
    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = context.Context(value=2.0, cohorts=set([6,7,8]))
    >>> compare_contexts_and_cohorts(set([g1,g2,g3]), [[3, 4, 5],[7, 8, 6],[0, 1, 2]])
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

    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = context.Context(value=2.0, cohorts=set([6,7,8]))
    >>> get_prime(set([g1,g2,g3]))[0] == set([g1, g3, g2])
    True
    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = context.Context(value=2.0, cohorts=set([5, 6,7,8]))
    >>> get_prime(set([g1,g2,g3]))[0] == set([g1])
    True
    >>> g1 = context.Context(value=1.0, cohorts=set([0]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = context.Context(value=2.0, cohorts=set([5, 6,7,8]))
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

    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = context.Context(value=2.0, cohorts=set([6,7,8]))
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

    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> g = context.Context(value=2.0, cohorts=set([6,7,8]))
    >>> is_prime(g, set([g1,g2]))
    True
    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> g = context.Context(value=2.0, cohorts=set([6,7,8,0]))
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

    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([0,1,2,3]))
    >>> is_exclusive(g1, g2)
    False
    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> is_exclusive(g1, g2)
    True
    """
    s1 = context1.get_cohorts_as_set()
    s2 = context2.get_cohorts_as_set()
    return (s1 & s2) == set([])

def separate_single_and_group_contexts(contexts):
    """Separate single and group contexts from a list of contexts

    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([0,1,2,3]))
    >>> s1 = context.Context(value=1.0, cohorts=set([0]))
    >>> s2 = context.Context(value=2.0, cohorts=set([1]))
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

    >>> s3 = context.Context(value=0.0, cohorts=set([3]))
    >>> g1 = context.Context(value=2.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=3.0, cohorts=set([0,1,2,3]))
    >>> cs = set([s3,g1,g2])
    >>> s = context.Context(value=1.0, cohorts=set([3]))
    >>> is_in(s, cs, ignore_value=True)
    True
    >>> is_in(s, cs, ignore_value=False)
    False
    >>> s = context.Context(value=1.0, cohorts=set([10]))
    >>> is_in(s, cs, ignore_value=True)
    False
    """
    for c in contexts:
        if context.equiv(c, ignore_value):
            return True
    return False

def sort(contexts):
    """Given a set, sort the set in terms of size of elements, and return a sorted list

    >>> g1 = context.Context(value=2.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=3.0, cohorts=set([0,1,2,3]))
    >>> g3 = context.Context(value=2.0, cohorts=set([0,1]))
    >>> g4 = context.Context(value=0.0, cohorts=set([0]))
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
    >>> g1 = context.Context(value=2.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=3.0, cohorts=set([0,1,2,3]))
    >>> g3 = context.Context(value=2.0, cohorts=set([0,1]))
    >>> g4 = context.Context(value=0.0, cohorts=set([0]))
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
    >>> i = set([context.Context(value=1.0, cohorts=[3,1,2]), context.Context(value=2.0, cohorts=[3,4]), context.Context(value=3.0, cohorts=[4,5,6])])
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

if __name__ == "__main__": # and __package__ is None:
    import doctest
    doctest.testmod()