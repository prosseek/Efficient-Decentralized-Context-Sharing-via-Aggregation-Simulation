import unittest
import sys
import os

from aggregation_analyzer.utils_read_reports import read_hosts_reports, get_data_from_iteration_key
from aggregation_analyzer.utils_gif import generate_gifs
from aggregation_analyzer.utils_gets import *
from aggregation_analyzer.utils_location import *

# real_world_intel_10
# avg - 92.59%
# avg - 100.00%
# aggr sum - 2358.00
# aggr sum - 17188.00
# rate - 728.92% (13.7%)

# real_world_intel_6
# avg - 95.51%
# avg - 100.00%
# aggr sum - 1668.00
# aggr sum - 5975.00
# rate - 358.21% (28%)

def get_count_from_key(hosts_reports, key): # condition, name, kind, timestamp, key):
    #hosts_reports = read_hosts_reports(condition, name, kind, timestamp)
    result = {}
    for host in hosts_reports.keys():
        iteration_report = hosts_reports[host]

        data = get_data_from_iteration_key(iteration_report, key)
        result[host] = data
    return result

def sum_lists(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,3],[1,2,3]]
    >>> sum_lists(input) == [3,6,9]
    True
    """
    return map(sum, zip(*input))

def sum_host_values_from_key(conditions, key):
    result = []
    hosts_reports = read_hosts_reports(**conditions)
    # 1. get the Received data (real communication) and sum it up.
    r = get_count_from_key(hosts_reports, key)
    hosts = get_host_names(**conditions)
    for host in hosts:
        result.append(sum_lists(r[host]))
    return result

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        conditions = {"condition":"normal", "name":"real_world_intel_10", "kind":"aggregates"} #, "timestamp":0}
        print sum_host_values_from_key(conditions, "Received")
        print sum_host_values_from_key(conditions, "Sent")
    #     r = []
    #     host_names = get_host_names("normal", real_world, "aggregates")
    #     for h in host_names:
    #         results = read_results("normal", real_world, "aggregates", h, 0)
    #         results = get_sizes(results)
    #         # Results are ([..],[..],[..]) <- sum, single, aggregates
    #         #print "%s-%d" % (h, sum(results[0]))
    #         r.append(sum(results[0]))
    #     x = sum(r)
    #     print "aggr sum - %4.2f" % x
    #
    #     r = []
    #     host_names = get_host_names("normal", real_world, "singles")
    #     for h in host_names:
    #         results = read_results("normal", real_world, "singles", h, 0)
    #         results = get_sizes(results)
    #         # Results are ([..],[..],[..]) <- sum, single, aggregates
    #         #print "%s-%d" % (h, sum(results[0]))
    #         r.append(sum(results[0]))
    #     y = sum(r)
    #     print "aggr sum - %4.2f" % y
    #
    #     print ("rate - %4.2f%%" % (100.0*y/x))
    #
    # def test_get_accuracy(self):
    #     r = []
    #     host_names = get_host_names("normal", real_world, "aggregates")
    #     for h in host_names:
    #         results = read_results("normal", real_world, "aggregates", h, 0)
    #         results = get_accuracy(results)
    #         r.append(results[0][-1])
    #         # Results are ([..],[..],[..]) <- sum, single, aggregates
    #         #print "%s-%d" % (h, sum(results[0]))
    #
    #     x = sum(r)/len(r)
    #     print "avg - %4.2f%%" % x
    #
    #     r = []
    #     host_names = get_host_names("normal", real_world, "singles")
    #     for h in host_names:
    #         results = read_results("normal", real_world, "singles", h, 0)
    #         results = get_accuracy(results)
    #         r.append(results[0][-1])
    #         # print results[0][-1]
    #         # Results are ([..],[..],[..]) <- sum, single, aggregates
    #         #print "%s-%d" % (h, sum(results[0]))
    #
    #     x = sum(r)/len(r)
    #     print "avg - %4.2f%%" % x

if __name__ == "__main__":
    unittest.main(verbosity=2)