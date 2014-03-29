import unittest
import sys
import os

from aggregation_analyzer.utils_read_results import read_results
from aggregation_analyzer.utils_gif import generate_gifs
from aggregation_analyzer.utils_gets import *
from aggregation_analyzer.utils_location import *

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_context_count(self):
        # Read packet counts
        # read_results(condition, name, kind, host, timestamp, iteration = None):
        host_names = get_host_names("normal", "real_world_intel_10", "aggregates")
        for h in host_names:
            results = read_results("normal", "real_world_intel_10", "aggregates", h, 0)
            results = get_sizes(results)
            # Results are ([..],[..],[..]) <- sum, single, aggregates
            print "%s-%d" % (h, sum(results[0]))

if __name__ == "__main__":
    unittest.main(verbosity=2)