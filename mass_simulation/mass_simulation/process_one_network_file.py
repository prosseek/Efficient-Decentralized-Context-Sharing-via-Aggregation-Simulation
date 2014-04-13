import sys
import os

from aggregation_analyzer.utils import *
from aggregation_analyzer.utils_location import *
from aggregation_analyzer.multiple_run_and_analysis import MultipleRunAndAnalysis

sims_dir = get_sims_dir()
reports_dir = get_reports_dir()
test_files_dir = get_test_files_dir()

test_name = "test_network1"
network_file_path = os.path.join(test_files_dir, test_name) + os.sep + test_name +  ".txt"
sims_file_dir = sims_dir
reports_file_dir = os.path.join(reports_dir, test_name)
drop_rate = 0
disconnection_rate = 0
threshold = sys.maxint

def process_one_file(sim_config):
    m = MultipleRunAndAnalysis(sim_config).run()

if __name__ == "__main__":
    sim_config = {
        "network_file_path": network_file_path,
        "run_count":10,
        "sims_dir":sims_file_dir,
        "reports_dir":reports_file_dir,
        "disconnection_rate":disconnection_rate,
        "drop_rate":drop_rate,
        "threshold":threshold
    }
    process_one_file(sim_config)