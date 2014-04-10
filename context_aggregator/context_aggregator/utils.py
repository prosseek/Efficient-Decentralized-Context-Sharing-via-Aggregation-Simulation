from utils_is import *
from utils_same import *

def is_in(context, contexts):
    """

    >>> contexts = {Context(value=1.0, cohorts=[1]), Context(value=2.0, cohorts=[2])}
    >>> context = Context(value=1.0, cohorts=[2], hopcount=10)
    >>> not is_in(context, contexts)
    False
    """

    cohorts1 = context.get_cohorts_as_set()

    for c in contexts:
        cohorts2 = c.get_cohorts_as_set()
        if cohorts1 == cohorts2:
            return c
    return False

def remove_if_in(context, contexts):
    """

    >>> contexts = {Context(value=1.0, cohorts=[1]), Context(value=2.0, cohorts=[2])}
    >>> context = Context(value=1.0, cohorts=[2], hopcount=10)
    >>> not is_in(context, contexts)
    False
    >>> remove_if_in(context, contexts)
    >>> is_in(context, contexts)
    False
    """
    c = is_in(context, contexts)
    if c:
        contexts.remove(c)

def get_average(contexts):
    """
    Caution: It assumes all the cohorts are exclusive.

    >>> a = {Context(value=2.0, cohorts=[1,2,3]), Context(value=1.0, cohorts=[5])}
    >>> get_average(a) == 1.75
    True
    """
    total_size = 0
    value = 0
    for c in contexts:
        size = len(c)
        total_size += size
        value += (c.value * size)
    return value/total_size

def empty_list(input):
    """
    >>> a = [[],[],[]]
    >>> empty_list(a)
    True
    >>> a = [[[],[]],[]]
    >>> empty_list(a)
    True
    >>> a = [[[],[]],[],1]
    >>> empty_list(a)
    False
    >>> a = [1,[]]
    >>> empty_list(a)
    False
    """
    # Non list value means non-empty -> return false
    if not(type(input) is list): return False

    # with  length zero means emtpy
    if len(input) == 0: return True

    # The real game
    for i in input:
        # We can finish the game early when it's not empty
        if not empty_list(i): return False

    # When nothing is non-empty, it's empty
    return True


def is_empty_dictionary(input):
    """
    >>> a = {33: [[], []], 2: [[], []], 3: [[], []], 35: [[], []]}
    >>> is_empty_dictionary(a)
    True
    >>> a = {}
    >>> is_empty_dictionary(a)
    True
    """
    if input == {}: return True
    for key, value in input.items():
        if type(value) is list:
            if not empty_list(value): return False
    return True


def get_matching_aggregate_contexts(aggregate_contexts, list_of_lists):
    """

    >>> aggrs = {Context(value=0.0, cohorts={0,1,2}), Context(value=0.0, cohorts={1,3}), Context(value=0.0, cohorts={2,4})}
    >>> r = get_matching_aggregate_contexts(aggrs, [[1,3],[2,4]])
    >>> same({Context(value=0.0, cohorts={1,3}), Context(value=0.0, cohorts={2,4})}, r)
    True
    >>> r = get_matching_aggregate_contexts(aggrs, [[1,3],[2,6]])
    >>> same({Context(value=0.0, cohorts={1,3})}, r)
    True
    """
    result = set()
    if aggregate_contexts:
        for c in aggregate_contexts:
            cohorts = c.get_cohorts_as_set()
            #print list_of_lists
            #for l in list_of_lists:
            if set(list_of_lists) == cohorts:
                result.add(c)
    return result

def get_matching_single_contexts(single_contexts, set_of_numbers):
    """

    >>> singles = {Context(value=0.0, cohorts={0}), Context(value=0.0, cohorts={1}), Context(value=0.0, cohorts={2})}
    >>> r = get_matching_single_contexts(singles, [0,1])
    >>> same({Context(value=0.0, cohorts={0}), Context(value=0.0, cohorts={1})}, r)
    True
    >>> singles = {Context(value=0.0, cohorts={1}, hopcount=Context.SPECIAL_CONTEXT), Context(value=0.0, cohorts={3}), Context(value=0.0, cohorts={2})}
    >>> r = get_matching_single_contexts(singles, [-1,3])
    >>> same({Context(value=0.0, cohorts={1}, hopcount=Context.SPECIAL_CONTEXT), Context(value=0.0, cohorts={3})}, r)
    True
    """
    result = set()
    for c in single_contexts:
        id = c.get_id()
        assert id != Context.AGGREGATED_CONTEXT
        if c.hopcount == Context.SPECIAL_CONTEXT:
            id = -id
        if id in set_of_numbers:
            result.add(c)
    return result

def get_prime(contexts):
    """get prime contexts that does not have any common element with other contexts

    >>> g1 = Context(value=1.0, cohorts={0,1,2})
    >>> g2 = Context(value=2.0, cohorts={3,4,5})
    >>> g3 = Context(value=2.0, cohorts={6,7,8})
    >>> get_prime({g1,g2,g3})[0] == {g1, g3, g2}
    True
    >>> g1 = Context(value=1.0, cohorts={0,1,2})
    >>> g2 = Context(value=2.0, cohorts={3,4,5})
    >>> g3 = Context(value=2.0, cohorts={5, 6,7,8})
    >>> get_prime({g1,g2,g3})[0] == {g1}
    True
    >>> g1 = Context(value=1.0, cohorts={0})
    >>> g2 = Context(value=2.0, cohorts={3,4,5})
    >>> g3 = Context(value=2.0, cohorts={5, 6,7,8})
    >>> get_prime({g1,g2,g3})[0] == {g1}
    True
    >>> get_prime({g1,g2,g3})[1] == {g2, g3}
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

    >>> g1 = Context(value=1.0, cohorts={0,1,2})
    >>> g2 = Context(value=2.0, cohorts={3,4,5})
    >>> g3 = Context(value=2.0, cohorts={6,7,8})
    >>> set(exclude_context(0, [g1,g2,g3])) == {g3,g2}
    True
    """
    result = set()
    for i, c in enumerate(contexts):
        if index != i:
            result.add(c)
    return result

def separate_single_and_group_contexts(contexts):
    """Separate single and group contexts from a list of contexts

    >>> g1 = Context(value=1.0, cohorts={0,1,2})
    >>> g2 = Context(value=2.0, cohorts={0,1,2,3})
    >>> s1 = Context(value=1.0, cohorts={0})
    >>> s2 = Context(value=2.0, cohorts={1})
    >>> s,g = separate_single_and_group_contexts({g1,s1,g2,s2})
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

def remove(c, cs, ignore_value=False):
    """Remove context c from a set of contexts cs

    >>> g1 = Context(value=2.0, cohorts={0,1,2})
    >>> g2 = Context(value=3.0, cohorts={0,1,2,3})
    >>> g3 = Context(value=2.0, cohorts={0,1})
    >>> g4 = Context(value=0.0, cohorts={0})
    >>> result = remove(g1, {g1,g2,g3,g4})
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
    >>> i = {Context(value=1.0, cohorts={3,1,2}), Context(value=2.0, cohorts={3,4}), Context(value=3.0, cohorts={4,5,6})}
    >>> r, r_context = get_maxcover_dictionary(i)
    >>> same(r.values(), [[1,2,3],[3,4],[4,5,6]])
    True
    """
    result = {}
    result_map_contexts = {}
    for i, c in enumerate(contexts):
        result[i] = list(c.get_cohorts_as_set())
        result_map_contexts[i] = c
    return result, result_map_contexts

if __name__ == "__main__":
    import doctest
    doctest.testmod()