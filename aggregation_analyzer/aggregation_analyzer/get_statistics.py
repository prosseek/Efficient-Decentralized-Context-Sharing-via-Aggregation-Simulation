import os

from get_information import GetInformation
from get_processed_information import GetProcessedInformation
from read_reports import ReadReports
from utils_location import get_simple_test_dir

class GetStatistics(object):
    def __init__(self, reports):
        self.reports = reports
        self.get_information = GetInformation(reports)
        self.get_processed_information = GetProcessedInformation(self.get_information)

    def get_size(self, condition, sub_name = None):
        """Given read report object that contains all the network info
        It returns the number of total communication packets

        >>> network_dir = get_simple_test_dir() + os.sep + "test_network1"
        >>> r = ReadReports(network_dir)
        >>> s = GetStatistics(r)
        >>> s.get_size("normal","aggregations") == [31, 14, 17]
        True
        >>> s.get_size("normal","singles") == [56, 56, 0]
        True
        >>> s.get_size("normal") == ([56, 56, 0], [31, 14, 17])
        True
        """
        if sub_name is not None:
            return self.get_processed_information.get_sent_total_sum(condition, sub_name)
        else:
            sub_name = "singles"
            s = self.get_processed_information.get_sent_total_sum(condition, sub_name)
            sub_name = "aggregations"
            a = self.get_processed_information.get_sent_total_sum(condition, sub_name)
            return (s,a)
