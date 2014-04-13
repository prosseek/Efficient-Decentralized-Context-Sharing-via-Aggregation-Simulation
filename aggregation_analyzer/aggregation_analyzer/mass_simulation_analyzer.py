import os
import glob

def get_identification_rate(lists):
    identification_rate_aggregate = []
    identification_rate_singles = []
    for l in lists:
        identification_rate = l['identification_rate'][0]
        identification_rate_aggregate.append(identification_rate[0])
        identification_rate_singles.append(identification_rate[3])

    if len(identification_rate_aggregate) != 0:
        avg1 = 1.0*sum(identification_rate_aggregate)/len(identification_rate_aggregate)
        avg2 = 1.0*sum(identification_rate_singles)/len(identification_rate_singles)
        return (avg1, avg2)
    return (None, None)

class MassSimulationAnalyzer(object):
    def __init__(self, directory):
        self.directory = directory
        last_name = os.path.basename(directory)
        if "tree" in last_name:
            self.type = "tree"
        elif "mesh" in last_name:
            self.type = "mesh"

    def get_type_number(self, t, n):
        pattern = self.directory + os.sep + "%s%d*" % (t,n)
        files = glob.glob(pattern)
        return files

    def exec_file(self, file_path):
        with open(file_path, "r") as f:
            result = f.read()
            f.close()
        exec(result) in globals()

    def process(self, directory):
        """
        the directory of network report is given
        returns singles/aggregates values
        """
        results = {}
        singles_file_path = directory + os.sep + "c_0_0_no" + os.sep + "report_singles.txt"
        aggregates_file_path = directory + os.sep + "c_0_0_no" + os.sep + "report_aggregates.txt"
        g = globals()
        self.exec_file(singles_file_path)
        results['singles'] = avg
        self.exec_file(aggregates_file_path)
        results['aggregates'] = avg
        return results

    def get_average(self, key, value):
        singles = []
        aggregates = []

        for f in value:
            r = self.process(f)
            singles.append(r['singles'])
            aggregates.append(r['aggregates'])

        singles_identification_rate = get_identification_rate(singles)
        aggregates_identification_rate = get_identification_rate(aggregates)
        return singles_identification_rate, aggregates_identification_rate
        #print (key, singles_identification_rate, aggregates_identification_rate)

    def run(self):
        result = {}
        for i in range(10, 110, 10): # range(10, 110, 10):
            result[i] = self.get_type_number(self.type, i)

        avg = {}
        for key, value in result.items():
            avg[key] = self.get_average(key, value)

        print avg

if __name__ == "__main__":
    m = MassSimulationAnalyzer("/Users/smcho/Desktop/reports/reports/dense_trees")
    m.run()
    m = MassSimulationAnalyzer("/Users/smcho/Desktop/reports/reports/dense_meshes")
    m.run()
