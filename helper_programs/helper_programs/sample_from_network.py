"""This module provides function to create sample files from network file.
The sample data value is same as network id
"""

from aggregation_simulator.utils_configuration import get_test_files_directory

def generate_sample_from_network(network):
    """
    >>> generate_sample_from_network(None)
    """
    print get_test_files_directory()

if __name__ == "__main__":
    import doctest
    doctest.testmod()