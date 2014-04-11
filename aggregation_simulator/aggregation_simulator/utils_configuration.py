"""Utilities for simulation
"""
import os.path
from os.path import expanduser
import ConfigParser #import *

# global doesn't seem to work with parallel python
CONFIGURATION_FILE_FOR_TEST = "config.cfg"

def get_network1():
    directory = get_test_files_directory()
    file_path = directory + os.sep + "tmp" + os.sep + "network1.txt"
    assert os.path.exists(file_path), "No %s exists - check if it is deleted" % file_path
    return file_path

def get_reports_directory():
    return get_configuration("config.cfg", "TestDirectory","reports_directory")

def get_test_files_directory():
    """
    >>> get_test_files_directory() is not None
    True
    """
    return get_configuration("config.cfg", "TestDirectory","test_files_directory")


def get_test_report_root_directory():
    return get_configuration("config.cfg", "TestDirectory","test_report_root_directory")


def find_configuration_file(config_filename):
    """

    >>> f = find_configuration_file("config.cfg")
    >>> f.endswith("config.cfg")
    True
    """
    home = os.path.expanduser("~")
    current_directory = os.path.abspath(".")
    while current_directory != home:
        current_directory = os.path.abspath(os.path.join(current_directory, '..'))
        file_path = os.path.join(current_directory, config_filename)
        if os.path.exists(file_path):
            return file_path
    return None

def get_configuration(config_file_name, section, key):
    """

    >>> f = get_configuration("config.cfg", "TestDirectory", "test_report_root_directory")
    >>> f is not None
    True
    """
    if not os.path.isabs(config_file_name):
        config_file_path = find_configuration_file(config_file_name)

    if config_file_path:
        f = ConfigParser.SafeConfigParser()
        f.read(config_file_path)
        result = f.get(section, key)
        if result.startswith("~"):
            result = result.replace("~", os.path.expanduser("~"))
        return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()