"""This module executes (simulates) a network multiple times and then get the average out of it.

# WARNING!

"""
import sys
import os
import pprint

from utils import *
from aggregation_simulator.run_simulation import *
from read_reports import ReadReports
from get_statistics import GetStatistics

class MultipleRunAndAnalysis(object):
    def __init__(self, config):
        """

        :type self: object
        """
        self.config = config

        # File source, simulation and report destination
        self.network_file_path = config["network_file_path"]
        self.sims_dir = config["sims_dir"]
        self.reports_dir = config["reports_dir"]

        # recover test name and enclosing directory
        self.test_name = os.path.basename(self.network_file_path).split('.')[0]
        self.network_data_dir = os.path.dirname(self.network_file_path)

        # condition directory in the network directory

        #self.test_sub_name = config["test_sub_name"]
        disconnection_rate = config.get("disconnection_rate", 0)
        self.disconnection_rate = 1.0*disconnection_rate/100.0 # Warning, disconnection rate is converted here
        drop_rate = config.get("drop_rate", 0)
        self.drop_rate = 1.0*drop_rate/100.0 # WARNING, drop rate is converted in here.
        self.threshold = config.get("threshold", sys.maxint)
        if self.threshold > sys.maxint/2.0:
            threshold_name = "no"
        else:
            threshold_name = self.threshold

        self.condition = "c_{drop_rate}_{disconnection_rate}_{threshold_name}".format(threshold_name=threshold_name, drop_rate=int(drop_rate), disconnection_rate=int(disconnection_rate))

        self.report_file_dir = self.reports_dir + os.sep + self.test_name + os.sep + self.condition
        if not os.path.exists(self.report_file_dir):
            os.makedirs(self.report_file_dir)

        #self.results = []

        # create or copy path if necessary
        simulation_root_dir = self.sims_dir
        sample_file_path = self.network_data_dir + os.sep + self.test_name + ".sample.txt"
        self.network_dir = make_ready_for_one_file_simulation(simulation_root_dir=simulation_root_dir,
                                         network_file_path=self.network_file_path,
                                         sample_file_path=sample_file_path,
                                         remove_existing_files=False)

    def execute(self, sub_name, count):
        """It executes the simulation count times to average the result"""
        assert count > 0, "count should be more than 0"

        results = []
        for i in range(count):
            print "Run %d of %s started" % ((i+1), sub_name)
            #for sub_name in ["singles", "aggregates"]:
            #print "Execute %s started" % sub_name
            run_simulation(network_dir=self.network_dir,
               condition=self.condition,
               test_sub_name=sub_name,
               disconnection_rate=self.disconnection_rate,
               drop_rate=self.drop_rate,
               threshold=self.threshold)
            print "Run %d ended" % (i+1)
            print "Start analysis of %d run started" % (i+1)
            d = ReadReports(self.network_dir, condition=self.condition, auto_read=True, use_cache=False)
            s = GetStatistics(d).run(self.condition, sub_name)
            print s
            print "End analysis of %d run started" % (i+1)
            results.append(s)
        return MultipleRunAndAnalysis.get_average(results), results

    def write(self, output_file_path, average, results):
        pp = pprint.PrettyPrinter(indent=4)
        with open(output_file_path, "w") as f:
            f.write("config=" + pp.pformat(self.config) + "\n\n")
            f.write("avg=" + pp.pformat(average) + "\n\n")
            f.write("results=" + pp.pformat(results) + "\n")

    def run(self, count=None):

        if count is None:
            count = self.config.get("run_count", 5)

        # get the average
        for sub_name in ["singles", "aggregates"]:
            average, results = self.execute(sub_name, count)
            report_file_name = "report_%s.txt" % sub_name
            report_file_path = self.report_file_dir + os.sep + report_file_name
            self.write(report_file_path, average, results)


    @staticmethod
    def get_average(results):
        avg = {}

        # collect all the data in a dictionary
        for r in results:
            for key, value in r.items():
                if key not in avg: avg[key] = []
                avg[key].append(value)

        results = {}
        for key, values in avg.items():
            #print values
            results[key] = avg_lists_column(values)
        return results

# def test_change_drop_rate(start, stop, increase, sub_dir="test_change_drop_rate"):
#     global run_count
#     for t in test_names:
#         for d in range(start, stop, increase):
#             drop_rate = d/100.0
#             for n in test_sub_names:
#                 condition = "c_%d_0_0" % (int(d))
#                 config = {
#                     "report_sub_dir":sub_dir,
#                     "network_dir":t,
#                     "condition":condition,
#                     "test_sub_name":n,
#                     "disconnection_rate":0.0,
#                     "drop_rate":drop_rate,
#                     "threshold":sys.maxint
#                 }
#                 m = MultipleRunAndAnalysis(config)
#                 m.run(run_count)
#
# def test_change_discon_rate(start, stop, increase, sub_dir="test_change_discon_rate"):
#     global run_count
#     for t in test_names:
#         for d in range(start, stop, increase):
#             discon_rate = d/100.0
#             for n in test_sub_names:
#                 condition = "c_0_%d_0" % int(d)
#                 config = {
#                     "report_sub_dir":sub_dir,
#                     "network_dir":t,
#                     "condition":condition,
#                     "test_sub_name":n,
#                     "disconnection_rate":discon_rate,
#                     "drop_rate":0.0,
#                     "threshold":sys.maxint
#                 }
#                 m = MultipleRunAndAnalysis(config)
#                 m.run(run_count)
#
# def test_change_threshold_rate(start, stop, increase, sub_dir="test_change_threshold_rate"):
#     global run_count
#     for t in test_names:
#         for d in range(start, stop, increase):
#             threshold = d
#             for n in test_sub_names:
#                 condition = "c_0_0_%d" % int(threshold)
#                 config = {
#                     "report_sub_dir":sub_dir,
#                     "network_dir":t,
#                     "condition":condition,
#                     "test_sub_name":n,
#                     "disconnection_rate":0.0,
#                     "drop_rate":0.0,
#                     "threshold":threshold
#                 }
#                 m = MultipleRunAndAnalysis(config)
#                 m.run(run_count)

if __name__ == "__main__":
    sims_dir = get_sims_dir()
    reports_dir = get_reports_dir()
    test_files_dir = get_test_files_dir()

    test_names = ["real_world_intel_6", "real_world_intel_6"]
    test_names = ["pseudo_realworld_100", "pseudo_realworld_100_2d","pseudo_realworld_49", "pseudo_realworld_49_2d"]

    test_name = "test_network1"
    network_file_path = os.path.join(test_files_dir, test_name) + os.sep + test_name +  ".txt"
    sims_file_dir = os.path.join(sims_dir, test_name)
    reports_file_dir = os.path.join(reports_dir, test_name)
    drop_rate = 0
    disconnection_rate = 0
    threshold = sys.maxint

    sim_config = {
        "network_file_path": network_file_path,
        "run_count":10,
        "sims_dir":sims_file_dir,
        "reports_dir":reports_file_dir,
        "disconnection_rate":disconnection_rate,
        "drop_rate":drop_rate,
        "threshold":threshold
    }

    m = MultipleRunAndAnalysis(sim_config).run()
