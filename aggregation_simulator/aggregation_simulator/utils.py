"""Utilities for simulation
"""
import os.path
from os.path import expanduser

def find_configuration_file(config_filename):
    """

    >>> f = find_configuration_file("config.txt")
    >>> f.endswith("config.txt")
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()