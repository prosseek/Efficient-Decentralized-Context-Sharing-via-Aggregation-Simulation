import unittest
import sys
import os

from aggregation_analyzer.utils_read_results import read_results
from aggregation_analyzer.utils_gif import generate_gifs

class TestGif(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple(self):
        r = read_results("real_world_intel_6", "aggregates", "host1", 0, 6)
        print r #["null IO"]
        r = read_results("real_world_intel_6", "aggregates", "host1", 0)
        print r
        print len(r)

    def test_generate_gifs_for_real_world_intel_normal(self):
        for i in range(54):
            host = "host%d" % (i+1)
            generate_gifs("normal","real_world_intel_6", "aggregates", host, 0)
            generate_gifs("normal","real_world_intel_6", "singles", host, 0)
            generate_gifs("normal","real_world_intel_10", "aggregates", host, 0)
            generate_gifs("normal","real_world_intel_10", "singles", host, 0)

    def test_generate_gifs_for_real_world_intel_marked(self):
        for i in range(54):
            host = "host%d" % (i+1)
            generate_gifs("marked_sample","real_world_intel_6", "aggregates", host, 0)
            generate_gifs("marked_sample","real_world_intel_10", "aggregates", host, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)