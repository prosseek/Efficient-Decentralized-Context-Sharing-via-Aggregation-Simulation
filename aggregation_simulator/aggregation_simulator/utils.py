from utils_configuration import *
from network import Network

from sample import Sample

import os
import shutil
import distutils.core
import random

def get_sample_from_network_file(network_file):
    """Given a network_file path, it creates the sample value as its id

    1: 23.6438
    2: 23.4968
    ...

    >>> print get_sample_from_network_file('/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/data/10_100_10_10/tree/tree10_10_2_0.txt')
    0: 0
    1: 1
    2: 2
    3: 3
    4: 4
    5: 5
    6: 6
    7: 7
    8: 8
    9: 9
    """
    if not os.path.exists(network_file):
        raise RuntimeError("No file %s exists" % network_file)
    n = Network(network_file)
    ids = n.get_host_ids()
    result = []
    for id in ids[0:-1]:
        result.append("%d: %d\n" % (id, id))
    result.append("%d: %d" % (ids[-1], ids[-1]))
    return "".join(result)

def check_drop(drop_rate):
    """returns True at the rate of drop_rate
    check_drop(0.2)
    """
    # This value should be around 200
    # print len(filter(lambda m: m < drop_rate, [random() for i in range(1000)]))
    assert 0<= drop_rate <= 1.0, "drop rate wrong (%5.3f), it should be between 1 and 0"
    return random.random() < drop_rate

if __name__ == "__main__":
    import doctest
    doctest.testmod()