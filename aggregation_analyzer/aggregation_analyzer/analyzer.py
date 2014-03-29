"""Analysis of simulation and genration of gnuplot file

"""
import os
import re

from aggregation_simulator.utils_configuration import get_test_report_root_directory
from glob import glob
from image_gen import generate_gif

def get_report_root_directory():
    test_root_dir = get_test_report_root_directory()
    report_dir = os.path.join(test_root_dir, "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def get_test_location(condition, name, kind, host, timestamp=0):
    test_root_dir = get_test_report_root_directory()
    timestamp = "%04d" % timestamp
    return test_root_dir + os.sep + condition + os.sep + name + os.sep + kind + os.sep + host + os.sep + timestamp

def starts_with(name, keys):
    """

    >>> keys = ["abc", "def", "xyz"]
    >>> starts_with("a", keys)
    "abc"
    >>> starts_with("k", keys)
    """
    for key in keys:
        if name.startswith(key): return key
    return None

def parse_percentage_precision(values):
    """
    avg(98.58%) individual(95.75%) -> 98.58, 95.75

    >>> parse_percentage_precision("avg(98.58%) individual(95.75%)")
    """
    pass

def read_statistics(file_path):
    result = {}
    keys = ["Correct average","Correct values","Estimated average","Estimated values","Identified values","% precision","Identified rate","Average number of cohorts"]
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

def read_statistic_results(condition, name, kind, host, timestamp, iteration = None):
    test_location = get_test_location(condition, name, kind, host, timestamp)

    if iteration is None:
        result = {}
        files = glob(test_location + os.sep + "*")

        for file in files:
            base_name = os.path.basename(file)
            p = re.search("(\d+)\.txt", base_name)
            if p:
                try:
                    i = int(p.group(1))
                    if type(i) is int:
                        result[i] = read_statistic_results(name, kind, host, timestamp, iteration=i)
                except ValueError:
                    pass # if the name is not 00..0 (int), don't do anything.
        return result
    else:
        iteration = "%04d" % iteration
        file_path = test_location + os.sep + iteration + ".txt"
        return read_statistics(file_path)

def generate_gifs(condition, name, kind, host, timestamp, iteration=None):
    test_location = get_test_location(condition, name, kind, host, timestamp)
    if iteration is None:
        result = {}
        files = glob(test_location + os.sep + "*")

        for file in files:
            base_name = os.path.basename(file)
            p = re.search("(\d+)\.txt", base_name)
            if p:
                try:
                    i = int(p.group(1))
                    if type(i) is int:
                        result[i] = generate_gifs(condition, name, kind, host, timestamp, iteration=i)
                except ValueError:
                    pass # if the name is not 00..0 (int), don't do anything.
#        for key, value in dictionary.items():
#            data = value["Estimated values"]
#            generate_gif(data, name + os.sep + kind + os.sep + host + os.sep + str(timestamp) + os.sep + "%04d.gif" % key)
    else:
        dictionary = read_statistic_results(condition, name, kind, host, timestamp, iteration)
        data = dictionary["Estimated values"]
        generate_gif(data, condition + os.sep + name + os.sep + kind + os.sep + host + os.sep + "%04d" % timestamp + os.sep + "%04d.gif" % iteration)

if __name__ == "__main__":
    #r = read_statistic_results("real_world_intel_6", "aggregates", "host1", 0, 6)
    #print r #["null IO"]
    #r = read_statistic_results("real_world_intel_6", "aggregates", "host1", 0)
    #print r
    #print len(r)

    for i in range(54):
        host = "host%d" % (i+1)
        # generate_gifs("normal","real_world_intel_6", "aggregates", host, 0)
        # generate_gifs("normal","real_world_intel_6", "singles", host, 0)
        generate_gifs("normal","real_world_intel_10", "aggregates", host, 0)
        # generate_gifs("normal","real_world_intel_10", "singles", host, 0)
        #generate_gifs("marked_sample","real_world_intel_10", "aggregates", host, 0)

    # host = "host24"
    # generate_gifs("normal","real_world_intel_6", "singles", host, 0, 0)