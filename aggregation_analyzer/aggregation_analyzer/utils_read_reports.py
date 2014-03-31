import os
import glob
import re

from utils import *
from utils_location import get_test_location, get_host_names

def get_data_from_iteration_key(iteration_dictionary, key):
    iterations = iteration_dictionary.keys()

    result = []
    for iteration in iterations:
        report = iteration_dictionary[iteration]
        values = report[key]
        result.append(values)
    return result

def read_report_into_dictionary(file_path):
    """Given a file path, it read a data into a dictionary
    """
    assert os.path.exists(file_path), "No file exists in %s" % file_path
    result = {}
    keys = ["Received", "Sent", "Correct average","Correct values","Estimated average","Estimated values","Identified values","% precision","Identified rate","Average number of cohorts"]
    eval_skip_list = ["Identified values"]
    with open(file_path, "r") as f:
        #lines = f.readlines()
        while True:
            no_input = False
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
                    if key in eval_skip_list:
                        result[key] = l.split(":")[1]
                    else:
                        result[key] = eval(l.split(":")[1])
    return result

def read_host_timestamp_reports(condition, name, kind, host, timestamp, iteration = None):
    """Given a location of a test results, it reads all of a specific iteration into dictionary.

    This method invokes read_statistics that reads one result from a filepath.

    """
    test_location = get_test_location(condition, name, kind, host, timestamp)

    if iteration is None:
        result = {}
        files = glob.glob(test_location + os.sep + "*")

        for file in files:
            base_name = os.path.basename(file)
            p = re.search("(\d+)\.txt", base_name)
            if p:
                try:
                    i = int(p.group(1))
                    if type(i) is int:
                        result[i] = read_host_timestamp_reports(condition, name, kind, host, timestamp, iteration=i)
                except ValueError:
                    pass # if the name is not 00..0 (int), don't do anything.
        return result
    else:
        iteration = "%04d" % iteration
        file_path = test_location + os.sep + iteration + ".txt"
        return read_report_into_dictionary(file_path)

def read_hosts_reports(condition, name, kind, timestamp=0):
    host_names = get_host_names(condition, name, kind)

    result = {}
    for host in host_names:
        result[host] = read_host_timestamp_reports(condition, name, kind, host, timestamp)
    return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()