"""
{'disseminate_abnormal':
    {'aggregation':
        {'host7':
            {0: {'Received': [2, 2, 0],
                'Average number of cohorts': [0.0, 0, 0],
                'Estimated average': 7.0,
                'Correct average': 4.5,
                '% precision': [44.44, -40.94],
                'Identified rate': [12.5, 1, 8, 12.5, 1, 8],
                'null IO': False,
                'Sent': [2, 2, 0],
                'Identified values': ' [?(1), ?(2), ?(3), ?(4), ?(5), ?(6), 7.00, ?(8)]\n',
                'Estimated values': [7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
                'Correct values': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]},
            1: {'Received': [1, 0, 1], ...

"""
import os
import glob
import re
import cPickle

from utils import *
from utils_location import *
from aggregation_simulator.network import Network

class ReadReports(object):
    def __init__(self, network_dir, auto_read = True, use_cache = True):
        self.network_dir = network_dir
        self.test_name = os.path.basename(network_dir)
        self.report = {}
        if auto_read:
            self.read_all(use_cache)
        self.hosts = self.get_hosts()

    #@staticmethod
    def get_hosts(self):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports.get_hosts(d)
        >>> r == ['host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8']
        True
        """
        network_dir = self.network_dir
        network_name = os.path.basename(network_dir)
        network_file_path = os.path.join(network_dir, network_name + ".txt")
        assert os.path.exists(network_file_path), "No %s network file exists" % network_file_path

        n = Network(network_file_path)
        ids = n.get_host_ids()
        return ["host%d" % i for i in sorted(ids)]

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
                            result[key] = recover_to_list((l.split(":")[1]).rstrip())

        return result

    def read_files_from_dir(self):
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

    def read_all(self, use_cache=False):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> results = r.read_all()
        >>> type(results) == dict and results is not None
        True
        >>> results = r.read_all()
        """
        cache_img = get_configuration("config.cfg","TestDirectory","cache_dir") + os.sep + self.test_name + ".img"
        dirname = os.path.dirname(cache_img)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if not os.path.exists(cache_img) or not use_cache:
            result = self.read_files_from_dir()
            with open(cache_img, "w") as f:
                cPickle.dump(result, f)
                f.close()
        else:
            # os.path.exists and not ignore_cache
            with open(cache_img, "r") as f:
                result = cPickle.load(f)
                #result = cPickle.load(f.read())
                f.close()
        self.report = result
        return result

    def read(self, condition, sub_name, timestamp):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> results = r.read("normal", "singles")
        >>> type(results) == dict and results is not None
        True
        """
        # For simple API
        # Users can just call read() without parameters to get the whole directory

        host_names = get_host_names(self.network_dir, condition, sub_name)
        results = {}
        for h in host_names:
            d = get_dir(self.network_dir, condition, sub_name, h, timestamp)
            results[h] = self.read_iterations(d)
        return results

if __name__ == "__main__":
    import doctest
    doctest.testmod()