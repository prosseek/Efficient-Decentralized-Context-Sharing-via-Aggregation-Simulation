import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.context_history import ContextHistory
from context_aggregator.output_selector import OutputSelector
from context_aggregator.utils_same import *

class TestOutputSelection(unittest.TestCase):

    def setUp(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)