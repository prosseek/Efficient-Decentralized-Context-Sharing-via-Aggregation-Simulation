import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from aggregation_simulator.utils_configuration import *
from aggregation_simulator.host import Host
from aggregation_simulator.aggregation_simulator import AggregationSimulator
from aggregation_simulator.utils import make_ready_for_test

from aggregation_simulator.network import Network
from context_aggregator.utils_same import same
from context_aggregator.context_aggregator import ContextAggregator


def get_test_network(condition, network_name):
    d = get_test_files_directory()
    network_file = os.path.join(d, "%s/%s/%s.txt" % (condition, network_name, network_name))
    network = Network()
    network.read(network_file)
    return network

class TestRealWorldDrop(unittest.TestCase):
    def setUp(self):
        pass

    def runit(self, condition, test_name, test_sub_name):
        network = get_test_network(condition, test_name)
        host_ids = network.get_host_ids() # [h0, h1, h2]
        hosts = []
        for h in host_ids:
            hosts.append(Host(h))
        neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

        test_directory, sample = make_ready_for_test(condition, test_name, test_sub_name)

        if test_sub_name.startswith("single"):
            propagation_mode = ContextAggregator.SINGLE_ONLY_MODE
        else:
            propagation_mode = ContextAggregator.AGGREGATION_MODE

        config = {"hosts":hosts, "neighbors":neighbors,\
                  "test_directory":test_directory, "sample":sample, \
                  ContextAggregator.PM:propagation_mode, "drop_rate":0.50}
        simulation = AggregationSimulator.run(config=config)

    def test_with_intel6_singles_only(self):
        return self.runit("normal", "real_world_intel_6_drop", "singles")

    def test_with_intel6_aggregate(self):
        return self.runit("normal", "real_world_intel_6_drop", "aggregates")

    def test_with_intel10_singles_only(self):
        return self.runit("normal", "real_world_intel_10_drop", "singles")

    def test_with_intel10_aggregate(self):
        return self.runit("normal", "real_world_intel_10_drop", "aggregates")

    def test_with_intel6_aggregate_marked_sample(self):
        return self.runit("marked_sample", "real_world_intel_6_drop", "aggregates")

    def test_with_intel10_aggregate_marked_sample(self):
        return self.runit("marked_sample", "real_world_intel_10_drop", "aggregates")


if __name__ == "__main__":
    unittest.main(verbosity=2)