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
from simulation_analyzer import SimulationAnalyzer

class VariousSimulationAnalyzer(SimulationAnalyzer):
    def __init__(self, network_dir):
        files = os.listdir(network_dir)
        self.drop_rate_list = []
        self.disconnection_rate_list = []
        self.threshold_rate_list = []
        self.normal = None

        for file in files:
            f = os.path.join(network_dir, file)
            if not file.startswith("c"): continue

            c, drop, discon, threshold = file.split('_')
            #print drop, discon, threshold
            if drop == '0' and discon == '0' and threshold == 'no':
                self.normal = f
            if drop != '0' and discon == '0' and threshold == 'no':
                self.drop_rate_list.append(f)
            if drop == '0' and discon != '0' and threshold == 'no':
                self.disconnection_rate_list.append(f)
            if drop == '0' and discon == '0' and threshold != 'no':
                self.threshold_rate_list.append(f)

    @staticmethod
    def bypass_the_bug(key, result):
        """
        """
        if key == "size":
            t = type(result[0][0])
            v = result[0][0]
        else:
            t = type(result[0])
            v = result[0]

        if t is list:
            return result[0]
        else:
            return result

    def read_singles_aggregates_reports(self, directory, key):
        a = os.path.join(directory, "report_aggregates.txt")
        s = os.path.join(directory, "report_singles.txt")
        self.exec_file(s, globals())
        avg1 = avg
        self.exec_file(a, globals())
        avg2 = avg

        #for some cases, we may have this results, it should outstrip the outer shell.
        #     avg={   'accuracy': [[100.0, 100.0]],
        # 'cohorst': [[0.0, 0, 0]], --> [0.0, 0, 0]
        # 'identification_rate': [[100.0, 100, 100, 100.0, 100, 100]],
        # 'size': [([28537, 28537, 0], [28537, 28537, 0])],
        # 'speed': [[11.31, 8, 14]]}
        result1 = VariousSimulationAnalyzer.bypass_the_bug(key, avg1[key])
        result2 = VariousSimulationAnalyzer.bypass_the_bug(key, avg2[key])

        return result1, result2

    def process_rate(self, lists, key, index):
        """Given key, return the value for the key for various range of drop_rate
        """
        results = {}
        for d in lists: # self.drop_rate_list:
            # c_0_10_no
            # index 1 -> drop rate
            # index 2 -> disconnection rate
            # index 3 -> threshold rate
            k = int(os.path.basename(d).split('_')[index])
            avg1, avg2 = self.read_singles_aggregates_reports(d, key)
            results[k] = (avg1, avg2)

        return results

    def process_rate_list(self, lists, index):
        results = {}
        for key in ["accuracy","identification_rate", "speed", "cohorst", "size"]:
            results[key] = self.process_rate(lists, key, index)
        return results

    def run(self):
        total_results = {}

        total_results["drop_rate"] = self.process_rate_list(self.drop_rate_list, index=1)
        total_results["disconnection_rate"] = self.process_rate_list(self.disconnection_rate_list, index=2)
        total_results["threshold_rate"] = self.process_rate_list(self.threshold_rate_list, index=3)
        return total_results

if __name__ == "__main__":
    m = VariousSimulationAnalyzer("/Users/smcho/tmp/reports/pseudo_realworld_100")
    pprint.pprint(m.run())
