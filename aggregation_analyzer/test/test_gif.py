import unittest
import sys
import os

from aggregation_analyzer.generate_gifs import GenerateGifs
from aggregation_analyzer.read_reports import ReadReports
from aggregation_simulator.utils_configuration import get_configuration
from aggregation_analyzer.utils_location import get_host_names
from aggregation_analyzer.get_information import GetInformation

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

        intel_test_root_dir = get_configuration("config.cfg","TestDirectory","intel_test_root_dir")
        network_name = "real_world_intel_6"
        network_dir = os.path.join(intel_test_root_dir, network_name)

        get_info = GetInformation(ReadReports(network_dir).read())
        hosts = get_info.get_hosts()

        g = GenerateGifs("%s/experiment" % network_name)
        host = hosts[0]

        values = get_info.get_iterations("normal", "aggregates", host, "Estimated values")
        for value in values:
            g.generate_gif(id_value, host + ".gif")

        # for i in range(54):
        #     host = "host%d" % (i+1)
        #     generate_gifs("normal","real_world_intel_6", "aggregates", host, 0)
        #     generate_gifs("normal","real_world_intel_6", "singles", host, 0)
        #     generate_gifs("normal","real_world_intel_10", "aggregates", host, 0)
        #     generate_gifs("normal","real_world_intel_10", "singles", host, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)