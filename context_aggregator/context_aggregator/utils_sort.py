#
# sort utilities
#

from context.context import Context

def sort_singles(contexts):
    """
    Sort a set of single contexts into a list

    >>> i = {Context(value=10,cohorts=[3],timestamp=5,hopcount=4),Context(value=10,cohorts=[1],timestamp=5,hopcount=4),Context(value=10,cohorts=[2],timestamp=5,hopcount=4)}
    >>> r =sort_singles(i)
    >>> list(r[0].get_cohorts_as_set())[0] == 1 and list(r[1].get_cohorts_as_set())[0] == 2 and list(r[2].get_cohorts_as_set())[0] == 3
    True
    """
    #return sorted(list(contexts), key=lambda c: list(c.get_cohorts_as_set())[0])
    return sorted(list(contexts), key=lambda c: c.get_id())

def sort_aggregates(contexts):
    """
    Sort a set of single contexts into a list

    >>> i = {Context(value=10,cohorts=[1,3],timestamp=5,hopcount=4),Context(value=10,cohorts=[1,2,3],timestamp=5),Context(value=10,cohorts=[1,3,2,6,7],timestamp=5)}
    >>> r =sort_aggregates(i)
    >>> sorted(list(r[0].get_cohorts_as_set())) == [1, 2, 3, 6, 7] and sorted(list(r[1].get_cohorts_as_set())) == [1, 2, 3]
    True
    >>> print r[0],r[1],r[2]
    v(10.00):c([1,2,3,6,7]):h(0):t(5) v(10.00):c([1,2,3]):h(0):t(5) v(10.00):c([1,3]):h(4):t(5)
    """
    return sorted(list(contexts), key=len, reverse=True)

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



if __name__ == "__main__": # and __package__ is None:
    import doctest
    doctest.testmod()