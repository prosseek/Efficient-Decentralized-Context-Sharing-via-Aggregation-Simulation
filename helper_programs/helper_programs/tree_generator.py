import random
import sys
import copy

from aggregation_simulator.network import Network

class RandomAddTreeGen:
    def __init__(self):
        pass

    def generate(self, node):
        """
        >>> g = RandomAddTreeGen()
        >>> n = g.generate(10)
        >>> print n
        """
        self.node = node
        n = Network()
        n.add_node(1)
        for i in range(2, node+1):
            j = 3
            n.add_neighbor(j)
        return n

class TreeGenerator:
    pass

if __name__ == "__main__":
    #t = Network('/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/massive_data/10_100_10_80/tree/tree20_10_100_90.txt')
    #print t.networkTopology
    #print TreeGen.tree_to_mesh(t.networkTopology, 0.8)
    g = TreeGenerator()
    print g.generate(node_size=5, max_depth=10, max_width=5, max_attempt=10)