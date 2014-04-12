import os
import copy
import random

from aggregation_simulator.network import Network
from aggregation_simulator.utils_configuration import get_test_files_directory

def get_average_network_link(network):
    n = Network(network)
    ids = n.get_host_ids()
    result = []
    for id in ids:
        result.append(n.get_neighbors(id))

    sizes = map(len, result)
    return 1.0*sum(sizes)/len(sizes)

def reduce_average_network_link(network, new_network_path, goal):
    network = Network(network).get_network()
    new_network = copy.copy(network)

    for key, neighbors in network.items():
        if len(neighbors) > goal:
            new_neighbors = sorted(neighbors, key=lambda e: random.random())
            new_neighbors = new_neighbors[0:goal]
            diff = set(neighbors) - set(new_neighbors)
            for d in diff:
                if len(new_network[d]) == 1: # if this is the only link, don't do anything
                    new_neighbors.append(d)
                else:
                    print "remove key(%d) from n(%s)" % (key, new_network[d])
                    new_network[d].remove(key)
                    print "removed key(%d) from n(%s)" % (key, new_network[d])
            new_network[key] = new_neighbors

    print new_network
    #new_network = Network.make_symmetric_network(self, new_network)
    n2 = Network(new_network)
    n2.write(new_network_path)
    n2.dot_gen(new_network_path + ".dot")

def generate_dot(network_file_path):
    network = Network(network_file_path)
    dot_file_path = network_file_path + ".dot"
    network.dot_gen(dot_file_path)

if __name__ == "__main__":
    network_name = "pseudo_realworld_49"
    network = get_test_files_directory() + os.sep + network_name + os.sep + network_name + ".txt"
    network_name = "pseudo_realworld_49_2d"
    new_network = get_test_files_directory() + os.sep + network_name + os.sep + network_name + ".txt"
    print get_average_network_link(network)
    generate_dot(new_network)
    #reduce_average_network_link(network, new_network,3)
    #print get_average_network_link(new_network)