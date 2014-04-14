import os

from get_processed_information import GetProcessedInformation
from read_reports import ReadReports
from utils_location import get_simple_test_dir

class GetStatistics(object):
    def __init__(self, reports):
        self.reports = reports
        self.get_processed_information = GetProcessedInformation(reports)

    def execute_fn(self, fn, condition = None, sub_name = None):
        if condition is not None:
            if sub_name is not None:
                return fn(condition, sub_name)
            else:
                sub_name = "singles"
                try: s = self.execute_fn(fn, condition, sub_name)
                except: s = None
                sub_name = "aggregates"
                try: a = self.execute_fn(fn, condition, sub_name)
                except: a = None
                return (s,a)
        else:
            results = {}
            for condition, value in self.reports.report.items():
                results[condition] = self.execute_fn(fn, condition)
            return results

    def get_size(self, condition = None, sub_name = None):
        """Given read report object that contains all the network info
        It returns the number of total communication packets

        >>> network_dir = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(network_dir)
        >>> s = GetStatistics(r)
        >>> s.get_size("normal","aggregates") == ([42, 14, 28], [42, 14, 28])
        True
        >>> s.get_size("normal","singles") == ([56, 56, 0], [56, 56, 0])
        True
        >>> s.get_size("normal") == (([56, 56, 0], [56, 56, 0]), ([42, 14, 28], [42, 14, 28]))
        True
        >>> s.get_size()['normal'] == (([56, 56, 0], [56, 56, 0]), ([42, 14, 28], [42, 14, 28]))
        True
        """
        fn = lambda condition, sub_name: self.get_processed_information.get_size(condition, sub_name)
        return self.execute_fn(fn, condition, sub_name)

    def get_speed(self, condition = None, sub_name = None):
        """Given read report object that contains all the network info
        It returns the number of total communication packets

        >>> network_dir = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(network_dir)
        >>> s = GetStatistics(r)
        >>> s.get_speed("normal","aggregates") == [4.75, 4, 5]
        True
        >>> s.get_speed("normal") == ([4.75, 4, 5], [4.75, 4, 5])
        True
        >>> s.get_speed()['normal'] == ([4.75, 4, 5], [4.75, 4, 5])
        True
        """
        fn = lambda condition, sub_name: self.get_processed_information.get_speed(condition, sub_name)
        return self.execute_fn(fn, condition, sub_name)


    def get_accuracy(self, condition = None, sub_name = None):
        """Given read report object that contains all the network info
        It returns the number of total communication packets

        >>> network_dir = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(network_dir)
        >>> s = GetStatistics(r)
        >>> s.get_accuracy("normal","aggregates") == [100.0, 67.98]
        True
        >>> s.get_accuracy("normal") == ([100.0, 100.0], [100.0, 67.98])
        True
        >>> s.get_accuracy()['normal'] == ([100.0, 100.0], [100.0, 67.98])
        True
        """
        fn = lambda condition, sub_name: self.get_processed_information.get_accuracy(condition, sub_name)
        return self.execute_fn(fn, condition, sub_name)

    def get_identified_rate(self, condition = None, sub_name = None):
        """Given read report object that contains all the network info
        It returns the number of total communication packets

        >>> network_dir = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(network_dir)
        >>> s = GetStatistics(r)
        >>> s.get_identified_rate("normal","aggregates") == [100.0, 8, 8, 56.25, 4, 8]
        True
        >>> s.get_identified_rate("normal") == ([100.0, 8, 8, 100.0, 8, 8], [100.0, 8, 8, 56.25, 4, 8])
        True
        >>> s.get_identified_rate()['normal'] == ([100.0, 8, 8, 100.0, 8, 8], [100.0, 8, 8, 56.25, 4, 8])
        True
        """
        fn = lambda condition, sub_name: self.get_processed_information.get_identified_rate(condition, sub_name)
        return self.execute_fn(fn, condition, sub_name)

    def get_cohorts(self, condition = None, sub_name = None):
        """Given read report object that contains all the network info
        It returns the number of total communication packets

        >>> network_dir = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(network_dir)
        >>> s = GetStatistics(r)
        >>> s.get_cohorts("normal","aggregates") == [1.75, 3, 1]
        True
        >>> s.get_cohorts("normal") == ([0.0, 0, 0], [1.75, 3, 1])
        True
        >>> s.get_cohorts()['normal'] == ([0.0, 0, 0], [1.75, 3, 1])
        True
        """
        fn = lambda condition, sub_name: self.get_processed_information.get_cohorts(condition, sub_name)
        return self.execute_fn(fn, condition, sub_name)

    def run(self, condition = None, sub_name = None):
        results = {}
        results["size"] = self.get_size(condition, sub_name)
        results["speed"] = self.get_speed(condition, sub_name)
        results["accuracy"] = self.get_accuracy(condition, sub_name)
        results["identification_rate"] = self.get_identified_rate(condition, sub_name)
        # Bug! The name should be cohorts
        results["cohorst"] = self.get_cohorts(condition, sub_name)
        return results

if __name__ == "__main__":
    import doctest
    doctest.testmod()