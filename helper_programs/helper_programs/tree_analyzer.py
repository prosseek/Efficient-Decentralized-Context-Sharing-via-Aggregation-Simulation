import os
import glob

from aggregation_simulator.network import Network
from aggregation_simulator.utils_configuration import get_configuration

def avg(lists):
    return 1.0*sum(lists)/len(lists)

def get_average_neighbors_size(directory, node):
    """Given directory location and node size, it will return the average number of neighbors
    for the node

    >>> d = get_configuration("config.cfg", "TestDirectory", "less_dense_10_100_dir")
    >>> dtree = d + os.sep + "tree"
    >>> dmesh = d + os.sep + "mesh"
    >>> r = get_average_neighbors_size(directory=dtree, node=10)
    >>> abs(r[0] - 1.8) < 0.001
    True
    """
    p = os.path.basename(directory)
    pattern = directory + os.sep + p + "%d_*.txt" % node

    network_file_paths = glob.glob(pattern)
    if len(network_file_paths) == 0: return 0

    results = [Network(n).get_average_neighbor_size() for n in network_file_paths]
    return avg(results), results

if __name__ == "__main__":
    import doctest
    doctest.testmod()