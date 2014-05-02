import sys
import pp
import glob
import os
import pprint

#sys.path.insert(0, "/Users/smcho/code/PyCharmProjects/contextAggregator/aggregation_simulator")

from aggregation_analyzer.utils_location import *
from aggregation_analyzer.multiple_run_and_analysis import MultipleRunAndAnalysis
from aggregation_analyzer.utils import *
from aggregation_analyzer.read_reports import ReadReports
from aggregation_analyzer.get_statistics import GetStatistics
from aggregation_analyzer.get_processed_information import GetProcessedInformation, GetInformation
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

from get_configs import *

methods = (MultipleRunAndAnalysis,
           ReadReports,
           separate_single_and_group_contexts,
           GetStatistics,
           avg,
           remove_if_in,
           avg_lists_column,
           GetInformation,
           GetProcessedInformation,
           simple_dict_to_list,
           get_host_names,
           sum_lists_column,
           get_dir,
           get_index_with_true,
           recover_to_list,
           starts_with,
           is_dictionary_standard,
           get_matching_aggregate_contexts,
           make_ready_for_one_file_simulation,
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
           is_empty_dictionary,
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
           get_average,
)
modules = ("re", "os",
           "ConfigParser",
           "shutil","copy","operator","random","cPickle","glob","pprint","warnings"
)

def run_parallel(configs):
    def function_to_run(config):
        m = MultipleRunAndAnalysis(config)
        return m.run()

    ppservers = ("146.6.28.105:30000",)
    #ppservers=()

    job_server = pp.Server(ppservers=ppservers)

    fn = pp.Template(job_server, function_to_run, methods, modules)

    jobs = []
    for config in configs:
        network_file = os.path.basename(config["network_file_path"])
        jobs.append((network_file, fn.submit(config)))

    for input, job in jobs:
        print "Processing", input, "is ", job()

    job_server.print_stats()


def run_massive_10_100():
    trees_dir = get_configuration("config.cfg", "TestDirectory", "trees_dir")
    #light_meshes_dir = get_configuration("config.cfg", "TestDirectory", "light_meshes_dir")
    #dense_meshes_dir = get_configuration("config.cfg", "TestDirectory", "dense_meshes_dir")

    #dirs = [trees_dir, light_meshes_dir, dense_meshes_dir]
    dirs = [trees_dir]
    names = ["trees_dir"]
    #names = ["trees_dir", "light_meshes_dir", "dense_meshes_dir"]
    for i, directory in enumerate(dirs):
        n = names[i]
        configs = get_configs_for_massive_simulation(directory, n)
        run_parallel(configs)

def run_various(test_name):
    remove_dirs(test_name)
    m = get_configs_for_various(test_name)
    #pprint.pprint(m)
    #run_parallel(m)
    for mp in m:
        process_one_file(mp)

if __name__ == "__main__":
    run_massive_10_100()
    # run_various("pseudo_realworld_100")
    # run_various("pseudo_realworld_100_2d")
    # run_various("pseudo_realworld_49")
    # run_various("pseudo_realworld_49_2d")
    #run_various("real_world_intel_10")
    #run_various("real_world_intel_6")