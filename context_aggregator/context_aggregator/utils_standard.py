"""Standard format utility

standard format
===============

1. A list with two list elements
2. The list element is sorted and not duplicated
3. The first element is a set of single contexts
4. The second element is the element in an aggregated context

example:
[[1,2,3],[4,5,6]] => three single contexts and one aggregated context with elements of 4,5,6

standard2 format
================

1. Same as standard1 format, but the single element is a tuple with (id, hop_count).

Example:
[[(1,0), (2,-3), (3,4)],[4,5,6]] => single context 1 is sampled, single context 2 is special, single context 3 has hopcount of 4


Contexts
========
We define contexts as

1. A set of single or aggregate contexts
2. There is only zero or one aggregate context
3. There can be zero or multiple single contexts

"""
from context.context import Context
#from utils_same import same

def aggregated_contexts_to_list_of_standard(contexts):
    """
    >>> x = set([Context(value=1.0, cohorts=[1,3,4,5]), Context(value=1.0, cohorts=[2,1,6,7]), Context(value=1.0, cohorts=[3,4,5,6,7])])
    >>> r = aggregated_contexts_to_list_of_standard(x)

    >>> res1 = [[1, 3, 4, 5], [1, 2, 6, 7], [3, 4, 5, 6, 7]]
    >>> res2 = [[1, 2, 6, 7], [1, 3, 4, 5], [3, 4, 5, 6, 7]]
    >>> r == res1 or r == res2
    True
    """
    result = []
    for c in contexts:
        r = contexts_to_standard(set([c]))[1]
        result.append(r)
    return sorted(result, key=lambda a: (len(a), a))

def contexts_to_standard2(context_set, remove_duplication=True):
    """
    Assume that there is only one aggregate, when there are more than one aggregated contexts, only
    the last one is used.

    When return_list, duplication may be possible, so the caller should be make sure there is no duplication.

    >>> x = set([Context(value=1.0, cohorts=[1], hopcount=Context.SPECIAL_CONTEXT), Context(value=1.0, cohorts=[2]), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[(1,-3),(2,0)],[3,4]]
    >>> contexts_to_standard2(x) == y
    True
    >>> x = set([Context(value=1.0, cohorts=[1], hopcount=0), Context(value=1.0, cohorts=[2], hopcount=-3), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[(1,0),(2,-3)],[3,4]]
    >>> contexts_to_standard2(x) == y
    True
    >>> x = set([Context(value=1.0, cohorts=[1], hopcount=0), Context(value=1.0, cohorts=[1], hopcount=0), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[(1,0)],[3,4]]
    >>> contexts_to_standard2(x) == y
    True
    >>> x = set([Context(value=1.0, cohorts=[1], hopcount=0), Context(value=1.0, cohorts=[1], hopcount=0), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[(1,0),(1,0)],[3,4]]
    >>> contexts_to_standard2(x, remove_duplication=False) == y
    True
    >>> contexts_to_standard2(None, remove_duplication=False) == [[],[]]
    True
    """

    # None processing is necessary, as sometimes aggregated contexts can be None and be requested
    # to convert using this method.
    if context_set is None:
        return [[],[]]

    assert type(context_set) in [set, list], "%s" % context_set
    singles = []
    aggregate = []
    for c in context_set:
        if c.is_single():
            singles.append(c.get_cohort_as_tuple())
        else:
            aggregate = list(c.get_cohorts_as_set())

    if remove_duplication:
        return [sorted(list(set(singles))), sorted(list(set(aggregate)))]
    else:
        return [sorted(singles), sorted(aggregate)]

def contexts_to_standard(context_set, remove_duplication=True):
    """
    Assume that there is only one aggregate, when there are more than one aggregated contexts, only
    the last one is used.

    When return_list, duplication may be possible, so the caller should be make sure there is no duplication.

    >>> x = set([Context(value=1.0, cohorts=[1], hopcount=Context.SPECIAL_CONTEXT), Context(value=1.0, cohorts=[2]), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[-1,2],[3,4]]
    >>> contexts_to_standard(x) == y
    True

    >>> x = set([Context(value=1.0, cohorts=[1], hopcount=Context.SPECIAL_CONTEXT), Context(value=1.0, cohorts=[2],hopcount=Context.SPECIAL_CONTEXT), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[-2,-1],[3,4]]
    >>> contexts_to_standard(x) == y
    True

    >>> x = set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[2]), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[1,2],[3,4]]
    >>> contexts_to_standard(x) == y
    True

    >>> x = set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[1,1],[3,4]]
    >>> contexts_to_standard(x, remove_duplication=False) == y
    True

    >>> x = set([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[1],[3,4]]
    >>> contexts_to_standard(x) == y
    True

    >>> x = list([Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[1]), Context(value=1.0, cohorts=[3,4])])
    >>> y = [[1],[3,4]]
    >>> contexts_to_standard(x) == y
    True

    >>> x = None
    >>> y = [[],[]]
    >>> contexts_to_standard(x) == y
    True
    """
    # y = [[(1,0),(1,0)],[3,4]]
    # When  result is [[],[]] with input of None, it shouldn't go through this routine
    result = contexts_to_standard2(context_set, remove_duplication)
    if context_set is not None:
        return [sorted(map(lambda m: m[0] if m[1] >= 0 else -m[0], result[0])), result[1]]
    else:
        return result # [[],[]] will be returned

def is_standard2(input):
    """
    >>> input = [[(1,0),(2,1),(3,-3),(4,-2)],[5,6,7]]
    >>> is_standard2(input)
    True
    >>> input = [[1,2,3,4],[5,6,7]]
    >>> is_standard2(input)
    False
    >>> input = [[(1,-3),2,3],[3,4]]
    >>> is_standard2(input)
    False
    >>> input = set([1,2,3])
    >>> is_standard2(input)
    False
    >>> input = [[(3,-3),(1,0),(2,1),(4,-2)],[5,6,7]]
    >>> is_standard2(input)
    False
    >>> input = [[(1,0),(1,0),(3,-3),(4,-2)],[5,6,7]]
    >>> is_standard2(input)
    False
    """
    if type(input) is not list: return False
    if len(input) != 2: return False

    if type(input[0]) is not list or type(input[1]) is not list: return False
    for i in input[0]:
        if type(i) is not tuple: return False
        if len(i) != 2: return False
        if type(i[0]) not in [int, long] or type(i[1]) not in [int, long]: return False
    for i in input[1]:
        if type(i) not in [long, int]: return False

    if sorted(input[0]) != input[0] or sorted(input[1]) != input[1]: return False
    if len(set(input[0])) != len(input[0]) or len(set(input[1])) != len(input[1]): return False
    return True

def is_dictionary_standard(input):
    """Check if all the elements of dictionary input are in standard form
    By definition, {} is *not* in standard form

    >>> in1 = {1:[[],[]]}
    >>> is_dictionary_standard(in1)
    True
    >>> in2 = {}
    >>> is_dictionary_standard(in2)
    False
    >>> in3 = {32: [[], [38, 44, 42, 28, 29, 45]], 33: [[], [38, 44, 42, 28, 29, 45]], 35: [[], [38, 44, 42, 28, 29, 45]], 36: [[], [38, 44, 42, 28, 29, 45]]}
    >>> is_dictionary_standard(in3)
    """
    assert type(input) is dict, "input is not dictionary"
    if input == {}: return False
    for value in input.values():
        if not is_standard(value): return False
    return True

def is_standard(input):
    """
    >>> in0 = [[], [38, 44, 42, 28, 29, 45]]
    >>> is_standard(in0)
    True
    >>> in1 = [[-2,-1],[]]
    >>> is_standard(in1)
    True
    >>> input = [[-2,1,3,4],[5,6,7]]
    >>> is_standard(input)
    True
    >>> input = [[1,2,3,4],[5,6,7]]
    >>> is_standard(input)
    True
    >>> input = [[1,2,3]]
    >>> is_standard(input)
    False
    >>> input = set([1,2,3])
    >>> is_standard(input)
    False
    >>> input = [[4,3,2,1],[7,6,5]]
    >>> is_standard(input)
    False
    >>> input = [[1,1,2,3,4],[5,6,7]]
    >>> is_standard(input)
    False
    >>> input = [[],[]]
    >>> is_standard(input)
    True
    """
    if type(input) is not list: return False
    if len(input) != 2: return False
    if type(input[0]) is not list or type(input[1]) is not list: return False
    if input == [[],[]]: return True
    if input[0] == []:
        for i in input[1]:
            if type(i) not in [long, int]: return False
        return True
    if input[1] == []:
        for i in input[0]:
            if type(i) not in [long, int]: return False
        return True
    for i in input[0]:
        if type(i) not in [long, int]: return False
    for i in input[1]:
        if type(i) not in [long, int]: return False
    if sorted(input[0]) != input[0] or sorted(input[1]) != input[1]: return False
    if len(set(input[0])) != len(input[0]) or len(set(input[1])) != len(input[1]): return False
    return True

def add_standards(in1, in2):
    """

    >>> in1 = [[1,2,3],[4,5,6]]
    >>> in2 = [[2,3,4],[6,7,8]]
    >>> r = add_standards(in1, in2)
    >>> r == [[1,2,3,4],[4,5,6,7,8]]
    True
    """
    assert is_standard(in1) and is_standard(in2), "in1(%s) and in2(%s)" % (in1, in2)
    singles = sorted(list(set(in1[0]) | set(in2[0])))
    aggrs = sorted(list(set(in1[1]) | set(in2[1])))
    return [singles, aggrs]

if __name__ == "__main__":
    import doctest
    doctest.testmod()