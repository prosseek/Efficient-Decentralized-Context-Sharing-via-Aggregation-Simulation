"""
{'disseminate_abnormal':
    {'aggregation':
        {'host7':
            {0:
"""
import os
import operator

from utils_location import get_simple_test_dir
from read_reports import ReadReports
from utils import *

class GetInformation(object):
    def __init__(self, r, use_cache=False):
        # Read all the report information when it's not ready
        if r.report == {}:
            # Warning, it may use old data
            r.read_all(use_cache=use_cache)
        self.report = r.report
        self.hosts = r.get_hosts()

    def get_hosts(self):
        return self.hosts

    def get_progress_data(self, condition, sub_name, key):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> results = info.get_progress_data("normal","singles","Sent")
        >>> results['host7'][0] == [2,2,0]
        True
        """
        results = {}
        for host in self.hosts:
            results[host] = self.get_iterations(condition, sub_name, host, key)
        return results

    def get_iterations(self, condition, sub_name, host, key):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> values = info.get_iterations("normal","singles","host1","Estimated values")
        >>> len(values) == 6
        True
        """

        iterations = self.report[condition][sub_name][host]
        results = []
        for i, value in iterations.items():
            results.append(value[key])
        return results

    @staticmethod
    def get_diff_max(correct_value, iterations):
        """In this example, the biggest difference is (5-1) = 4

        >>> correct_value = [1,2,3,4,5]
        >>> iterations = [[1,1,1,1,1], [2,2,2,2,2], [3,3,3,3,3]]
        >>> GetInformation.get_diff_max(correct_value, iterations) == 4
        True
        """
        zipped = zip(*iterations)
        maxes = map(max, zipped)
        mins = map(min, zipped)
        diffs1 = map(abs, map(operator.sub, maxes, correct_value))
        diffs2 = map(abs, map(operator.sub, mins, correct_value))
        result = [max(i,j) for i,j in zip(diffs1, diffs2)]
        return max(result)

    #
    # Get APIs
    #
    def get_sum_list(self, condition, sub_name, key):
        """
        When key is "Sent": this list is returned
        index - host, [Sum of single + aggr, number of single, number of aggr]
        [[9, 9, 0], [9, 9, 0], [1, 1, 0], [9, 9, 0], [17, 17, 0], [9, 9, 0], [1, 1, 0], [1, 1, 0]]

        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_sum_list("normal","singles","Sent")[0] == [9,9,0]
        True
        """
        results = []
        r = self.get_progress_data(condition, sub_name, key)
        for host, value in r.items():
            results.append(sum_lists_column(value))
        return results

    def get_sent(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_sent("normal","singles") == [56,56,0]
        True
        """
        results = []
        r = self.get_sum_list(condition, sub_name, "Sent")
        return sum_lists_column(r)

    def get_received(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_received("normal","singles") == [56,56,0]
        True
        """
        results = []
        r = self.get_sum_list(condition, sub_name, "Received")
        return sum_lists_column(r)

    def get_correct_values(self, condition):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_correct_value("normal") == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        True
        """
        if "singles" in self.report[condition]:
            sub_name = "singles"
        elif "aggregate" in self.report[condition]:
            sub_name = "aggregate"
        elif "aggregates" in self.report[condition]:
            sub_name = "aggregates"
        else:
            raise RuntimeError("No singles or aggregage")
        rep = self.report[condition][sub_name]["host1"][0]
        return rep["Correct values"]

    def get_identified_values(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_identified_values("normal","singles")[0][0] == ['?(1)', '?(2)', '?(3)', '?(4)', '?(5)', '?(6)', 7.0, '?(8)']
        True
        """
        results = []
        r = self.get_progress_data(condition, sub_name, "Identified values")
        for host, value in r.items():
            results.append(value)
        return results