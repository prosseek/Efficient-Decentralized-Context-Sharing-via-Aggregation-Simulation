"""Aggregation utility
"""
import sys
#print sys.path
import context.context as context

def get_prime(contexts):
    """get prime contexts that does not have any common element with other contexts

    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = context.Context(value=2.0, cohorts=set([6,7,8]))
    >>> get_prime(set([g1,g2,g3])) == set([g1, g3, g2])
    True
    >>> g1 = context.Context(value=1.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=2.0, cohorts=set([3,4,5]))
    >>> g3 = context.Context(value=2.0, cohorts=set([5, 6,7,8]))
    >>> get_prime(set([g1,g2,g3])) == set([g1])
    True
    """
    result = set()
    # Index works only with list
    contexts = list(contexts)
    for i, c in enumerate(contexts):
        cs = exclude_context(i, contexts)
        if is_prime(c, cs):
            result.add(c)
    return result

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
    >>> is_in(g1, result)
    False
    >>> len(result)
    3
    """
    result = set()
    for i in cs:
        if not c.equiv(i, ignore_value=ignore_value):
            result.add(i)
    return result

def dis_aggregate(contexts):
    """Given a set of contexts, subtract all the contexts

    >>> g1 = context.Context(value=2.0, cohorts=set([0,1,2]))
    >>> g2 = context.Context(value=3.0, cohorts=set([0,1,2,3]))
    >>> g3 = context.Context(value=2.0, cohorts=set([0,1]))
    >>> g4 = context.Context(value=0.0, cohorts=set([0]))
    >>> result = dis_aggregate(set([g1,g2,g3,g4]))
    >>> s1 = context.Context(value=0.0, cohorts=set([0]))
    >>> s2 = context.Context(value=0.0, cohorts=set([1]))
    >>> s3 = context.Context(value=0.0, cohorts=set([2]))
    >>> s4 = context.Context(value=0.0, cohorts=set([3]))
    >>> s5 = context.Context(value=0.0, cohorts=set([10]))
    >>> is_in(s1, result) and is_in(s2, result) and is_in(s3, result)
    True
    >>> is_in(s4, result) and is_in(s5, result)
    True
    """

    pass
    # cs = contexts
    # index = 0
    # while True:
    #     l = sorted(contexts)
    #     sub = l[0]
    #     sup = l[1:]
    #
    #     broken_contexts = []
    #     newly_generated_contexts = []
    #     for c in sup:
    #         r = c - sub
    #         if r:
    #             newly_generated_contexts.append(r)
    #             broken_contexts.append(sup)
    #             remove(r, cs)
    #
    #     # if something is divided
    #     if divided:
    #
    #
    #     if index >= len(l): break

if __name__ == "__main__": # and __package__ is None:
    import doctest
    doctest.testmod()