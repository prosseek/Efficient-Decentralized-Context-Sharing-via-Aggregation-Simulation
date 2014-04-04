import os.path
import shutil
import warnings
import functools

from aggregation_simulator.run_simulation import run_simulation
from aggregation_simulator.utils_configuration import *
from utils import *

def log(func):
    @functools.wraps(func)
    def wrapper(*args):
        with warnings.catch_warnings(record=True) as w:
            try:
                r = func(*args)
                if w != []:
                    print w[-1]
                return r
            except Exception, e:
                print "sorry %s" % e
    return wrapper

def get_mass_simulation_root_dir():
    return get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory","mass_simulation_root_dir")

@log
def make_ready_for_one_file_simulation(network_file, sample_file=None):
    """Given a network_file path, it runs simulation based on the configuration
    >>> #network_file_path = '/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/data/10_100_10_10/tree/tree10_10_2_0.txt'
    >>> #sample_path = '/Usersa/smcho/code/PyCharmProjects/contextAggregator/aggregation_simulator/test_files/normal/real_world_intel_10/real_world_intel_10_sample.txt'
    >>> #make_ready_for_one_file_simulation(network_file_path, sample_path)
    """
    # 1. information gathering
    mass_simulation_root_dir = get_mass_simulation_root_dir()
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

def process_one_network_file(network_file, condition="normal", disconnection_rate=0.0, drop_rate=0.0):
    """
    >>> network_file_path = '/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/data/10_100_10_10/tree/tree10_10_2_0.txt'
    >>> process_one_network_file(network_file_path)
    True
    """
    test_name = get_test_name(network_file)
    network_dir = make_ready_for_one_file_simulation(network_file)
    #network_path = os.path.join(network_dir, test_name + ".txt")
    #network = Network(network_path)

    params = {"condition":condition,
              "test_name":test_name,
              "test_sub_name":"singles",
              "disconnection_rate":disconnection_rate,
              "drop_rate":drop_rate}
    run_simulation(network_dir, **params) # condition, test_name, test_sub_name, disconnection_rate = 0.0, drop_rate=0.0):
    params["test_sub_name"] = "aggregates"
    run_simulation(network_dir, **params)
if __name__ == "__main__":
    import doctest
    doctest.testmod()
