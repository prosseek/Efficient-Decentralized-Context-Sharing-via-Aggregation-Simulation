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
)
modules = ("re", "os",
           "ConfigParser",
           "shutil","copy","operator"
)

def run_parallel(subdir):
    directory = os.path.expanduser("~/code/PyCharmProjects/contextAggregator/test_files/data/%s" % subdir)
    print directory
    print os.path.exists(directory)
    # get all the simulation files
    network_files = glob.glob(directory + os.sep + "*.txt")

    def function_to_run(network_file):
        return process_one_network_file(network_file)

    ppservers = ("146.6.28.105:30000",)
    #ppservers=()

    job_server = pp.Server(ppservers=ppservers)

    #fn = pp.Template(job_server, sum_primes, (a.A, b.B), ("a","b","math"))
    fn = pp.Template(job_server, function_to_run, methods, modules)

    jobs = [(network_file, fn.submit(network_file)) for network_file in network_files]

    for input, job in jobs:
        print "Processing", input, "is ", job()

    job_server.print_stats()

if __name__ == "__main__":
    subdirs = ["10_100_10_80/mesh","10_100_10_80/tree","200_500_50_50/mesh","200_500_50_50/tree"]
    # 10_100_10_10/mesh, 10_100_10_10/tree
    for subdir in subdirs:
        run_parallel(subdir)

