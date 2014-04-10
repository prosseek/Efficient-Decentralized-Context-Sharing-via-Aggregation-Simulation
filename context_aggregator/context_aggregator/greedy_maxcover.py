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

    @staticmethod
    def get_selection_from_previous_results(lists, previous_selection):
        """

        >>> previous_selection = [[17, 18, 19], [8, 10, 11, 13], [9, 12, 14, 48, 49, 50, 51, 52, 53, 54]]
        >>> lists = [[18, 19], [47, 48], [8, 10, 11, 13], [8, 9, 10, 11, 52, 53, 54], [9, 14, 15, 16, 52, 53, 54], [9, 12, 14, 15, 18, 52, 53], [9, 12, 14, 48, 49, 50, 51, 52, 53, 54]]
        >>> same(GreedyMaxCover.get_selection_from_previous_results(lists, previous_selection), [[8, 10, 11, 13], [9, 12, 14, 48, 49, 50, 51, 52, 53, 54], [18, 19]])
        True
        """
        prev_set = map(frozenset, previous_selection)
        current_set = map(frozenset, lists)

        # find the one selected from previous choice
        selected = []
        for i in prev_set:
            if i in current_set:
                selected.append(sorted(list(i)))
        for i in selected:
            lists = GreedyMaxCover.remove_itself_and_enemies(lists, i)

        # get the candidates from the rest
        result = []
        GreedyMaxCover._solve(lists, result)
        selected += result

        return selected

    @staticmethod
    def _solve_from_size(lists, selected_paths):
        # get the largest element
        if not lists:
            return
        else:
            sorted_list = sorted(lists, key=lambda e: (-len(e), e))
            l = sorted_list[0]
            selected_paths.append(l)
            l = GreedyMaxCover.remove_itself_and_enemies(lists, l)
            GreedyMaxCover._solve_from_size(l, selected_paths)

    def solve(self, lists, previous_selection=set()):
        """
        >>> x = {Context(value=1.0, cohorts={1,2,3}), Context(value=2.0, cohorts={2,3,4})}
        >>> m = GreedyMaxCover()
        >>> r = m.run(x) # Silent the result
        >>> r = m.results_in_list
        >>> r == [[1,2,3]] or r == [[2,3,4]]
        True
        """
        result1 = []
        GreedyMaxCover._solve(lists, result1)
        size1 = MaxCover.length_of_total_elements(result1)
        size2 = -1
        result2 = []

        if previous_selection:
           result2 = GreedyMaxCover.get_selection_from_previous_results(lists, previous_selection)
           size2 = MaxCover.length_of_total_elements(result2)

        result3 = []
        GreedyMaxCover._solve_from_size(lists, result3)
        size3 = MaxCover.length_of_total_elements(result3)

        # Find the distinct set of possible selections

        if size1 > size2:
            if size1 > size3: return [result1]
            else: return [result3]
        else:
            if size2 > size3: return [result2]
            else: return [result3]

if __name__ == "__main__":
    import doctest
    doctest.testmod()