"""
{'disseminate_abnormal':
    {'aggregation':
        {'host7':
            {0:
"""
import os

from utils_location import get_simple_test_dir
from read_reports import ReadReports

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