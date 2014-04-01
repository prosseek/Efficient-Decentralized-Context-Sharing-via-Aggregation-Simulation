from aggregation_simulator.utils_configuration import *
from aggregation_simulator.network import Network
from context_aggregator.context_aggregator import ContextAggregator
from aggregation_simulator.utils_configuration import *
from aggregation_simulator.host import Host
from aggregation_simulator.aggregation_simulator import AggregationSimulator
from aggregation_simulator.utils import make_ready_for_test

def get_test_network(condition, network_name):
    d = get_test_files_directory()
    network_file = os.path.join(d, "%s/%s/%s.txt" % (condition, network_name, network_name))
    network = Network()
    network.read(network_file)
    return network

def runit(condition, test_name, test_sub_name, disconnection_rate = 0.0, drop_rate=0.0):
    network = get_test_network(condition, test_name)
    host_ids = network.get_host_ids() # [h0, h1, h2]
    hosts = []
    for h in host_ids:
        hosts.append(Host(h))
    neighbors = network.get_network() # {0:[1], 1:[0,2], 2:[1]}

    test_directory, sample = make_ready_for_test(condition, test_name, test_sub_name)

    if test_sub_name.startswith("single"):
        propagation_mode = ContextAggregator.SINGLE_ONLY_MODE
    else:
        propagation_mode = ContextAggregator.AGGREGATION_MODE

    config = {"hosts":hosts, "neighbors":neighbors,\
              "test_directory":test_directory, "sample":sample, \
              "disconnection_rate":disconnection_rate, "drop_rate":drop_rate, \
              ContextAggregator.PM:propagation_mode}
    simulation = AggregationSimulator.run(config=config)