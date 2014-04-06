import os.path
import shutil
import warnings
import functools
import glob
import sys

from aggregation_simulator.run_simulation import run_simulation
from aggregation_simulator.utils_configuration import *
from utils import *

CONFIGURATION_FILE_FOR_TEST = "config.cfg"
# def log(func):
#     @functools.wraps(func)
#     def wrapper(*args):
#         with warnings.catch_warnings(record=True) as w:
#             try:
#                 r = func(*args)
#                 if w != []:
#                     print w[-1]
#                 return r
#             except Exception, e:
#                 print "sorry %s" % e
#     return wrapper

def get_mass_simulation_root_dir():
    return get_configuration("config.cfg", "TestDirectory","mass_simulation_root_dir")

#@log
def make_ready_for_one_file_simulation(simulation_root_dir, network_file, sample_file=None):
    """Given a network_file path, it runs simulation based on the configuration
    >>> #network_file_path = '/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/data/10_100_10_10/tree/tree10_10_2_0.txt'
    >>> #sample_path = '/Usersa/smcho/code/PyCharmProjects/contextAggregator/aggregation_simulator/test_files/normal/real_world_intel_10/real_world_intel_10_sample.txt'
    >>> #make_ready_for_one_file_simulation(network_file_path, sample_path)
    """
    # 1. information gathering
    if simulation_root_dir is None:
        mass_simulation_root_dir = get_mass_simulation_root_dir()
    else:
        mass_simulation_root_dir = simulation_root_dir

    # print mass_simulation_root_dir
    if not os.path.exists(network_file):
        raise RuntimeError("No file %s exists" % network_file)

    network_name = os.path.basename(network_file).replace(".txt","")

    # 2. copy the file to the destination
    network_path = os.path.join(mass_simulation_root_dir, network_name)
    if os.path.exists(network_path):
        shutil.rmtree(network_path)
    os.makedirs(network_path)
    shutil.copy(network_file, network_path)

    sample_generate = True
    if sample_file is not None:
        if os.path.exists(sample_file):
            with open(sample_file, "r") as f:
                sample = f.read()
                f.close()
            sample_generate = False
        else:
            warnings.warn("no sample file, %s created" % sample_file)

    if sample_generate:
        sample = get_sample_from_network_file(network_file)

    sample_file_path = os.path.join(network_path, network_name + "_sample.txt")
    with open(sample_file_path, "w") as f:
        f.write(sample)
        f.close()

    return network_path

def get_test_name(network_file):
    """

    >>> print get_test_name("/blah/blah/hello.txt")
    hello
    """
    return os.path.basename(network_file).replace(".txt", "")

def process_network_files(directory, condition="normal", disconnection_rate=0.0, drop_rate=0.0):
    """
    >>> directory = '/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/data/10_100_10_10/tree'
    >>> process_network_files(directory)
    """
    network_files = glob.glob(directory + os.sep + "*.txt")
    for p in network_files:
        sys.stdout.write("Processing: %s %s %4.2f %4.2f" % (p, condition, disconnection_rate, drop_rate))
        process_one_network_file(None, p, condition, disconnection_rate, drop_rate)

def process_singles_and_aggregates(
                             network_dir,
                             condition,
                             disconnection_rate = 0.0,
                             drop_rate = 0.0):

    """
    Assume that the network and sample file exists in network directory
    """
    print "Processing %s ...\n" % network_dir

    params = {
              "network_dir":network_dir,
              "condition":condition,
              "test_sub_name":"singles",
              "disconnection_rate":disconnection_rate,
              "drop_rate":drop_rate}
    run_simulation(**params)
    params["test_sub_name"] = "aggregates"
    run_simulation(**params)

    return "OK"

# TODO: Bad name rename it
def process_one_network_file(simulation_root_directory,
                             network_file,
                             sample_file=None,
                             condition="normal",
                             disconnection_rate=0.0,
                             drop_rate=0.0):
    """
    Sample file creation when it is None, and remove all the existing directories
    """
    network_dir = make_ready_for_one_file_simulation(simulation_root_dir=simulation_root_directory, network_file=network_file, sample_file=sample_file)
    return process_singles_and_aggregates(network_dir, condition,disconnection_rate,drop_rate)

if __name__ == "__main__":
    # network_file_path = "/Users/smcho/code/PyCharmProjects/contextAggregator/helper_programs/test/pseudo_realworld_50.txt"
    # sensor_file_path = "/Users/smcho/code/PyCharmProjects/contextAggregator/helper_programs/mote_loc_data/pdf/sensor.500.txt"
    # process_one_network_file(network_file_path, sensor_file_path, condition="drop_30", disconnection_rate=0.0, drop_rate=0.3)
    # import doctest
    # doctest.testmod()
    network_file_path = "/Users/smcho/code/PyCharmProjects/contextAggregator/helper_programs/test/pseudo_realworld_50.txt"
    sensor_file_path = "/Users/smcho/code/PyCharmProjects/contextAggregator/helper_programs/mote_loc_data/pdf/sensor.500.txt"
    config = {
        "simulation_root_directory":None,
        "network_file":network_file_path,
        "sample_file":sensor_file_path,
        "condition":"normal",
        "disconnection_rate":0.0,
        "drop_rate":0.0
    }
    process_one_network_file(**config)
