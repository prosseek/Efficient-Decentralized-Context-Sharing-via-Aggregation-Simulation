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
import copy
import re

from context_aggregator.utils_same import *
from utils_configuration import *

class Network(object):
    def __init__(self, network_file=None):
        self.network = {}
        self.network_file = None
        if network_file is not None:
            if type(network_file) is str:
                self.network = self.read(network_file)
            elif type(network_file) is dict:
                self.network = network_file

    def read(self, network_file):
        """
        """
        self.network_file = os.path.abspath(network_file)
        if not os.path.exists(self.network_file):
            #print >> sys.stderr, "\n>> ERROR! no file %" % self.network_file
            raise Exception("No file %s exists for graph" % self.network_file)
        else:
            self.network = self.network_file_parse_into_dictionary(network_file = self.network_file)
            #self.network = self.make_symmetric_network(self.network)

        return self.network

    def write(self, network_file):
        hosts = self.get_host_ids()

        with open(network_file, "w") as f:
            for h in hosts:
                neighbors = str(self.get_neighbors(h))[1:-1].replace(",","")
                connection = "%d: %s\n" % (h, neighbors)
                f.write(connection)
            f.close()

    def get_network(self):
        return self.network

    def get_host_ids(self):
        return sorted(self.network.keys())

    def get_network(self):
        return self.network

    def __getitem__(self, index):
        """

        >>> file_path = get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory", "test1")
        >>> n = Network(file_path)
        >>> same(n[3], [2,4,6])
        True
        """
        return self.get_neighbors(index)

    def get_neighbors(self, index):
        """

        >>> file_path = get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory", "test1")
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

        >>> file_path = get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory", "test1")
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

        >>> file_path = get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory", "test1")
        >>> n = Network(file_path)
        >>> len(n.dot_gen()) == len('graph graphname {1--2\\n2--3\\n3--4\\n3--6\\n4--5\\n6--7\\n7--8\\n}')
        True
        """
        string = ""
        dot_file_template = """graph graphname {%s}"""

        key_set = set()
        for key, value in sorted(self.network.items()):
            for i in value:
                key_set.add(tuple(sorted((key, i))))

        #print key_set
        for i in sorted(key_set):
            string += "%d--%d\n" % (i[0], i[1])

        result = dot_file_template % string

        if dot_file_path:
            if os.path.exists(dot_file_path):
                os.unlink(dot_file_path)
            with open(dot_file_path, 'w') as f:
                f.write(result)
                    # dot -Tpng a.dot -o a.png
            command = "dot -Tpng %s -o %s" % (dot_file_path, dot_file_path + ".png")
            os.system(command)
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
        >>> file_path = get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory", "test1")
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

    def __str__(self):
        return str(self.get_network())

    def add_node(self, index):
        """
        >>> n = Network()
        >>> n.add_node(1)
        >>> print n
        {1: []}
        """
        n = self.get_network()
        if index not in n:
            n[index] = []

    def add_neighbor(self, index, neighbor):
        """
        >>> file_path = get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory", "test1")
        >>> n = Network(file_path)
        >>> same(n.add_neighbor(7, 9), {1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 9, 6], 8: [7], 9: [7]})
        True
        >>> same(n.get_network(), {1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 9, 6], 8: [7], 9: [7]})
        True
        >>> dot_file = get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory", "tmp_dot2")
        >>> dumb = n.dot_gen(dot_file)
        >>> n = Network(file_path)
        >>> same(n.add_neighbor(10, 11), {1: [2], 2: [1, 3], 3: [2, 4, 6], 4: [3, 5], 5: [4], 6: [3, 7], 7: [8, 6], 8: [7], 10: [11], 11: [10]})
        True
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

    def get_average_neighbor_size(self):
        """Given network path, it will return the number of average neighbors for the network.

        >>> p = get_configuration("config.cfg","TestDirectory","test_files_directory")
        >>> pth = p + os.sep + "test_network1/test_network1.txt"
        >>> Network(pth).get_average_neighbor_size()
        1.75
        """
        hosts = self.get_host_ids()
        r = []
        for h in hosts:
            r.append(len(self.get_neighbors(h)))
        return 1.0*sum(r)/len(r)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
