"""Utilities for simulation
"""
import os.path
from os.path import expanduser
from ConfigParser import *

CONFIGURATION_FILE_FOR_TEST = "config.cfg"

def get_test_files_directory():
    """
    >>> get_test_files_directory() is not None
    True
    """
    return get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory","test_files_directory")

def get_img_report_root_directory():
    return get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory","img_report_root_directory")

def get_test_report_root_directory():
    return get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory","test_report_root_directory")


def find_configuration_file(config_filename):
    """

    >>> f = find_configuration_file(CONFIGURATION_FILE_FOR_TEST)
    >>> f.endswith(CONFIGURATION_FILE_FOR_TEST)
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

    >>> f = get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory", "test_report_root_directory")
    >>> f is not None
    True
    """
    if not os.path.isabs(config_file_name):
        config_file_path = find_configuration_file(config_file_name)

    if config_file_path:
        f = SafeConfigParser()
        f.read(config_file_path)
        result = f.get(section, key)
        if result.startswith("~"):
            result = result.replace("~", os.path.expanduser("~"))
        return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()