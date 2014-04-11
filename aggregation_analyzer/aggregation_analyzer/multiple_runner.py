"""This module executes (simulates) a network multiple times and then get the average out of it.
"""
import sys
import os
import pprint

from utils import *
from aggregation_simulator.run_simulation import *
from read_reports import ReadReports
from get_statistics import GetStatistics

class MultipleRunner(object):
    def __init__(self, config):
        self.config = config
        self.test_name = config["network_dir"]
        self.network_data_dir = get_test_files_directory() + os.sep + self.test_name
        self.condition = config["condition"]
        self.test_sub_name = config["test_sub_name"]
        self.disconnection_rate = config["disconnection_rate"]
        self.drop_rate = config["drop_rate"]
        self.threshold = config["threshold"]
        output_dir = get_reports_directory() + os.sep + config["network_dir"]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        name = "report_{condition}_{test_sub_name}_{drop_rate}_{disconnection_rate}_{threshold}.txt".format(**config)
        self.output_file_path = output_dir + os.sep + name
        self.results = []

        # create or copy path if necessary
        simulation_root_dir = get_configuration("config.cfg", "TestDirectory", "simple_test_root_dir")
        network_file_path = self.network_data_dir + os.sep + self.test_name + ".txt"
        sample_file_path = self.network_data_dir + os.sep + self.test_name + ".sample.txt"
        self.network_dir = make_ready_for_one_file_simulation(simulation_root_dir=simulation_root_dir,
                                         network_file_path=network_file_path,
                                         sample_file_path=sample_file_path,
                                         remove_existing_files=False)

    def execute(self, count):
        """It executes the simulation count times to average the result"""
        assert count > 0, "count should be more than 0"

        for i in range(count):
            print "Run %d started" % (i+1)
            run_simulation(network_dir=self.network_dir,
               condition=self.condition,
               test_sub_name=self.test_sub_name,
               disconnection_rate=self.disconnection_rate,
               drop_rate=self.drop_rate,
               threshold=self.threshold)
            print "Run %d ended" % (i+1)
            print "Start analysis of %d run started" % (i+1)
            d = ReadReports(self.network_dir, auto_read=True, use_cache=False)
            s = GetStatistics(d).run(self.condition, self.test_sub_name)
            print s
            print "End analysis of %d run started" % (i+1)
            self.results.append(s)
        return MultipleRunner.get_average(self.results), self.results

    def write(self, output_file_path, average, results):
        pp = pprint.PrettyPrinter(indent=4)
        with open(output_file_path, "w") as f:
            f.write("config=" + pp.pformat(self.config) + "\n\n")
            f.write("avg=" + pp.pformat(average) + "\n\n")
            f.write("results=" + pp.pformat(results) + "\n")

    def run(self, count=5):
        # get the average
        average, results = self.execute(count)
        self.write(self.output_file_path, average, results)


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

test_names = ["real_world_intel_6", "real_world_intel_6"]
test_names = ["test_network1"]
test_sub_names = ["singles", "aggregates"]

def test_change_drop_rate():
    for t in test_names:
        for d in range(0, 55, 10):
            drop_rate = d
            for n in test_sub_names:
                condition = "c%d_0_0" % int(drop_rate)
                config = {
                    "network_dir":t,
                    "condition":condition,
                    "test_sub_name":n,
                    "disconnection_rate":0.0,
                    "drop_rate":d,
                    "threshold":sys.maxint
                }
                m = MultipleRunner(config)
                m.run(5)

def test_change_discon_rate():
    for t in test_names:
        for d in range(0, 55, 10):
            discon_rate = d
            for n in test_sub_names:
                condition = "c0_%d_0" % int(discon_rate)
                config = {
                    "network_dir":t,
                    "condition":condition,
                    "test_sub_name":n,
                    "disconnection_rate":discon_rate,
                    "drop_rate":0.0,
                    "threshold":sys.maxint
                }
                m = MultipleRunner(config)
                m.run(5)

def test_change_threshold_rate():
    for t in test_names:
        for d in range(0, 20, 2):
            threshold = d
            for n in test_sub_names:
                condition = "c_0_0_%d" % int(threshold)
                config = {
                    "network_dir":t,
                    "condition":condition,
                    "test_sub_name":n,
                    "disconnection_rate":0.0,
                    "drop_rate":0.0,
                    "threshold":threshold
                }
                m = MultipleRunner(config)
                m.run(5)

if __name__ == "__main__":
    test_change_drop_rate()
    test_change_discon_rate()
    test_change_threshold_rate()