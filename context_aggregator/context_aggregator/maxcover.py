"""maximum cover algorithm

The interface is `run() method` with

* input of a set of aggregate contexts
* output of a set of selected contexts

    if non_primes:
        m = MaxCover()
        selected_non_primes = m.run(non_primes)

1. As a result, there should a format from/to a set of contexts to the
data structure that we use for solving the problem.
2. The run() is the inner method that actually solves the problem.

"""

from copy import *
from collections import OrderedDict

from utils_same import same
from context.context import Context
from utils_standard import aggregated_contexts_to_list_of_standard

class MaxCover(object):
    def __init__(self):
        self.solutionResults = []
        self.conversion_dictionary = {}
        self.results_in_list = []
    #
    # API
    #

    def run(self, non_primes, previous_selection=set()):
        self.conversion_dictionary = MaxCover.make_conversion_dictionary(non_primes)
        # The solver problem consists of only lists.
        inputs = map(list, self.conversion_dictionary.keys())
        if previous_selection is not None:
            previous_selection = aggregated_contexts_to_list_of_standard(previous_selection)
        results_in_list = self.solve(inputs, previous_selection)

        results = []

        for r in results_in_list:
            result = []
            for i in r:
                result.append(self.conversion_dictionary[frozenset(i)])
            results.append(result)
        # We need to return a list of results
        return results

    ########################################

    #
    # Converter from/to set of aggregated contexts
    #

    @staticmethod
    def make_conversion_dictionary(non_primes):
        """

        >>> np = {Context(value=1.0, cohorts={1,2,3}), Context(value=1.0, cohorts={3,4,5})}
        >>> r = MaxCover.make_conversion_dictionary(np)
        >>> same(r[frozenset([3,1,2])], Context(value=1.0, cohorts={1,2,3}))
        True
        >>> same(r[frozenset([3,5,4])], Context(value=1.0, cohorts={5,4,3}))
        True
        """
        result = {}
        for np in non_primes:
            key = frozenset(np.get_cohorts_as_set())
            result[key] = np
        return result

    @staticmethod
    def create_universe(X):
        """
        >>> d = [[1, 2, 3],[3, 4],[4, 5, 6]]
        >>> result = MaxCover.create_universe(d)
        >>> set([1,2,3,4,5,6]) == set(result)
        True
        """

        universe = set()
        for value in X:
            universe |= set(value)
        return list(universe)

    @staticmethod
    def length_of_total_elements(X):
        """
        >>> X = [[1, 2, 3], [3, 4], [4, 5, 6]]
        >>> l = MaxCover.length_of_total_elements(X)
        >>> l == 6
        True
        """

        set_result = set()

        for e in X:
            set_result |= set(e)

        return len(set(set_result))

    @staticmethod
    def find_friend_enemy(X, i):
        """Friend of X -> the set of lists that is not share elements with X
        Enemy of X -> the set of lists that shares elements with X

        >>> X = [[1, 2, 3], [3, 4], [4, 5, 6]]
        >>> friend, enemy = MaxCover.find_friend_enemy(X, [1,2,3])
        >>> friend == [[4,5,6]]
        True
        >>> enemy == [[3,4]]
        True

        >>> friend, enemy = MaxCover.find_friend_enemy(X, [3,4])
        >>> friend == []
        True
        >>> same(enemy,[[1,2,3],[4,5,6]])
        True

        >>> friend, enemy = MaxCover.find_friend_enemy(X, [4,5,6])
        >>> friend == [[1,2,3]]
        True
        >>> enemy == [[3,4]]
        True
        """

        enemy = []
        friend = []
        set_i = set(i)
        for j in X:
            if i == j: continue
            if set(j).isdisjoint(set_i):
                # if there is an intersection, it's an enemy
                friend.append(j)
            else:
                enemy.append(j)
        return friend, enemy

    def solve(self):
        raise RuntimeError("MaxCover solve() was not supposed to run, you should inherit the class and implement the algorithm")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
