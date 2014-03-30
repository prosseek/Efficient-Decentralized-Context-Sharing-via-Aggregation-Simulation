import operator

from maxcover import MaxCover
from context.context import Context
from utils_same import same

class GreedyMaxCover(MaxCover):
    @staticmethod
    def _solve(lists, selected_paths):
        """
        >>> x = [[3,4,5], [5,6]]
        >>> r = []
        >>> GreedyMaxCover._solve(x, r)
        >>> same(r, [[3,4,5]])
        True
        >>> x = [[1,2,3],[3,4],[4,5,6]]
        >>> r = []
        >>> GreedyMaxCover._solve(x, r)
        >>> same(r, [[4,5,6],[1,2,3]])
        True
        """
        if not lists:
            return
        else:
            l = GreedyMaxCover.get_list_with_maximum_friends(lists)
            selected_paths.append(l)
            l = GreedyMaxCover.remove_itself_and_enemies(lists, l)
            GreedyMaxCover._solve(l, selected_paths)

    @staticmethod
    def remove_itself_and_enemies(lists, l):
        """
        >>> x = [[1,2,3],[3,4],[4,5,6],[6,7,8,9]]
        >>> GreedyMaxCover.remove_itself_and_enemies(x,[1,2,3]) == [[4,5,6],[6,7,8,9]]
        True
        """
        f,e = MaxCover.find_friend_enemy(lists,l)
        result = []
        for i in lists:
            if i == l or i in e: continue
            result.append(i)
        return result

    @staticmethod
    def get_list_with_maximum_friends(lists):
        """
        >>> x = [[1,2,3],[3,4],[4,5,6],[6,7,8,9]]
        >>> GreedyMaxCover.get_list_with_maximum_friends(x) == [1,2,3]
        True
        """
        result = {}
        for i,l in enumerate(lists):
            friend, enemy = MaxCover.find_friend_enemy(lists, l)
            f = MaxCover.length_of_total_elements(friend)
            e = MaxCover.length_of_total_elements(enemy)
            result[i] = f - e

        #print result
        r = sorted(result.iteritems(), key=operator.itemgetter(1), reverse=True)
        #print r
        return lists[r[0][0]]

    def solve(self, lists):
        """
        >>> x = {Context(value=1.0, cohorts={1,2,3}), Context(value=2.0, cohorts={2,3,4})}
        >>> m = GreedyMaxCover()
        >>> r = m.run(x) # Silent the result
        >>> r = m.results_in_list
        >>> r == [[1,2,3]] or r == [[2,3,4]]
        True
        """
        result = []
        GreedyMaxCover._solve(lists, result)
        return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()