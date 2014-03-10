import sys
import unittest
import os.path

# This is a package module that uses relative/absolute path `from .utils import *`
source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context.context import Context

class TestContext(unittest.TestCase):
    def test_simple(self):
        a = Context(value=1.0, cohorts=set([0]))
        b = Context(value=2.0, cohorts=set([1]))
        c = a + b
        self.assertTrue(str(c) == "v(1.5):c([0, 1]):h(-1)")

        
if __name__ == "__main__":
    unittest.main(verbosity=2)