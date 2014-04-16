import unittest
import sys
import os
import pprint

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../helper_programs"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from utils import *
from tree_analyzer import *

class TestTreeAnalyzer(unittest.TestCase):

    def setUp(self):
        pass

    def get_avg(self, directory):
        d = get_configuration("config.cfg", "TestDirectory", directory)
        dtree = d + os.sep + "tree"
        dmesh = d + os.sep + "mesh"
        r_tree = []
        r_mesh = []
        for i in range(10, 110, 10):
            r = get_average_neighbors_size(directory=dtree, node=i)
            r_tree.append(r[0])

        for i in range(10, 110, 10):
            r = get_average_neighbors_size(directory=dmesh, node=i)
            r_mesh.append(r[0])

        return r_tree, r_mesh

    def test_tree_analyzer(self):
        pprint.pprint(self.get_avg("less_dense_10_100_dir"))
        pprint.pprint(self.get_avg("more_dense_10_100_dir"))