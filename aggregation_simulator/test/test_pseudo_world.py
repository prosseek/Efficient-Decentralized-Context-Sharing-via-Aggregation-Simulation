import unittest
import sys

from utils import *

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

pseudo30 = "pseudo_realworld_30"
pseudo50 = "pseudo_realworld_50"
disconnection_rate = 0.0
drop_rate = 0.0

simulation_root_dir = get_configuration("config.cfg", "TestDirectory", "pseudo_test_root_dir")

test_name = "pseudo_realworld_30"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path30 = os.path.join(d, test_name + ".txt")
sample_file_path30=os.path.join(d, test_name + ".sample.txt")
test_name = "pseudo_realworld_50"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path50 = os.path.join(d, test_name + ".txt")
sample_file_path50=os.path.join(d, test_name + ".sample.txt")
test_name = "pseudo_realworld_100"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path100 = os.path.join(d, test_name + ".txt")
sample_file_path100=os.path.join(d, test_name + ".sample.txt")
test_name = "pseudo_realworld_100_2d"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path100_2d = os.path.join(d, test_name + ".txt")
sample_file_path100_2d = os.path.join(d, test_name + ".sample.txt")
test_name = "pseudo_realworld_49_tree"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path49tree = os.path.join(d, test_name + ".txt")
sample_file_path49tree=os.path.join(d, test_name + ".sample.txt")
test_name = "pseudo_realworld_49"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path49 = os.path.join(d, test_name + ".txt")
sample_file_path49=os.path.join(d, test_name + ".sample.txt")
test_name = "pseudo_realworld_49_2d"
d = os.path.join(get_test_files_directory(), test_name)
network_file_path49_2d = os.path.join(d, test_name + ".txt")
sample_file_path49_2d = os.path.join(d, test_name + ".sample.txt")

class TestPseudoWorld(unittest.TestCase):
    def setUp(self):
        pass

    def test_pseudo30_th5_aggregates(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path30,
            "sample_file_path":sample_file_path30,
            "condition":"th5",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":20
        }
        return runit(**params)

    def test_pseudo50_th5_aggregates(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path50,
            "sample_file_path":sample_file_path50,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":20
        }
        return runit(**params)

    # real world 6m
    def test_pseudo30_singles(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path30,
            "sample_file_path":sample_file_path30,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    # *****************************
    def test_pseudo30_aggregates(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path30,
            "sample_file_path":sample_file_path30,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo50_singles(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path50,
            "sample_file_path":sample_file_path50,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo50_aggregates(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path50,
            "sample_file_path":sample_file_path50,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)


    # ***********************
    def test_pseudo100_singles(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path100,
            "sample_file_path":sample_file_path100,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo100_aggregates(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path100,
            "sample_file_path":sample_file_path100,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo100_2d_singles(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path100_2d,
            "sample_file_path":sample_file_path100_2d,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo100_2d_aggregates(self):
        test_name = "pseudo_realworld_100_2d"
        d = os.path.join(get_test_files_directory(), test_name)
        network_file_path70_2d = os.path.join(d, test_name + ".txt")
        sample_file_path70_2d = os.path.join(d, test_name + ".sample.txt")

        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path100_2d,
            "sample_file_path":sample_file_path100_2d,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    # 49 ##############################
    # ***********************
    def test_pseudo49_singles(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path49,
            "sample_file_path":sample_file_path49,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo49_aggregates(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path49,
            "sample_file_path":sample_file_path49,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo49_2d_singles(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path49_2d,
            "sample_file_path":sample_file_path49_2d,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo49_2d_aggregates(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path49_2d,
            "sample_file_path":sample_file_path49_2d,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo49_tree_singles(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path49tree,
            "sample_file_path":sample_file_path49tree,
            "condition":"normal",
            "test_sub_name":"singles",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

    def test_pseudo49_tree_aggregates(self):
        params = {
            "simulation_root_dir":simulation_root_dir,
            "network_file_path":network_file_path49tree,
            "sample_file_path":sample_file_path49tree,
            "condition":"normal",
            "test_sub_name":"aggregates",
            "disconnection_rate":0.0,
            "drop_rate":0.0,
            "threshold":sys.maxint
        }
        return runit(**params)

if __name__ == "__main__":
    unittest.main(verbosity=2)