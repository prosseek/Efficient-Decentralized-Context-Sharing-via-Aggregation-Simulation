from utils_configuration import *
from network import Network
from context_aggregator.context_aggregator import ContextAggregator
from run_simulation import *
from host import Host
from aggregation_simulator import AggregationSimulator
from sample import Sample
from utils import get_sample_from_network_file

import warnings
import os
import shutil
import sys
import distutils.core

def get_sample_name(test_name):
    return test_name + ".sample.txt"

def make_ready_for_one_file_simulation(simulation_root_dir, network_file_path, sample_file_path=None, remove_existing_files=True):
    """Given a network_file path, it runs simulation based on the configuration
    >>> #network_file_path = '/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/data/10_100_10_10/tree/tree10_10_2_0.txt'
    >>> #sample_path = '/Usersa/smcho/code/PyCharmProjects/contextAggregator/aggregation_simulator/test_files/normal/real_world_intel_10/real_world_intel_10_sample.txt'
    >>> #make_ready_for_one_file_simulation(network_file_path, sample_path)
    """
    # 1. information gathering
    # if simulation_root_dir is None:
    #     mass_simulation_root_dir = get_mass_simulation_root_dir()
    # else:
    #     mass_simulation_root_dir = simulation_root_dir

    # print mass_simulation_root_dir
    if not os.path.exists(network_file_path):
        raise RuntimeError("No file %s exists" % network_file_path)

    network_name = os.path.basename(network_file_path).replace(".txt","")

    # 2. copy the file to the destination
    network_dir = os.path.join(simulation_root_dir, network_name)
    if remove_existing_files:
        if os.path.exists(network_dir):
            shutil.rmtree(network_dir)
        os.makedirs(network_dir)
        shutil.copy(network_file_path, network_dir)
    else: # don't remove, but create if none
        if not os.path.exists(network_dir):
            os.makedirs(network_dir)
            shutil.copy(network_file_path, network_dir)
        else: # network exists, so check if networkfile is there
            target_network_file_path = os.path.join(simulation_root_dir, network_name + ".txt")
            if not os.path.exists(target_network_file_path):
                shutil.copy(network_file_path, network_dir)



    sample_generate = True
    if sample_file_path is not None:
        if os.path.exists(sample_file_path):
            with open(sample_file_path, "r") as f:
                sample = f.read()
                f.close()
            sample_generate = False
        else:
            warnings.warn("no sample file, %s created" % sample_file_path)

    if sample_generate:
        sample = get_sample_from_network_file(network_file_path)

    sample_file_path = os.path.join(network_dir, network_name + ".sample.txt")
    with open(sample_file_path, "w") as f:
        f.write(sample)
        f.close()

    return network_dir

def make_ready_for_test(network_dir, test_name, condition, test_sub_name):
    """

    >>> test_files_directory = get_test_files_directory()
    >>> result = make_ready_for_test(test_files_directory, "normal", "test1","aggregate")
    >>> len(result) == 2
    True
    """
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

    # get the target root file
    test_report_directory = network_dir + os.sep + condition
    test_report_sub_directory = test_report_directory + os.sep + test_sub_name
    if os.path.exists(test_report_sub_directory):
        shutil.rmtree(test_report_sub_directory)
    os.makedirs(test_report_sub_directory)

    sample = Sample()
    sample.read(sample_file_path)

    return test_report_sub_directory, sample

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
    for h in host_ids:
        hosts.append(Host(h))
    neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

    test_directory, sample = make_ready_for_test(network_dir=network_dir, test_name=test_name, condition=condition, test_sub_name=test_sub_name)

    if test_sub_name.startswith("single"):
        propagation_mode = ContextAggregator.SINGLE_ONLY_MODE
    else:
        propagation_mode = ContextAggregator.AGGREGATION_MODE

    config = {"hosts":hosts, "neighbors":neighbors,
              "test_directory":test_directory, "sample":sample,
              "disconnection_rate":disconnection_rate, "drop_rate":drop_rate,
              ContextAggregator.PM:propagation_mode,
              "threshold":threshold}
    simulation = AggregationSimulator.run(config=config)
    return simulation

if __name__ == "__main__":
    import doctest
    doctest.testmod()