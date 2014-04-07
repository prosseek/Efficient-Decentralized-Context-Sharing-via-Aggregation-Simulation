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
