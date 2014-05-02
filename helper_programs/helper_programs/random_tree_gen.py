import random
import os
import copy

from aggregation_simulator.network import Network

class RandomTreeGen:
    def __init__(self):
        pass

    def mass_gen(self, total_size, node_size, directory, name = "tree"):
        result = set()
        networks = []
        while True:
            if len(result) == total_size:
                break
            n = self.generate(node_size)
            size_before = len(result)
            result.add(unicode(n))
            if len(result) != size_before: # it's new
                networks.append(n)

        for i, n in enumerate(networks):
            file_path = os.path.join(directory, name + str(i+1) + ".txt")
            self.write(n, file_path)

    def write(self, n, file_path):
        n.write(file_path)
        dot_file_path = file_path + ".dot"
        n.dot_gen(dot_file_path)

    def generate(self, node, file_path = None):
        """
        """
        n = Network()
        n.add_node(1)
        for i in range(2, node+1):
            r = range(1, i)
            j = random.choice(r)
            n.add_neighbor(i,j)

        if file_path is not None:
            self.write(n, file_path)

        return n

if __name__ == "__main__":
    import doctest
    doctest.testmod()