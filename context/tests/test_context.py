import sys
import unittest
import os.path

# This is a package module that uses relative/absolute path `from .utils import *`
source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context.context import Context

class TestContext(unittest.TestCase):
    def test_simple(self):
        c = Context()
        a = Context()
        assert c == a
        
if __name__ == "__main__":
    unittest.main(verbosity=2)