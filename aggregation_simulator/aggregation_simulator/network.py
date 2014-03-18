"""Network file

Network file format is composed of multiple lines that start with a host and a neighbor.
Dictionary is used for representing network: network[1] = [2].

1: 2
2: 1 3
3: 2 4 6
4: 3 5
5: 4
6: 3 7
7: 6 8
8: 7

"""

import os
import sys
import re
import copy

from context_aggregator.utils import *
from utils import *
from ConfigParser import *

class Network(object):
    def __init__(self, network_file=None):
        self.network = {}
        self.network_file = None
        if network_file is not None:
            self.network = self.load_file(network_file)

    def load_file(self, network_file):
        """

        >>> file_path = get_configuration("config.txt", "TestDirectory", "test1")
        >>> n = Network()
        >>> p = n.load_file(file_path)
        >>> same({1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 6], 8: [7]}, n.get_network())
        True
        """
        self.network_file = os.path.abspath(network_file)
        if not os.path.exists(self.network_file):
            print >> sys.stderr, "\n>> ERROR! no file %" % self.network_file
            raise Exception("No file %s exists for graph" % self.network_file)
        else:
            self.network = self.network_file_parse_into_dictionary(network_file = self.network_file)
            self.network = self.make_symmetric_network(self.network)

        return self.network

    def get_network(self):
        return self.network

    def __getitem__(self, index):
        """

        >>> file_path = get_configuration("config.txt", "TestDirectory", "test1")
        >>> n = Network(file_path)
        >>> same(n[3], [2,4,6])
        True
        """
        return self.get_neighbors(index)

    def get_neighbors(self, index):
        """

        >>> file_path = get_configuration("config.txt", "TestDirectory", "test1")
        >>> n = Network(file_path)
        >>> same(n.get_neighbors(3), [2,4,6])
        True
        """
        if index in self.network:
            return self.network[index]
        else:
            return None

    def make_symmetric_network(self, network):
        """Symmetric network means 1:2 -> 2:1

        >>> network = {1: [2,3], 2:[3], 3:[1]}
        >>> n = Network()
        >>> d = n.make_symmetric_network(network)
        >>> same(d, {1: [2,3], 2:[1,3], 3:[1,2]})
        True
        """
        result = {}
        for key in network:
            values = network[key]
            for key2 in values:
                if key not in result: result[key] = set()
                if key2 not in result: result[key2] = set()
                result[key].add(key2)
                result[key2].add(key)

        for key in result:
            result[key] = list(result[key])

        return result

    def get_first_rest(self, l):
        """Split and return the host and its neighbors

        >>> n = Network()
        >>> f,r = n.get_first_rest("3: 2 4 6")
        >>> f
        3
        >>> r == [2,4,6]
        True
        """
        assert type(l) is str

        regex = re.compile("^(\d+):\s*((\d+\s*)+)")
        res = regex.search(l.rstrip())
        first = int(res.group(1))
        rest = map(lambda x: int(x), res.group(2).split(' '))
        return first, rest

    def network_file_parse_into_dictionary(self, network_file):
        """

        >>> file_path = get_configuration("config.txt", "TestDirectory", "test1")
        >>> n = Network()
        >>> d = n.network_file_parse_into_dictionary(file_path)
        >>> same(d, {1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [6, 8], 8: [7]})
        True
        """
        network = {}
        with open(network_file, 'r') as f:
            for l in f:
                first, rest = self.get_first_rest(l)
                network[first] = rest

        return network

    #
    # File output
    #
    def dot_gen(self, dot_file_path = None):
        """

        >>> file_path = get_configuration("config.txt", "TestDirectory", "test1")
        >>> n = Network(file_path)
        >>> len(n.dot_gen()) == len('graph graphname {1--2\\n2--3\\n3--4\\n3--6\\n4--5\\n6--7\\n7--8\\n}')
        True
        >>> dot_tmp = get_configuration("config.txt", "TestDirectory", "tmp_dot")
        >>> dumb = n.dot_gen(dot_tmp)
        >>> os.path.exists(dot_tmp)
        True
        """
        string = ""
        dot_file_template = """graph graphname {%s}"""

        cache = []
        for key, value in sorted(self.network.items()):
            for i in value:
                if sorted((key,i)) not in cache:
                    string += "%d--%d\n" % (key, i)
                    cache.append(sorted((key,i)))

        result = dot_file_template % string

        if dot_file_path:
            if os.path.exists(dot_file_path):
                os.unlink(dot_file_path)
            with open(dot_file_path, 'w') as f:
                f.write(result)
        return result

    #
    # Network configuration change
    #
    def clear_network(self, network):
        """
        >>> x = {1: [], 2: [3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 6], 8: [7]}
        >>> n = Network()
        >>> same({2: [3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 6], 8: [7]}, n.clear_network(x))
        True
        """
        network = copy.copy(network)
        remove = []
        for index in network:
            neighbors = network[index]
            if not neighbors:
                remove.append(index)

        for r in remove:
            del network[r]

        return network


    #
    # Modifying network by adding/removing neighbors
    #

    def remove_neighbor(self, index, neighbor):
        """
        >>> file_path = get_configuration("config.txt", "TestDirectory", "test1")
        >>> n = Network(file_path)
        >>> same({2: [3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 6], 8: [7]}, n.remove_neighbor(1, 2))
        True
        """
        network = self.get_network()
        if index in network:
            neighbors = network[index]
            if neighbor in neighbors:
                del neighbors[neighbors.index(neighbor)]
            if neighbor in network:
                neighbors = network[neighbor]
                if index in neighbors:
                    del neighbors[neighbors.index(index)]
        else:
            return network

        return self.clear_network(network)

    def add_neighbor(self, index, neighbor):
        """
        >>> file_path = get_configuration("config.txt", "TestDirectory", "test1")
        >>> n = Network(file_path)
        >>> same(n.add_neighbor(7, 9), {1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 9, 6], 8: [7], 9: [7]})
        True
        >>> same(n.get_network(), {1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 9, 6], 8: [7], 9: [7]})
        True
        >>> dot_file = get_configuration("config.txt", "TestDirectory", "tmp_dot2")
        >>> dumb = n.dot_gen(dot_file)
        >>> n = Network(file_path)
        >>> same(n.add_neighbor(10, 11), {1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 6], 8: [7], 10: [11], 11: [10]})
        True
        >>> dot_file = get_configuration("config.txt", "TestDirectory", "tmp_dot3")
        >>> dumb = n.dot_gen(dot_file)
        """

        network = self.get_network()
        if index in network:
            neighbors = network[index]
            if neighbor in neighbors: # already in the neighbors
                return network
            else:
                neighbors.append(neighbor)
        else:
            network[index] = [neighbor]

        self.network = self.make_symmetric_network(network)
        return self.network

if __name__ == "__main__":
    import doctest
    doctest.testmod()
