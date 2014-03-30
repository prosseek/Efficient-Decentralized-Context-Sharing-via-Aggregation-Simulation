import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.brutal_force_maxcover import BrutalForceMaxCover
from utils import *
from context_aggregator.utils_same import *

class TestBrutalForceMaxcover(unittest.TestCase):

    def setUp(self):
        self.X = {
            'A': [1, 2, 3],
            'B': [3, 4],
            'C': [4, 5, 6]
        }
        self.m = BrutalForceMaxCover()
        
    def test_findFriendEnemy(self):
        X = {
            'A': [1, 2],
            'B': [2, 3, 4],
            'C': [3,4,5,8],
            'D': [5,6,7],
            'E': [7,8]
        }
        m = BrutalForceMaxCover()
        friend, enemy = m.find_friend_enemy(X, 'A')
        self.assertTrue(same(friend, set(['C','D','E'])))
        self.assertTrue(same(enemy, set(['B'])))
        
        friend, enemy = m.find_friend_enemy(X, 'B')
        self.assertTrue(same(friend, set(['D','E'])))
        self.assertTrue(same(enemy, set(['A','C'])))
        
        friend, enemy = m.find_friend_enemy(X, 'C')
        self.assertTrue(same(friend, set(['A'])))
        self.assertTrue(same(enemy, set(['B','D','E'])))
        
        friend, enemy = m.find_friend_enemy(X, 'D')
        self.assertTrue(same(friend, set(['A','B'])))
        self.assertTrue(same(enemy, set(['C','E'])))
        
        friend, enemy = m.find_friend_enemy(X, 'E')
        self.assertTrue(same(friend, set(['A','B'])))
        self.assertTrue(same(enemy, set(['C','D'])))
        
    def test_solve2(self):
        X = {
            'A': [1, 2],
            'B': [2, 3, 4],
            'C': [3,4,5,8],
            'D': [5,6,7],
            'E': [7,8]
        }
            
        ec = BrutalForceMaxCover()
        result = ec.solve(X)
        #print "r", result
        expected1 = ['A','C']
        expected2 = ['B','D']
        #print result
        self.assertTrue(same(result, expected1) or same(result, expected2))
        
    def test_solve3(self):
        X = {0: [1, 2], 1: [2, 3, 4], 2: [8, 3, 4, 5], 3: [5, 6, 7], 4: [8, 7]}
        ec = BrutalForceMaxCover()
        result = ec.solve(X)
        #print result
        expected1 = [2,0]
        expected2 = [1,3]
        # print expected
        # print result
    #    TODO Something's wrong here
    #    self.assertTrue(same(result, expected1) or same(result,expected2))
    #     
    def test_solve4(self): # for debugging in random15
        X = {0: [0, 6, 12], 1: [4,5,7,8], 2: [4,5,6,13], 3: [3,5,12,13], 4: [5,6,7,8,13]}
        ec = BrutalForceMaxCover()
        result = ec.solve(X)
        #print result
        expected = [0,1]
        self.assertTrue(same(result, expected))   
        
    def test_solve5(self): # for debugging in random15
        X = {0: [0,1], 1:[2,3], 2:[2,4], 3:[1,2,3,4]}
        ec = BrutalForceMaxCover()
        result = ec.solve(X)
        #print result
        expected1 = [0,1]
        expected2 = [0,2]
        expected3 = [3]
        #print result
        #print result
        # print result
        # print expected3
        # print same(result, expected3)
        self.assertTrue(same(result, expected1) or same(result,expected2) or same(result, expected3))   
    
    def test_cover(self):
        X = {1, 2, 3, 4, 5, 6, 7}
        Y = {
            'A': [1, 4, 7],
            'B': [1, 4],
            'C': [4, 5, 7],
            'D': [3, 5, 6],
            'E': [2, 3, 6, 7],
            'F': [2, 7]}
        ec = BrutalForceMaxCover()
        result = ec.solve(Y)
        expected = ['B','F','D']
        self.assertTrue(same(result, expected))
        
    def test_cover2(self):
        X = {1, 2, 3, 4}
        Y = {
            1: [1, 2],
            2: [2, 3],
            3: [3, 4],
            4: [4, 1]}
        ec = BrutalForceMaxCover()
        result = ec.solve(Y)
        expect1 = [1,3]
        expect2 = [2,4]
        ## FIX THIS
        #self.assertTrue(same(result, expect1) or same(result, expect2))

if __name__ == "__main__":
    unittest.main(verbosity=2)