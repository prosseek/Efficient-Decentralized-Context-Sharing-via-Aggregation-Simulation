import unittest
import sys
import os
import time

from aggregation_analyzer.generate_gifs import GenerateGifs
from aggregation_analyzer.read_reports import ReadReports
from aggregation_simulator.utils_configuration import get_configuration
from aggregation_analyzer.utils_location import get_host_names
from aggregation_analyzer.get_information import GetInformation
from aggregation_analyzer.utils_location import *
from aggregation_simulator.network import Network

class TestReadReport(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_reports(self):
        d = get_simple_test_dir() + os.sep + "test_network1"
        r = ReadReports(d)

        t1 = time.clock()
        results = r.read_all(use_cache=False)
        print time.clock() - t1

        t1 = time.clock()
        results = r.read_all(use_cache=True)
        print time.clock() - t1

    def test_read_intel_reports(self):
        d = get_intel_test_dir() + os.sep + "real_world_intel_6"
        r = ReadReports(d)

        t1 = time.time()
        results1 = r.read_all(use_cache=False)
        print time.time() - t1

        t1 = time.time()
        results2 = r.read_all(use_cache=True)
        print time.time() - t1

        print len(results1), len(results2)


if __name__ == "__main__":
    unittest.main(verbosity=2)