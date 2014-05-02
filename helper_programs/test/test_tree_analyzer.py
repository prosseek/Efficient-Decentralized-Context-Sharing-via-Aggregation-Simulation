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

    def test_avg_for_simulation(self):
        d = get_configuration("config.cfg", "TestDirectory", "test_files_directory")
        names = ["real_world_intel_6_tree", "real_world_intel_6", "real_world_intel_10"
                 ,"pseudo_realworld_49_tree","pseudo_realworld_49_2d","pseudo_realworld_49"
                 ,"pseudo_realworld_100_2d", "pseudo_realworld_100"]

        for n in names:
            print "process - %s" % n
            filepath = d + os.sep + n + os.sep + n + ".txt"
            network = Network(filepath)
            print network.get_average_neighbor_size()

    def atest_tree_analyzer(self):
        pprint.pprint(self.get_avg("less_dense_10_100_dir"))
        pprint.pprint(self.get_avg("more_dense_10_100_dir"))