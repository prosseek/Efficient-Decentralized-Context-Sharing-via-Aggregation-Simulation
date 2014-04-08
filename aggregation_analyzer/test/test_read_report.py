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
        t1 = time.time()
        r = ReadReports(d, auto_read = False, use_cache = False)
        results1 = r.read_all(use_cache=False)
        time1 = time.time() - t1


        t1 = time.time()
        r = ReadReports(d, auto_read = False, use_cache = True)
        results2 = r.read_all(use_cache=True)
        time2 = time.time() - t1

        print "For test real_world_intel_6"
        print time1, time2
        print "--------------"


if __name__ == "__main__":
    unittest.main(verbosity=2)