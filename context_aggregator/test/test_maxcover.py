import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.brutal_force_maxcover import BrutalForceMaxCover
from context_aggregator.greedy_maxcover import GreedyMaxCover
from context_aggregator.maxcover import MaxCover
from utils import *
from context_aggregator.utils_same import *


world1 = [[47, 48], [37, 39], [24, 46], [48, 54], [15, 18], [30, 37], [38, 40], [20, 21, 22], [9, 11, 54],
         [32, 34, 36], [13, 14, 16, 19],[8, 10, 11, 13], [8, 10, 52, 53], [11, 13, 49, 50, 51],
         [30, 34, 36, 41, 43], [9, 12, 14, 52, 53], [49, 50, 51, 52, 53], [26, 27, 28, 30, 41, 43],
         [24, 26, 27, 28, 30, 38], [26, 27, 28, 30, 32, 34], [12, 13, 14, 48, 49, 50, 51],
         [18, 19, 24, 26, 27, 28, 30], [21, 22, 24, 26, 27, 28, 30, 39]]
selection1 = [[15, 18], [24, 46], [37, 39], [47, 48], [38, 40], [9, 11, 54], [32, 34, 36], [20, 21, 22], [13, 14, 16, 19], [49, 50, 51, 52, 53], [26, 27, 28, 30, 41, 43]]

class TestMaxcover(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_findFriendEnemy(self):
        X = [[1, 2],[2, 3, 4],[3,4,5,8],[5,6,7],[7,8]]
        m = MaxCover()
        friend, enemy = MaxCover.find_friend_enemy(X, [1,2])
        self.assertTrue(same(friend, [[3,4,5,8],[5,6,7],[7,8]]))
        self.assertTrue(same(enemy, [[2,3,4]]))
        
        friend, enemy = m.find_friend_enemy(X, [2,3,4])
        self.assertTrue(same(friend, [[5,6,7],[7,8]]))
        self.assertTrue(same(enemy, [[1,2],[3,4,5,8]]))

        friend, enemy = m.find_friend_enemy(X, [3,4,5,8])
        self.assertTrue(same(friend, [[1,2]]))
        self.assertTrue(same(enemy, [[5,6,7],[7,8],[2,3,4]]))

        friend, enemy = m.find_friend_enemy(X, [5,6,7])
        self.assertTrue(same(friend, [[1,2],[2,3,4]]))
        self.assertTrue(same(enemy, [[3,4,5,8],[7,8]]))

        friend, enemy = m.find_friend_enemy(X, [7,8])
        self.assertTrue(same(friend, [[1,2],[2,3,4]]))
        self.assertTrue(same(enemy, [[3,4,5,8],[5,6,7]]))

    def test_get_length(self):
        # print MaxCover.length_of_total_elements(world1)
        # 37
        self.assertTrue(len(MaxCover.create_universe(world1)) == MaxCover.length_of_total_elements(world1))

        # This is 34
        print MaxCover.length_of_total_elements(selection1)

    # def test_solve2(self):
    #     X = {
    #         'A': [1, 2],
    #         'B': [2, 3, 4],
    #         'C': [3,4,5,8],
    #         'D': [5,6,7],
    #         'E': [7,8]
    #     }
    #
    #     ec = MaxCover()
    #     result = ec.solve(X)
    #     #print "r", result
    #     expected1 = ['A','C']
    #     expected2 = ['B','D']
    #     #print result
    #     self.assertTrue(same(result, expected1) or same(result, expected2))
    #
    # def test_solve3(self):
    #     X = {0: [1, 2], 1: [2, 3, 4], 2: [8, 3, 4, 5], 3: [5, 6, 7], 4: [8, 7]}
    #     ec = MaxCover()
    #     result = ec.solve(X)
    #     #print result
    #     expected1 = [2,0]
    #     expected2 = [1,3]
    #     # print expected
    #     # print result
    # #    TODO Something's wrong here
    # #    self.assertTrue(same(result, expected1) or same(result,expected2))
    # #
    # def test_solve4(self): # for debugging in random15
    #     X = {0: [0, 6, 12], 1: [4,5,7,8], 2: [4,5,6,13], 3: [3,5,12,13], 4: [5,6,7,8,13]}
    #     ec = MaxCover()
    #     result = ec.solve(X)
    #     #print result
    #     expected = [0,1]
    #     self.assertTrue(same(result, expected))
    #
    # def test_solve5(self): # for debugging in random15
    #     X = {0: [0,1], 1:[2,3], 2:[2,4], 3:[1,2,3,4]}
    #     ec = MaxCover()
    #     result = ec.solve(X)
    #     #print result
    #     expected1 = [0,1]
    #     expected2 = [0,2]
    #     expected3 = [3]
    #     #print result
    #     #print result
    #     # print result
    #     # print expected3
    #     # print same(result, expected3)
    #     self.assertTrue(same(result, expected1) or same(result,expected2) or same(result, expected3))
    #
    # def test_cover(self):
    #     X = {1, 2, 3, 4, 5, 6, 7}
    #     Y = {
    #         'A': [1, 4, 7],
    #         'B': [1, 4],
    #         'C': [4, 5, 7],
    #         'D': [3, 5, 6],
    #         'E': [2, 3, 6, 7],
    #         'F': [2, 7]}
    #     ec = MaxCover()
    #     result = ec.solve(Y)
    #     expected = ['B','F','D']
    #     self.assertTrue(same(result, expected))
    #
    # def test_cover2(self):
    #     X = {1, 2, 3, 4}
    #     Y = {
    #         1: [1, 2],
    #         2: [2, 3],
    #         3: [3, 4],
    #         4: [4, 1]}
    #     ec = MaxCover()
    #     result = ec.solve(Y)
    #     expect1 = [1,3]
    #     expect2 = [2,4]
    #     ## FIX THIS
    #     #self.assertTrue(same(result, expect1) or same(result, expect2))

if __name__ == "__main__":
    unittest.main(verbosity=2)