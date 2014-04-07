import os
import glob
import re

from utils import *
from utils_location import *

class ReadReports(object):
    def __init__(self, network_dir):
        self.network_dir = network_dir
        self.test_name = os.path.basename(network_dir)
        self.report = {}

    def read_iterations(self, directory):
        results = {}
        files = glob.glob(directory + os.sep + "*")

        for file in files:
            base_name = os.path.basename(file)
            p = re.search("(\d+)\.txt", base_name)
            if p:
                try:
                    i = int(p.group(1))
                    if type(i) is int:
                        results[i] = ReadReports.read_simulation_report(file)
                except ValueError:
                    pass # if the name is not 00..0 (int), don't do anything.
        return results

    @staticmethod
    def read_simulation_report(file_path):
        """Given a file path, it read a data into a dictionary
        """
        assert os.path.exists(file_path), "No file exists in %s" % file_path

        result = {}
        keys = ["Received", "Sent", "Correct average","Correct values","Estimated average","Estimated values","Identified values","% precision","Identified rate","Average number of cohorts"]

        with open(file_path, "r") as f:
            no_input = False
            while True:
                l = f.readline()
                if not l: break
                if l.startswith("## INPUT"):
                    l = eval(f.readline())
                    if l == {}:
                        no_input = True
                    else:
                        no_input = False
                elif l.startswith("## OUTPUT"):
                    l = eval(f.readline())
                    if l == {}:
                        no_output = True
                    else:
                        no_output = False

                    if no_input and no_output:
                        result["null IO"] = True
                    else:
                        result["null IO"] = False
                else:
                    key = starts_with(l, keys)
                    if key:
                        try:
                            result[key] = eval(l.split(":")[1])
                        except SyntaxError:
                            # Identified values will raise an error because of its error format
                            # Identified values: [1.00, ?(2), ?(3), ?(4), ?(5), ?(6), ?(7), ?(8)]
                            # [1.00, ?(2), ?(3), ?(4), ?(5), ?(6), ?(7), ?(8)]
                            #        ^
                            # SyntaxError: invalid syntax
                            result[key] = l.split(":")[1]

        return result

    def read_all(self):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> results = r.read_all()
        >>> type(results) == dict and results is not None
        True
        """
        dirs = os.listdir(self.network_dir)

        # d is the condition
        for condition in dirs:
            full_path = os.path.join(self.network_dir, condition)

            if os.path.isdir(full_path): # when condition is directory: "normal" ...
                self.report[condition] = {}
                dirs = os.listdir(full_path) # get all the sub directories
                for sub_name in dirs:
                    sub_name_full_path = os.path.join(full_path, sub_name)
                    if os.path.isdir(sub_name_full_path):
                        self.report[condition][sub_name] = self.read(condition, sub_name, timestamp=0)
        return self.report

    def read(self, condition = None, sub_name = None, timestamp=0):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> results = r.read("normal", "singles")
        >>> type(results) == dict and results is not None
        True
        """
        # For simple API
        # Users can just call read() without parameters to get the whole directory
        if condition is None and sub_name is None and timestamp == 0:
            return self.read_all()
        else:
            host_names = get_host_names(self.network_dir, condition, sub_name)
            results = {}
            for h in host_names:
                d = get_dir(self.network_dir, condition, sub_name, h, timestamp)
                results[h] = self.read_iterations(d)
            return results

if __name__ == "__main__":
    import doctest
    doctest.testmod()