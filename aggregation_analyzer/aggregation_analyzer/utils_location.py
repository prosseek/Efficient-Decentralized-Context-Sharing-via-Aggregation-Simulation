import os
import glob
import re

from aggregation_simulator.utils_configuration import get_configuration, CONFIGURATION_FILE_FOR_TEST

def get_dir(network_dir, condition, sub_name, host, timestamp=0):
    timestamp = "%04d" % timestamp
    directory = network_dir + os.sep + condition + os.sep + sub_name + os.sep + host + os.sep + timestamp
    return directory

def get_sims_dir():
    return get_configuration("config.cfg", "TestDirectory", "sims_dir")

def get_reports_dir():
    return get_configuration("config.cfg", "TestDirectory", "reports_dir")

def get_test_files_dir():
    return get_configuration("config.cfg", "TestDirectory", "test_files_directory")

def get_pseudo_test_dir():
    return get_configuration("config.cfg", "TestDirectory", "pseudo_test_root_dir")

def get_intel_test_dir():
    return get_configuration("config.cfg", "TestDirectory", "intel_test_root_dir")

def get_simple_test_dir():
    return get_configuration("config.cfg", "TestDirectory", "simple_test_root_dir")

def get_img_report_dir():
    return get_configuration("config.cfg", "TestDirectory","img_report_root_directory")

def get_host_names(network_dir, condition="normal", sub_name=""):
    """Get the host names for the network + condition + sub_name in sorted way
    >>> network_dir = os.path.join(simple_test_root_dir(), "test_network1")
    >>> print get_host_names(network_dir, "normal", "singles")
    ['host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8']
    """
    directory = network_dir + os.sep + condition + os.sep + sub_name + os.sep
    files = os.listdir(directory)

    r = {}
    for file in files:
        base_name = os.path.basename(file)
        p = re.search("host(\d+)", base_name)
        if p:
            r[int(p.group(1))] = p.group(0)

    result = []
    for key in sorted(r.keys()):
        result.append(r[key])
    return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()