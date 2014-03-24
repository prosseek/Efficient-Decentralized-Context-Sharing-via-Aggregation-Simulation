from utils_standard import *

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

    >>> input = {Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=2.0, cohorts=[3,4])}
    >>> is_contexts(input)
    True
    >>> input = {Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[1]), Context(value=2.0, cohorts=[3,4])}
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

    >>> input = {Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=2.0, cohorts=[3])}
    >>> is_set_of_aggregates(input)
    False
    >>> input = {Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=2.0, cohorts=[3,4])}
    >>> is_set_of_aggregates(input)
    False
    >>> input = {Context(value=1.0, cohorts=[1,3,4]), Context(value=1.0, cohorts=[2,1,3]), Context(value=2.0, cohorts=[3,4])}
    >>> is_set_of_aggregates(input)
    True
    """
    if type(input) is not set: return False
    for c in input:
        if type(c) is not Context: return False
        if c.is_single(): return False
    return True

def is_in(context, contexts, ignore_value=False):
    """Returns if context is a member of contexts in a sense of equivalence

    >>> s3 = Context(value=0.0, cohorts={3})
    >>> g1 = Context(value=2.0, cohorts={0,1,2})
    >>> g2 = Context(value=3.0, cohorts={0,1,2,3})
    >>> cs = {s3,g1,g2}
    >>> s = Context(value=1.0, cohorts={3})
    >>> is_in(s, cs, ignore_value=True)
    True
    >>> is_in(s, cs, ignore_value=False)
    False
    >>> s = Context(value=1.0, cohorts={10})
    >>> is_in(s, cs, ignore_value=True)
    False
    """
    for c in contexts:
        if context.equiv(c, ignore_value):
            return True
    return False

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()