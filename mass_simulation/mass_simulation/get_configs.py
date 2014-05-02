import sys

from aggregation_analyzer.utils_location import *

def get_configs(sim_config):
    run_count = sim_config.get("run_count", 5)

    drop_rate_start = sim_config.get("drop_rate_start", 0)
    drop_rate_end = sim_config.get("drop_rate_end", 1)
    drop_rate_step = sim_config.get("drop_rate_step", 1)
    drop_rate_range = (drop_rate_start, drop_rate_end, drop_rate_step)

    disconnection_rate_start = sim_config.get("disconnection_rate_start", 0)
    disconnection_rate_end = sim_config.get("disconnection_rate_end", 1)
    disconnection_rate_step = sim_config.get("disconnection_rate_step", 1)
    disconnection_rate_range = (disconnection_rate_start, disconnection_rate_end, disconnection_rate_step)

    threshold_rate_start = sim_config.get("threshold_rate_start", sys.maxint-1)
    threshold_rate_end = sim_config.get("threshold_rate_end", sys.maxint)
    threshold_rate_step = sim_config.get("threshold_rate_step", 1)
    threshold_range = (threshold_rate_start, threshold_rate_end, threshold_rate_step)

    configs = []

    test_name = sim_config["test_name"]
    reports_dir = sim_config["reports_dir"]
    sims_dir = sim_config["sims_dir"]

    drop_rate_start = sim_config.get("drop_rate_start", 0)
    drop_rate_end = sim_config.get("drop_rate_end", drop_rate_start+1)
    drop_rate_step = sim_config.get("drop_rate_step", drop_rate_start+1)
    drop_rate_range = (drop_rate_start, drop_rate_end, drop_rate_step)

    threshold = sys.maxint

    test_files_dir = get_test_files_dir() # We know where the test files are
    network_file_path = os.path.join(test_files_dir, test_name) + os.sep + test_name +  ".txt"

    results = []

    for drop_rate in range(*drop_rate_range):
        for disconnection_rate in range(*disconnection_rate_range):
            for threshold in range(*threshold_range):
                sim_config = {
                    "network_file_path": network_file_path,
                    "run_count":run_count,
                    # make ready code will create the subdir, so you don't need to sepcify it.
                    "sims_dir":sims_dir,
                    "reports_dir":reports_dir,
                    "disconnection_rate":disconnection_rate,
                    "drop_rate":drop_rate,
                    "threshold":threshold
                }
                results.append(sim_config)
    return results

def get_configs_for_massive_simulation(directory, name):

    results = []
    files = glob.glob(directory + os.sep + "*.txt")

    for f in files:
        #print file
        sim_config = {}
        sim_config["reports_dir"] = get_reports_dir() + os.sep + name
        sim_config["sims_dir"] = get_sims_dir() + os.sep + name
        sim_config["run_count"] = 1
        sim_config["network_file_path"] = f
        results.append(sim_config)

    return results

def get_configs_for_rate(test_name, name, start, end, step):
    sim_config = {}
    sim_config["test_name"] = test_name
    sim_config["reports_dir"] = get_reports_dir()
    sim_config["sims_dir"] = get_sims_dir()
    sim_config["run_count"] = 5

    sim_config["%s_start" % name] =  start
    sim_config["%s_end" % name] = end
    sim_config["%s_step" % name] = step

    configs = get_configs(sim_config)
    return configs

def get_configs_for_various(test_name):
    normal = get_configs_for_rate(test_name, "disconnection_rate", 0, 10, 5)
    various_disconnection = get_configs_for_rate(test_name, "disconnection_rate", 10, 91, 5)
    various_dropping = get_configs_for_rate(test_name, "drop_rate", 10, 91, 10)
    various_threshold = get_configs_for_rate(test_name, "threshold_rate", 1, 50, 1)
    return normal + various_disconnection + various_dropping + various_threshold

