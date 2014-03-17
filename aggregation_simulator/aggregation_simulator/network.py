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

from context_aggregator.utils import *
from utils import *
from ConfigParser import *

class Network(object):
    def __init__(self, network_file=None):
        self.network = {}
        self.networkFile = None
        if network_file is not None:
            self.network_file = os.path.abspath(network_file)
            if not os.path.exists(self.network_file):
                print >> sys.stderr, "\n>> ERROR! no file %" % self.network_file
                raise Exception("No file %s exists for graph" % self.network_file)
            else:
                network = self.network_file_parse(network_file = self.network_file)
                self.network = self.make_symmetric_network(network)
            #self.buildHost()
        f = find_configuration_file("config.txt")
        if f is None:
            raise "configuration file not found, put config.txt into anypath up to ~"
        else:
            self.config_parser = ConfigParser()
            self.config_parser.read(f)

    def read_config(self, section, key):
        return self.config_parser.get(section, key)

    def get_network(self):
        return self.network

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
        >>> n = Network()
        >>> test_file_directory = n.read_config("TestDirectory", "path")
        >>> file_path = os.path.join(test_file_directory, "network1.txt")
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
