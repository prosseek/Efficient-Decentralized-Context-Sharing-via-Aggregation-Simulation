"""
For N data that has this format, get the average
avg={   'accuracy': [[100.0, 40.132999999999996]],
    'cohorst': [[7.0, 7, 0]],
    'identification_rate': [[100.0, 10, 10, 30.0, 3, 10]],
    'size': [([35, 20, 15], [35, 20, 15])],
    'speed': [[2.2, 2, 3]]}

{'identification_rate': {10: ((100.0, 100.0), (100.0, 100.0)),
                         20: ((100.0, 100.0), (100.0, 100.0)),
((100,0, 100.0) <- singles only com
 (100.0, 22.40) <- aggregations com (total rate, rate only with singles)

 'speed': {10: (11.084099999999992, 11.084099999999992),
           20: (4.6905, 4.6905),
 <- average speed for singles and aggregates (always singles first)
"""

import os
import glob
import pprint

from utils import avg_lists_column
from simulation_analyzer import *

class MassSimulationAnalyzer(SimulationAnalyzer):
    def __init__(self, directory):
        self.directory = directory
        last_name = os.path.basename(directory)
        if "tree" in last_name:
            self.type = "tree"
        elif "mesh" in last_name:
            self.type = "mesh"

    def get_type_number(self, t, n):
        pattern = self.directory + os.sep + "%s%d_*" % (t,n)
        files = glob.glob(pattern)
        return files

    def process(self, directory):
        """
        the directory of network report is given
        returns singles/aggregates values
        """
        results = {}
        singles_file_path = directory + os.sep + "c_0_0_no" + os.sep + "report_singles.txt"
        aggregates_file_path = directory + os.sep + "c_0_0_no" + os.sep + "report_aggregates.txt"
        g = globals()
        self.exec_file(singles_file_path, globals())
        results['singles'] = avg
        self.exec_file(aggregates_file_path, globals())
        results['aggregates'] = avg
        return results

    def get_average(self, fun, value):
        singles = []
        aggregates = []

        for f in value:
            r = self.process(f)
            singles.append(r['singles'])
            aggregates.append(r['aggregates'])

        singles_identification_rate = fun(singles)
        aggregates_identification_rate = fun(aggregates)

        #print (key, singles_identification_rate, aggregates_identification_rate)
        # First one is for singles only case: 100 for total 100 for only single contexts
        # (100, (100.0, 100.0), (100.0, 22.403200000000012))
        return singles_identification_rate, aggregates_identification_rate

    def get_identification_rate_average(self, value):
        return self.get_average(get_identification_rate, value)

    def get_speed_average(self, value):
        return self.get_average(get_speed_rate, value)

    def get_cohorts_average(self, value):
        return self.get_average(get_cohorts_rate, value)

    def get_accuracy_average(self, value):
        return self.get_average(get_accuracy, value)

    def get_size_average(self, value):
        return self.get_average(get_size, value)

    def run(self):
        total_results = {}
        result = {}
        for i in range(10, 110, 10): # range(10, 110, 10):
            result[i] = self.get_type_number(self.type, i)

        avg = {}
        for key, value in result.items():
            avg[key] = self.get_identification_rate_average(value)
        total_results["identification_rate"] = avg

        avg = {}
        for key, value in result.items():
            avg[key] = self.get_speed_average(value)
        total_results["speed"] = avg

        avg = {}
        for key, value in result.items():
            avg[key] = self.get_cohorts_average(value)
        total_results["cohorts"] = avg

        avg = {}
        for key, value in result.items():
            avg[key] = self.get_accuracy_average(value)
        total_results["accuracy"] = avg

        avg = {}
        for key, value in result.items():
            avg[key] = self.get_size_average(value)
        total_results["size"] = avg

        return total_results


if __name__ == "__main__":
    #m = MassSimulationAnalyzer("/Users/smcho/tmp/reports/dense_meshes_dir")
    #pprint.pprint(m.run())
    # m = MassSimulationAnalyzer("/Users/smcho/tmp/reports/dense_trees_dir")
    # pprint.pprint(m.run())
    #m = MassSimulationAnalyzer("/Users/smcho/tmp/reports/light_meshes_dir")
    #pprint.pprint(m.run())
    m = MassSimulationAnalyzer("/Users/smcho/tmp/reports/trees_dir")
    pprint.pprint(m.run())