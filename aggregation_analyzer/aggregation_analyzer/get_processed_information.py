import os
import operator

from utils import sum_lists_column
from utils_location import get_simple_test_dir
from read_reports import ReadReports
from get_information import GetInformation

class GetProcessedInformation(object):
    def __init__(self, info):
        self.info = info

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
        >>> info = GetProcessedInformation(GetInformation(ReadReports(d), use_cache=False))
        >>> info.get_sent_total_sum("normal","singles") == [56,56,0]
        True
        """
        results = []
        r = self.info.get_sent(condition, sub_name)
        v = self.get_sum_hosts(r)
        return sum_lists_column(v)


    def get_received_total_sum(self, condition, sub_name):
        """
        >>> d = get_simple_test_dir() + os.sep + "test_network1"
        >>> info = GetProcessedInformation(GetInformation(ReadReports(d), use_cache=False))
        >>> info.get_received_total_sum("normal","singles") == [56,56,0]
        True
        """
        results = []
        r = self.info.get_received(condition, sub_name)
        r = self.get_sum_hosts(r)
        return sum_lists_column(r)

if __name__ == "__main__":
    import doctest
    doctest.testmod()