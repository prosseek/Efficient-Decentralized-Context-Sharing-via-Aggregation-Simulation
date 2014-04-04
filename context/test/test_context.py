import sys
import unittest
import os.path

# This is a package module that uses relative/absolute path `from .utils import *`
source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context.context import Context

class TestContext(unittest.TestCase):
    def test_deserialize(self):
        c = Context(value=1.0, cohorts={0,1,2})
        s = c.serialize(zipped=True)
        c2 = Context.deserialize(s,zipped=True)
        c == c2

    def test_big_number(self):
        c = Context(value=1.0, cohorts={40000})
        s = c.serialize(zipped=True)
        c2 = Context.deserialize(s,zipped=True)
        c == c2
if __name__ == "__main__":
    unittest.main(verbosity=2)