import unittest
import sys
import os.path

# This is a utility for context, and it is not exported to users.
# In order to test_files this module, importing it directly (not as a pacakge) from the source is necessary
source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

class TestUtils(unittest.TestCase):
    def test_get_number_of_one(self):
        pass
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)