"""Utilities for simulation
"""
import os.path
from os.path import expanduser
from ConfigParser import *

CONFIGURATION_FILE_FOR_TEST = "config.cfg"

def find_configuration_file(config_filename):
    """

    >>> f = find_configuration_file(CONFIGURATION_FILE_FOR_TEST)
    >>> f.endswith(CONFIGURATION_FILE_FOR_TEST)
    True
    """
    home = expanduser("~")
    current_directory = os.path.abspath(".")
    while current_directory != home:
        current_directory = os.path.abspath(os.path.join(current_directory, '..'))
        file_path = os.path.join(current_directory, config_filename)
        if os.path.exists(file_path):
            return file_path
    return None

def get_configuration(config_file_name, section, key):
    """

    >>> f = get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory", "test1")
    >>> f.endswith("network1.txt")
    True
    """
    config_file_path = find_configuration_file(config_file_name)
    if config_file_path:
        f = ConfigParser()
        f.read(config_file_path)
        return f.get(section, key)

if __name__ == "__main__":
    import doctest
    doctest.testmod()