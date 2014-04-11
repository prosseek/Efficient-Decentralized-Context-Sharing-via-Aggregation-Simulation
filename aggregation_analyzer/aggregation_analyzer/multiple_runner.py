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

if __name__ == "__main__":
    test1 =  "real_world_intel_6"
    #test1 =  "test_network1"
    config = {
        "network_dir":test1,
        "condition":"normal",
        "test_sub_name":"aggregates",
        "disconnection_rate":0.0,
        "drop_rate":0.0,
        "threshold":sys.maxint
    }
    m = MultipleRunner(config)
    m.run(5)
