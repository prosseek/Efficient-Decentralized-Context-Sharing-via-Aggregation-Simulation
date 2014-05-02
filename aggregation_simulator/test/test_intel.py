import unittest
import sys

from utils import *

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

real_world_6 = "real_world_intel_6"
real_world_10 = "real_world_intel_10"
disconnection_rate = 0.0
drop_rate = 0.0

simulation_root_dir = get_configuration("config.cfg", "TestDirectory", "intel_test_root_dir")
test_name = "real_world_intel_6"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path6 = os.path.join(d, test_name + ".txt")
sample_file_path6=os.path.join(d, test_name + ".sample.txt")
test_name = "real_world_intel_10"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path10 = os.path.join(d, test_name + ".txt")
sample_file_path10=os.path.join(d, test_name + ".sample.txt")
test_name = "real_world_intel_6_tree"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path6tree = os.path.join(d, test_name + ".txt")
sample_file_path6tree=os.path.join(d, test_name + ".sample.txt")

class TestIntel(unittest.TestCase):
    def setUp(self):
        pass


    # real world 6m
    def test_with_intel_6_tree_singles_only(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path6tree,
            "sample_file_path":sample_file_path6tree,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    # *************************************
    def test_with_intel6_tree_aggregate(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path6tree,
            "sample_file_path":sample_file_path6tree,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    # real world 6m
    def test_with_intel6_singles_only(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path6,
            "sample_file_path":sample_file_path6,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    # *************************************
    def test_with_intel6_aggregate(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path6,
            "sample_file_path":sample_file_path6,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_with_intel6_aggregate_threshold(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path6,
            "sample_file_path":sample_file_path6,
            "condition":"threshold_5",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":5
        }
        return runit(**params)

    # real world 6m
    def test_with_intel10_singles_only(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path10,
            "sample_file_path":sample_file_path10,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_with_intel10_aggregate(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path10,
            "sample_file_path":sample_file_path10,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    # real world aggregate with mark 6/10m
    def test_with_intel6_aggregate_marked_sample(self):
        return runit("marked_sample", real_world_6, "aggregates", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

    def test_with_intel10_aggregate_marked_sample(self):
        return runit("marked_sample", real_world_10, "aggregates", disconnection_rate=disconnection_rate,drop_rate=drop_rate)


if __name__ == "__main__":
    unittest.main(verbosity=2)