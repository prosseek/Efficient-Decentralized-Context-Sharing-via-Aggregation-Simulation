import unittest
import sys
import os

from aggregation_analyzer.generate_gifs import GenerateGifs
from aggregation_analyzer.read_reports import ReadReports
from aggregation_analyzer.get_information import GetInformation
from aggregation_analyzer.utils_location import *

class TestGif(unittest.TestCase):
    def setUp(self):
        pass

    # def test_simple(self):
    #     r = read_results("real_world_intel_6", "aggregates", "host1", 0, 6)
    #     print r #["null IO"]
    #     r = read_results("real_world_intel_6", "aggregates", "host1", 0)
    #     print r
    #     print len(r)

    def test_generate_gifs_for_real_world_intel_normal(self):
        intel_test_root_dir = get_intel_test_dir()
        network_name = "real_world_intel_6"
        network_dir = os.path.join(intel_test_root_dir, network_name)
        #GenerateGifs.generate_gifs(network_dir, "normal", "aggregates")
        #GenerateGifs.generate_gifs(network_dir, "normal", "singles")
        GenerateGifs.generate_gifs(network_dir, "threshold_5", "aggregates")

if __name__ == "__main__":
    unittest.main(verbosity=2)