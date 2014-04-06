import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../helper_programs"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from utils import *
from generate_network import *

class TestGenerateNetwork(unittest.TestCase):

    def setUp(self):
        pass

    def test_gen_pdf_sample(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        location_file = os.path.join(current_dir + os.sep + "../mote_loc_data/pdf", "mote_locs.2500.txt")
        con(location_file, "network14.txt", 14)

if __name__ == "__main__":
    unittest.main(verbosity=2)