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

class TestRealWorld(unittest.TestCase):
    def setUp(self):
        pass

    # real world 6m
    def test_with_intel6_singles_only(self):
        return runit("normal", real_world_6 , "singles", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

    def test_with_intel6_aggregate(self):
        return runit("normal", real_world_6, "aggregates", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

    # real world 10m
    def test_with_intel10_singles_only(self):
        return runit("normal", real_world_10, "singles", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

    def test_with_intel10_aggregate(self):
        return runit("normal", real_world_10, "aggregates", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

    # real world aggregate with mark 6/10m
    def test_with_intel6_aggregate_marked_sample(self):
        return runit("marked_sample", real_world_6, "aggregates", disconnection_rate=disconnection_rate,drop_rate=drop_rate)

    def test_with_intel10_aggregate_marked_sample(self):
        return runit("marked_sample", real_world_10, "aggregates", disconnection_rate=disconnection_rate,drop_rate=drop_rate)


if __name__ == "__main__":
    unittest.main(verbosity=2)