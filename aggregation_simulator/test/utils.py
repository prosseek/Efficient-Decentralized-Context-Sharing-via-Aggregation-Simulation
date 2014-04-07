from aggregation_simulator.run_simulation import *


def get_test_network(condition, network_name):
    d = get_test_files_directory()
    network_file = os.path.join(d, "%s/%s/%s.txt" % (condition, network_name, network_name))
    network = Network()
    network.read(network_file)
    return network

def runit(simulation_root_dir, network_file_path, sample_file_path, condition, test_sub_name, disconnection_rate = 0.0, drop_rate=0.0, threshold=sys.maxint):
    network_dir = make_ready_for_one_file_simulation(simulation_root_dir=simulation_root_dir,
                                                     network_file_path=network_file_path,
                                                     sample_file_path=sample_file_path,
                                                     remove_existing_files=False)
    run_simulation(network_dir=network_dir,
                   condition=condition,
                   test_sub_name=test_sub_name,
                   disconnection_rate=disconnection_rate,
                   drop_rate=drop_rate,
                   threshold=threshold)