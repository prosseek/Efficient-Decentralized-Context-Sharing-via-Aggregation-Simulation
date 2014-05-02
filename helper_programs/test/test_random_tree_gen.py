import unittest
import sys
import os
import pprint

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../helper_programs"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from utils import *
from random_tree_gen import *

class TestRandomTreeGen(unittest.TestCase):

    def setUp(self):
        pass

    def test_random(self):
        r = RandomTreeGen()
        for i in range(10, 101, 10):
            name = "tree_%d_" % i
            #print name
            r.mass_gen(total_size=100, node_size=i, directory="/Users/smcho/Desktop/res", name=name)

