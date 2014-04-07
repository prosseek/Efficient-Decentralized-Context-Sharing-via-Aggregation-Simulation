import sys
import pp
import glob
import os

#sys.path.insert(0, "/Users/smcho/code/PyCharmProjects/contextAggregator/aggregation_simulator")

from process_one_network_file import *
from utils import *
from aggregation_simulator.network import *
from aggregation_simulator.host import *
from context_aggregator.context_aggregator import ContextAggregator
from context_aggregator.utils_configuration import process_default_values
from context_aggregator.input import *
from context_aggregator.output import *
from context_aggregator.inputoutput import *
from context_aggregator.context_database import *
from context_aggregator.assorted_context_database import *
from context_aggregator.context_history import *
from aggregation_simulator.run_simulation import *
from aggregation_simulator.sample import *
from aggregation_simulator.aggregation_simulator import *
from context.context import *
from aggregation_simulator.utils_report import *
from context_aggregator.utils import *
from context_aggregator.output_selector import *
from context_aggregator.disaggregator import *
from context_aggregator.greedy_maxcover import *
from context_aggregator.maxcover import *

methods = (process_one_network_file,
           process_singles_and_aggregates,
           get_test_name,
           make_ready_for_one_file_simulation,
           get_mass_simulation_root_dir,
           get_configuration,
           find_configuration_file,
           get_sample_from_network_file,
           run_simulation,
           Network,
           Host,
           ContextAggregator,
           process_default_values,
           InputOutput,
           Input,
           Output,
           ContextDatabase,
           AssortedContextDatabase,
           ContextHistory,
           make_ready_for_test,
           get_sample_name,
           Sample,
           AggregationSimulator,
           Context,
           cohort_type_as_bytearray,
           set2bytearray,
           get_matching_single_contexts,
           get_number_of_one_from_bytearray,
           get_number_of_one_from_number,
           bytearray2set,
           byte2set,
           contexts_to_standard,
           contexts_to_standard2,
           report_generate,
           StatisticalReport,
           empty_dictionary,
           empty_list,
           container_to_string,
           context_set_to_string,
           sort_singles,
           values_to_string,
           get_cohorts_statistics,
           get_identified_values,
           estimate_average,
           get_estimated_values,
           calculate_error,
           add_standards,
           is_standard,
           OutputSelector,
           aggregated_contexts_to_list_of_standard,
           Disaggregator,
           sub,
           cohort_type_as_set,
           is_in,
           get_prime,
           exclude_context,
           is_prime,
           sort_aggregates,
           is_exclusive,
           MaxCover,
           GreedyMaxCover,
           check_drop,
)
modules = ("re", "os",
           "ConfigParser",
           "shutil","copy","operator","random"
)

def run_networks_in_directory(network_files):
    def function_to_run(config):
        return process_one_network_file(**config)

    ppservers = ("146.6.28.105:30000",)
    #ppservers=()

    job_server = pp.Server(ppservers=ppservers)

    fn = pp.Template(job_server, function_to_run, methods, modules)

    config = {
        "simulation_root_directory":None,
        "sample_file":None,
        "condition":"normal",
        "disconnection_rate":0.0,
        "drop_rate":0.0
    }
    jobs = []
    for network_file in network_files:
        config["network_file"] = network_file
        jobs.append((network_file, fn.submit(config)))

    for input, job in jobs:
        print "Processing", input, "is ", job()

    job_server.print_stats()

def run_various_parallel(network_dir, condition, variation):
    """
    choices = {"drop_rate":(20, 0.0, 50.0, 5.0), "disconnection_rate":(20, 0.0, 50.0, 5.0)}
    <- 20 means 20 times iteration
    <- 0.0 5.0 10.0 ... 50.0 inclusive
    for key, value in choices.items():
            print key, value
            run_various_parallel(network_file, sample_file, key, value)
    """
    def function_to_run(config):
        return process_singles_and_aggregates(**config)

    print "The directory where network file is located %s %s" % (network_file_path, os.path.exists(network_file_path))
    ppservers = ("146.6.28.105:30000",)

    job_server = pp.Server(ppservers=ppservers)

    fn = pp.Template(job_server, function_to_run, methods, modules)
    iter = variation[0]
    start = variation[1]
    stop = variation[2]
    increase = variation[3]
    configs = []

    disconnection_rate = 0.0
    drop_rate = 0.0

    value = start
    while value <= stop:

        if condition == "drop_rate":
            disconnection_rate = value
        else:
            drop_rate = value

        for i in range(iter):
            condition_name = "%s_droprate_%s_discountrate_%s_iter_%d" % (condition, drop_rate, disconnection_rate, i) # drop_rate or disconnection_rate
            config = {
                "network_dir":network_dir,
                "condition":condition_name,
                "disconnection_rate":disconnection_rate,
                "drop_rate":drop_rate
            }
            configs.append(config)
        value += increase

    jobs = []
    for config in configs:
        jobs.append((network_file_path, fn.submit(config)))

    for input, job in jobs:
        print "Processing", input, "is ", job()

    job_server.print_stats()


def run_mass_parallel(subdir):
    directory = os.path.expanduser("~/code/PyCharmProjects/contextAggregator/test_files/data/%s" % subdir)

    print "The directory where multiple networks located %s %s" % (directory, os.path.exists(directory))
    # get all the simulation files
    network_files = glob.glob(directory + os.sep + "*.txt")
    return run_networks_in_directory(network_files)

if __name__ == "__main__":
    #test_files_directory=%(project_root_dir)s/contextAggregator/aggregation_simulator/test_files
    simulation_root_dir = get_configuration("config.cfg","TestDirectory","various_simulation_root_dir")
    if not os.path.exists(simulation_root_dir): os.makedirs(simulation_root_dir)
    base_directory = get_configuration("config.cfg","TestDirectory","test_files_directory")
    network_files = [
        "pseudo_realworld_50",
        "pseudo_realworld_30",
        "real_world_intel_6",
        "real_world_intel_10"
        #"test_network1"
    ]
    choices = {"drop_rate":(5, 0.0, 50.0, 5.0), "disconnection_rate":(20, 0.0, 50.0, 5.0)}
    #choices = {"drop_rate":(2, 0.0, 5.0, 5.0)}
    for file in network_files:
        # make ready for the simulation
        file_name = os.path.join(base_directory, file)
        network_file_path = os.path.join(file_name, file + ".txt")
        sample_file_path = os.path.join(file_name, file + ".sample.txt")
        assert os.path.exists(network_file_path), "no %s exists" % network_file_path
        assert os.path.exists(sample_file_path), "no %s exists" % sample_file_path

        network_dir = make_ready_for_one_file_simulation(simulation_root_dir=simulation_root_dir, network_file=network_file_path, sample_file=sample_file_path)

        for key, value in choices.items():
            print key, value
            run_various_parallel(network_dir, key, value)

    # subdirs = ["10_100_10_80/mesh"] # ,"10_100_10_80/tree","200_500_50_50/mesh","200_500_50_50/tree"]
    # # 10_100_10_10/mesh, 10_100_10_10/tree
    # for subdir in subdirs:
    #     run_mass_parallel(subdir)

