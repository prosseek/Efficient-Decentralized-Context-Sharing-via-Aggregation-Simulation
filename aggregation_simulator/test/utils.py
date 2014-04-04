from aggregation_simulator.utils_configuration import *
from aggregation_simulator.network import Network
from context_aggregator.context_aggregator import ContextAggregator
from aggregation_simulator.utils_configuration import *
from aggregation_simulator.run_simulation import *
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
    d = get_test_files_directory()
    #network_dir = get_test_network(condition, test_name)
    run_simulation(d, condition, test_name, test_sub_name, disconnection_rate, drop_rate)