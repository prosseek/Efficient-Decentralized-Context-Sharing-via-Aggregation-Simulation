from utils_configuration import *
from network import Network
from context_aggregator.context_aggregator import ContextAggregator
from run_simulation import *
from host import Host
from aggregation_simulator import AggregationSimulator
from sample import Sample

import os
import shutil
import distutils.core

def get_sample_name(test_name):
    return test_name + "_sample.txt"

def make_ready_for_test(network_dir, test_name, condition, test_sub_name):
    """Given test_for_real_world name in test_files directory, and sub directory
    Returns the test_directory where the reports are recorded, and the sample file

    >>> test_files_directory = get_test_files_directory()
    >>> result = make_ready_for_test(test_files_directory, "normal", "test1","aggregate")
    >>> len(result) == 2
    True
    """
    #test_files_directory = get_test_files_directory()

    sample_name = get_sample_name(test_name)
    sample_file_path = os.path.join(network_dir, sample_name)
    # There should be sample files
    assert os.path.exists(sample_file_path), "No sample file at %s" % sample_file_path

    net_file_path = os.path.join(network_dir, test_name + ".txt")
    dot_file_path = net_file_path + ".dot"

    if os.path.exists(net_file_path):
        if not os.path.exists(dot_file_path):
            n = Network(net_file_path)
            dumb = n.dot_gen(dot_file_path)

    # directory = network_dir + os.sep + os.sep + test_name + os.sep + condition
    # if os.path.exists(directory):
    #     shutil.rmtree(directory)
    # os.makedirs(directory)

    # get the target root file
    test_report_directory = network_dir + os.sep + condition
    test_report_sub_directory = test_report_directory + os.sep + test_sub_name
    if os.path.exists(test_report_sub_directory):
        shutil.rmtree(test_report_sub_directory)
    os.makedirs(test_report_sub_directory)

    # http://stackoverflow.com/questions/15034151/copy-directory-contents-into-a-directory-with-python
    #distutils.dir_util.copy_tree(directory, test_report_directory)

    sample = Sample()
    sample.read(sample_file_path)

    return test_report_sub_directory, sample

def run_simulation(network_dir, condition, test_name, test_sub_name, disconnection_rate = 0.0, drop_rate=0.0):
    network_file_path = os.path.join(network_dir, test_name + ".txt")
    network = Network(network_file_path)
    host_ids = network.get_host_ids() # [h0, h1, h2]
    hosts = []
    for h in host_ids:
        hosts.append(Host(h))
    neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

    test_directory, sample = make_ready_for_test(network_dir=network_dir, test_name=test_name, condition=condition, test_sub_name=test_sub_name)

    if test_sub_name.startswith("single"):
        propagation_mode = ContextAggregator.SINGLE_ONLY_MODE
    else:
        propagation_mode = ContextAggregator.AGGREGATION_MODE

    config = {"hosts":hosts, "neighbors":neighbors,\
              "test_directory":test_directory, "sample":sample, \
              "disconnection_rate":disconnection_rate, "drop_rate":drop_rate, \
              ContextAggregator.PM:propagation_mode}
    simulation = AggregationSimulator.run(config=config)
    return simulation

if __name__ == "__main__":
    import doctest
    doctest.testmod()