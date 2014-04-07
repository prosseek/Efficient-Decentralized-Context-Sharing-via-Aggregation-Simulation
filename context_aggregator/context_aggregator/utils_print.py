from utils_sort import *

def context_set_to_sting_with_missing_numbers(set_of_numbers):
    """

    >>> i = [1,4,6]
    >>> print context_set_to_sting_with_missing_numbers(i)
    [1,4,6:2,3,5]
    >>> i = [1,4]
    >>> print context_set_to_sting_with_missing_numbers(i)
    [1,4:2,3]
    """
    mx = max(set_of_numbers)
    mn = min(set_of_numbers)
    missing = []
    for i in range(mn+1,mx+1):
        if i not in set_of_numbers:
            str(missing.append(str(i)))
    if len(missing) == 0:
        missing_string = ""
    elif len(missing) == 1:
        missing_string = str(missing[0])
    else:
        missing_string = (",".join(missing))
    existing_string = ",".join(str(c) for c in set_of_numbers)

    return "[" + existing_string + ":" + missing_string + "]"

def context_set_to_string(set_of_contexts, display_mode=0):
    """
    We assume that the contexts are all singles or all aggregates

    display mode 0 shows
    [(10.00,[1],4,5)(10.00,[2],4,5)] <-- single
    [(10.00,[1,3,4],-1,5)(10.00,[2,3,4],-1,5)] <-- aggregate

    display mode -1 shows simpler
    [1,2] <-- single
    [1,3,4][2,3,4] <-- aggregates

    display mode 1 shows the missing member in the group
    [1,2] <-- single
    [1,3,4:2][2,3,4:1] <-- aggregates

    >>> singles = set([Context(value=10,cohorts=[1],timestamp=5,hopcount=4),Context(value=10,cohorts=[3],timestamp=5,hopcount=4)])
    >>> aggregates = set([Context(value=10,cohorts=[1,3,4],timestamp=5,hopcount=-1),Context(value=10,cohorts=[2,3],timestamp=5,hopcount=-1)])
    >>> print context_set_to_string(singles)
    [(10.00,[1],4,5)(10.00,[3],4,5)]
    >>> print context_set_to_string(aggregates)
    [(10.00,[1,3,4],-1,5)(10.00,[2,3],-1,5)]
    >>> print context_set_to_string(singles,display_mode=-1)
    [1,3]
    >>> print context_set_to_string(aggregates,display_mode=-1)
    [1,3,4][2,3]
    >>> print context_set_to_string(singles,display_mode=1)
    [1,3:2]
    >>> print context_set_to_string(aggregates,display_mode=1)
    [1,3,4:2][2,3:]
    >>> ag = {Context(24.83,[28,29,30],-1,0),Context(25.08,[28,29,30,40,43],-1,0),Context(25.10,[26,27,28,29,30],-1,0)}
    >>> print context_set_to_string(ag)
    [(25.10,[26,27,28,29,30],0,-1)(25.08,[28,29,30,40,43],0,-1)(24.83,[28,29,30],0,-1)]
    """
    if not set_of_contexts:
        return "[]"

    if list(set_of_contexts)[0].is_single():
        single_mode = True
    else:
        single_mode = False

    if single_mode:
        set_of_contexts = sort_singles(set_of_contexts)
    else:
        set_of_contexts = sort_aggregates(set_of_contexts)

    if display_mode == 0:
        c_string = "[" + "".join([c.to_string(True) for c in set_of_contexts]) + "]"
        return c_string
    elif display_mode == -1:
        if single_mode:
            c_string = "[" + ",".join(str(list(c.get_cohorts_as_set())[0]) for c in set_of_contexts) + "]"
        else:
            c_string = "".join(str(sorted(list(c.get_cohorts_as_set()))).replace(" ","") for c in set_of_contexts)
        return c_string
    elif display_mode == 1:
        if single_mode:
            numbers = [list(c.get_cohorts_as_set())[0] for c in set_of_contexts]
            return context_set_to_sting_with_missing_numbers(numbers)
        else:
            aggregate_strings = []
            for c in set_of_contexts:
                r = context_set_to_sting_with_missing_numbers(c.get_cohorts_as_set())
                aggregate_strings.append(r)
            c_string = "".join(aggregate_strings)
        return c_string

def container_to_string(container, display_mode = 0):
    """
    display mode 0 shows
    [(10.00,[1],4,5)(10.00,[2],4,5)]
    [(10.00,[1,3,4],-1,5)(10.00,[2,3,4],-1,5)]

    display mode -1 shows simpler
    [1,2]
    [1,3,4][2,3,4]

    display mode 1 shows the missing member in the group
    [1,2]
    [1,3,4:2][2,3,4:1]


    >>> class Container(object):
    ...     def __init__(self):self.singles = set();self.aggregates = set()
    ...
    >>> c = Container()
    >>> c.singles = set([Context(value=10,cohorts=[1],timestamp=5,hopcount=4),Context(value=10,cohorts=[2],timestamp=5,hopcount=4)])
    >>> c.aggregates = set([Context(value=10,cohorts=[1,3,4],timestamp=5,hopcount=-1),Context(value=10,cohorts=[2,3],timestamp=5,hopcount=-1)])
    >>> print container_to_string(c)
    [(10.00,[1],4,5)(10.00,[2],4,5)]
    [(10.00,[1,3,4],-1,5)(10.00,[2,3],-1,5)]
    >>> print container_to_string(c,-1)
    [1,2]
    [1,3,4][2,3]
    >>> print container_to_string(c,1)
    [1,2:]
    [1,3,4:2][2,3:]
    """

    s = context_set_to_string(container.singles, display_mode=display_mode)
    a = context_set_to_string(container.aggregates, display_mode=display_mode)

    return s + "\n" + a
