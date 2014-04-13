import os
import operator

from utils import sum_lists_column, simple_dict_to_list, avg, avg_lists_column
from utils_location import get_simple_test_dir
from read_reports import ReadReports
from get_information import GetInformation

class GetProcessedInformation(object):
    def __init__(self, reports):
        assert type(reports) is ReadReports
        self.reports = reports
        self.information = GetInformation(reports)

    @staticmethod
    def get_diff_max(correct_value, iterations):
        """In this example, the biggest difference is (5-1) = 4

        >>> correct_value = [1,2,3,4,5]
        >>> iterations = [[1,1,1,1,1], [2,2,2,2,2], [3,3,3,3,3]]
        >>> GetProcessedInformation.get_diff_max(correct_value, iterations) == 4
        True
        """
        zipped = zip(*iterations)
        maxes = map(max, zipped)
        mins = map(min, zipped)
        diffs1 = map(abs, map(operator.sub, maxes, correct_value))
        diffs2 = map(abs, map(operator.sub, mins, correct_value))
        result = [max(i,j) for i,j in zip(diffs1, diffs2)]
        return max(result)


    @staticmethod
    def get_sum_hosts(r):
        """
        When key is "Sent": this list is returned
        index - host, [Sum of single + aggr, number of single, number of aggr]
        [[9, 9, 0], [9, 9, 0], [1, 1, 0], [9, 9, 0], [17, 17, 0], [9, 9, 0], [1, 1, 0], [1, 1, 0]]

        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> info = GetInformation(ReadReports(d), use_cache=False)
        >>> r = info.get_sent("normal","singles")
        >>> GetProcessedInformation.get_sum_hosts(r)[0] == [9,9,0]
        True
        """
        results = []
        for host, value in r.items():
            results.append(sum_lists_column(value))
        return results

    def get_sent_total_sum(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> info = GetProcessedInformation(ReadReports(d))
        >>> info.get_sent_total_sum("normal","singles") == [56,56,0]
        True
        """
        results = []
        r = self.information.get_sent(condition, sub_name)
        v = self.get_sum_hosts(r)
        return sum_lists_column(v)

    def get_received_total_sum(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> info = GetProcessedInformation(ReadReports(d))
        >>> info.get_received_total_sum("normal","singles") == [56,56,0]
        True
        """
        results = []
        r = self.information.get_received(condition, sub_name)
        r = self.get_sum_hosts(r)
        return sum_lists_column(r)

    def get_size(self, condition, sub_name):
        return (self.get_sent_total_sum(condition, sub_name), self.get_received_total_sum(condition, sub_name))

    def get_speed(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(d)
        >>> info = GetProcessedInformation(r)
        >>> info.get_speed("normal","singles") == [4.75, 4, 5]
        True
        """
        # {'host7': 5, 'host6': 4, 'host5': 5, 'host4': 5, 'host3': 4, 'host2': 5, 'host1': 5, 'host8': 5}
        null_io = self.information.get_last_non_null_io(condition, sub_name)
        #print self.information.get_null_io(condition, sub_name)
        l = simple_dict_to_list(null_io)
        return [avg(l), min(l), max(l)]

    def get_accuracy(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> info = GetProcessedInformation(ReadReports(d))
        >>> info.get_accuracy("normal","singles") == [100.0, 100.0]
        True
        """
        precisions = self.information.get_precision(condition, sub_name)
        lists = simple_dict_to_list(precisions)
        last_list = map(lambda m: m[-1], lists)
        return avg_lists_column(last_list)

    def get_identified_rate(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> info = GetProcessedInformation(ReadReports(d))
        >>> info.get_identified_rate("normal","singles") == [100.0, 8, 8, 100.0, 8, 8]
        True
        """
        precisions = self.information.get_identified_rate(condition, sub_name)
        lists = simple_dict_to_list(precisions)
        last_list = map(lambda m: m[-1], lists)
        return avg_lists_column(last_list)

    def get_cohorts(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> info = GetProcessedInformation(ReadReports(d))
        >>> info.get_cohorts("normal","singles") == [0.0, 0, 0]
        True
        """
        precisions = self.information.get_average_number_of_cohorts(condition, sub_name)
        lists = simple_dict_to_list(precisions)
        last_list = map(lambda m: m[-1], lists)
        return avg_lists_column(last_list)

if __name__ == "__main__":
    import doctest
    doctest.testmod()