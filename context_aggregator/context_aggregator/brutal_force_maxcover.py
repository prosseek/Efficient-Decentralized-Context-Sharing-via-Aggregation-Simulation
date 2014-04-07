"""maximum cover algorithm"""

from copy import *
from collections import OrderedDict
from utils import *

class BrutalForceMaxCover(object):
    def __init__(self): 
        self.solutionResults = []

    def create_universe(self, X):
        """
        >>> d = {'A': [1, 2, 3], 'B': [3, 4], 'C': [4, 5, 6]}
        >>> result = BrutalForceMaxCover().create_universe(d)
        >>> set([1,2,3,4,5,6]) == set(result)
        True
        """

        universe = set()
        for value in X.values():
            universe |= set(value)
        return list(universe)

    def find_maximum(self, d):
        """Given a dictionary d, find the key and length of the key

        >>> m = BrutalForceMaxCover()
        >>> X = { 'A': [1, 2, 3], 'B': [3, 4], 'C': [4, 5, 6, 7, 8, 9, 10]}

        #universe = self.m.createUniverse(X)
        >>> key, value = m.find_maximum(X)
        >>> key == 'C' and value == len(X['C'])
        True

        >>> X = {0: [0, 6, 12], 1: [4, 5, 7, 8], 2: [4, 5, 6, 13], 3: [3, 5, 12, 13], 4: [5, 6, 7, 8, 13]}
        >>> key, value = m.find_maximum(X)
        >>> key == 4 and value == len(X[4])
        True
        """

        # sort the dictionary based on the length of the element
        result = OrderedDict(sorted(d.items(), key=lambda t: len(t[1]), reverse=True))
        maximum = result.items()[0] # 0th item is the one with largest element
        return maximum[0], len(maximum[1])


    def find_friend_enemy(self, X, i):
        """Friend of X -> the set of lists that is not share elements with X
        Enemy of X -> the set of lists that shares elements with X

        >>> X = {'A': [1, 2, 3], 'B': [3, 4], 'C': [4, 5, 6]}
        >>> m = BrutalForceMaxCover()
        >>> friend, enemy = m.find_friend_enemy(X, 'A')
        >>> friend == set(['C'])
        True
        >>> enemy == set(['B'])
        True

        >>> friend, enemy = m.find_friend_enemy(X, 'B')
        >>> friend == set([])
        True
        >>> enemy == set(['A','C'])
        True

        >>> friend, enemy = m.find_friend_enemy(X, 'C')
        >>> friend == set(['A'])
        True
        >>> enemy == set(['B'])
        True
        """

        # Don't spoil the input data
        X = copy(X)
        # 1. select the item in a dictionary
        temp = X[i]
        del X[i]

        # We use set in order not to allow the duplicates
        temp_set = set(temp)
        friend_set = set()
        enemy_set = set()

        # j is a key
        for j in X:
            # j_set is a value in a set
            j_set = set(X[j])
            if temp_set & j_set == set([]):
                # if there is an intersection, it's an enemy
                friend_set.add(j)
            else:
                enemy_set.add(j)
            
        return friend_set, enemy_set


    def length_of_total_elements(self, path, X):
        """
        >>> m = BrutalForceMaxCover()
        >>> X = {'A': [1, 2, 3], 'B': [3, 4], 'C': [4, 5, 6]}
        >>> l = m.length_of_total_elements(['A','C'], X)
        >>> l == 6
        True
        >>> l = m.length_of_total_elements(['A','B'], X)
        >>> l == -2
        True
        """

        set_length = set()
        list_length = list()

        for p in path:
            list_length += X[p]

        if len(list_length) == len(set(list_length)): return len(list_length)
        return -2 # Duplication exists, no meaning of path, -2 because initial max value is -1

    def solve_list_input(self, all_lists):
        """
        >>> x = [[1,2,3],[3,4],[4,5,6]]
        >>> ec = BrutalForceMaxCover()
        >>> ec.solve_list_input(x) == [[1,2,3],[4,5,6]]
        True
        """
        result = {}
        for list in all_lists:
            key = str(list)
            result[key] = list
        r = self.solve(result)

        final_result = []
        for key in r:
            final_result.append(result[key])
        return final_result

    def solve(self, all_dictionary):
        """
        >>> X = {'A': [1, 2, 3], 'B': [3, 4], 'C': [4, 5, 6]}
        >>> ec = BrutalForceMaxCover()
        >>> result = ec.solve(X)
        >>> set(result) == set(['A','C'])
        True
        """

        Xp = copy(all_dictionary)
        path = []
        results = []
        self._solve(Xp.keys(), Xp, path, results)

        # results has all the path information, from the results, find the maximum path
        max_length = -1
        max_path = None
        for path in results:
            pathLength = self.length_of_total_elements(path, all_dictionary)
            if pathLength > max_length:
                max_length = pathLength
                max_path = path

        return max_path

    def run(self, non_primes): # all_dictionary):
        all_dictionary, map_contexts = get_maxcover_dictionary(non_primes)
        max_path = self.solve(all_dictionary)
        result = set()
        for i in max_path:
            result.add(map_contexts[i])
        return result

    def _solve(self, keys, world_dictionary, cover, covers):
        """It's the inner method for finding **all** paths that gives any kind of cover
        Input: keys
               world_dictionary

        Output: cover
                covers <-- This has all the path information

        The covers include paths starting from each key iteratively
        [['A', 'C']]
        [['A', 'C'], ['C', 'A']]
        [['A', 'C'], ['C', 'A'], ['B']]

        >>> X = {'A': [1, 2, 3], 'B': [3, 4], 'C': [4, 5, 6]}
        >>> ec = BrutalForceMaxCover()
        >>> path = []
        >>> results = []
        >>> result = ec._solve(X.keys(), X, path, results)
        >>> set(map(frozenset,results)) == set(map(frozenset,[['A', 'C'], ['C', 'A'], ['B']]))
        True
        """
        if len(keys) == 0:
            p = copy(cover)
            covers.append(p)
            return
        for key in keys:
            # X is a whole dictionary, we need to copy as X is modified
            Xp = copy(world_dictionary)
            friend_key_set, enemy_key_set = self.find_friend_enemy(Xp, key)
            # Remove the key
            del Xp[key]
            # Remove all of the enemy set
            for e in enemy_key_set:
                del Xp[e]

            cover.append(key) # push the key as this key covered the path
            self._solve(friend_key_set, Xp, cover, covers)
            # It's different path, so the appended key should be removed
            cover.pop() # pop the key


if __name__ == "__main__":
    import doctest
    doctest.testmod()
