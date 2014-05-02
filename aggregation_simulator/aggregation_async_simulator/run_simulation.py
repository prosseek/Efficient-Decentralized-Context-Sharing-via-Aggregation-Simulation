from aggregation_simulator.utils_configuration import *
from aggregation_simulator.network import Network
from context_aggregator.context_aggregator import ContextAggregator
from aggregation_simulator.host import Host
from aggregation_async_simulator import AggregationAsyncSimulator
from aggregation_simulator.run_simulation import make_ready_for_test

import warnings
import os
import shutil
import sys
import distutils.core

def run_simulation(network_dir, condition, test_sub_name, disconnection_rate=0.0, drop_rate=0.0, threshold=sys.maxint):
    """
    Network directory should contain network and sample files
    """
    test_name = os.path.basename(network_dir)
    print "%s - %s - %s disconnect(%4.2f) drop(%4.2f) threshold(%d)" % (network_dir, test_name, test_sub_name, disconnection_rate, drop_rate, threshold)
    network_file_path = os.path.join(network_dir, test_name + ".txt")
    assert os.path.exists(network_file_path), "No network file %s exists " % network_file_path
    sample_file_path = os.path.join(network_dir, test_name + ".sample.txt")
    assert os.path.exists(sample_file_path), "No network file %s exists " % sample_file_path

    network = Network(network_file_path)
    host_ids = network.get_host_ids() # [h0, h1, h2]
    hosts = []

    neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}
    for h in host_ids:
        # neighbor should be set in this experiment
        hosts.append(Host(id=h, neighbors=neighbors[h]))

    test_directory, sample = make_ready_for_test(network_dir=network_dir, test_name=test_name, condition=condition, test_sub_name=test_sub_name)

    if test_sub_name.startswith("single"):
        propagation_mode = ContextAggregator.SINGLE_ONLY_MODE
    else:
        propagation_mode = ContextAggregator.AGGREGATION_MODE

    config = {"network":network, "hosts":hosts, "neighbors":neighbors,
              "test_directory":test_directory, "sample":sample,
              "disconnection_rate":disconnection_rate, "drop_rate":drop_rate,
              ContextAggregator.PM:propagation_mode,
              "threshold":threshold}
    s = AggregationAsyncSimulator()
    simulation = s.run(config=config)
    return simulation
