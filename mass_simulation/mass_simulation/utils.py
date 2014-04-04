import os

from aggregation_simulator.network import Network

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
