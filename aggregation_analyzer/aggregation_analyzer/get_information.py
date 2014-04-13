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
from utils import get_index_with_true

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

    #
    # Get APIs
    #

    def get_sent(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_sent("normal","singles")['host7'][0] == [2, 2, 0]
        True
        """
        r = self.get_progress_data(condition, sub_name, "Sent")
        return r

    def get_received(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_received("normal","singles")['host8'][0] == [1, 1, 0]
        True
        """
        r = self.get_progress_data(condition, sub_name, "Sent")
        return r

    def get_correct_values(self, condition):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_correct_values("normal") == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
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
        >>> info.get_identified_values("normal","singles")['host1'][0] == [1.0, '?(2)', '?(3)', '?(4)', '?(5)', '?(6)', '?(7)', '?(8)']
        True
        """
        return self.get_progress_data(condition, sub_name, "Identified values")

    def get_estimated_average(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_estimated_average("normal","singles")['host7']
        [7.0, 7.0, 6.0, 5.0, 4.5, 4.5]
        """
        return self.get_progress_data(condition, sub_name, "Estimated average")

    def get_estimated_values(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_estimated_values("normal","singles")['host7'][0]
        [7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0]
        """
        return self.get_progress_data(condition, sub_name, "Estimated values")

    def get_precision(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_precision("normal","singles")['host7'][-1]
        [100.0, 100.0]
        """
        return self.get_progress_data(condition, sub_name, "% precision")

    def get_identified_rate(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_identified_rate("normal","singles")['host7'][-1]
        [100.0, 8, 8, 100.0, 8, 8]
        """
        return self.get_progress_data(condition, sub_name, "Identified rate")

    def get_average_number_of_cohorts(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_average_number_of_cohorts("normal","singles")['host7'][-1]
        [0.0, 0, 0]
        """
        return self.get_progress_data(condition, sub_name, "Average number of cohorts")

    def get_null_io(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_null_io("normal","singles")['host7'] == [False, False, False, False, False, True]
        True
        """
        return self.get_progress_data(condition, sub_name, "null IO")

    def get_last_non_null_io(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetInformation(r, use_cache=False)
        >>> info.get_last_non_null_io("normal","singles")['host7'] == 5
        True
        """
        null_io = self.get_null_io(condition, sub_name)
        result = {}
        for host, value in null_io.items():
            result[host] = get_index_with_true(value)
        return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()