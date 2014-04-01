#!/usr/bin/env python

import unittest
import sys
import os

suiteString = """
def suite():
    test_suite = unittest.TestSuite()
    {s}
    return test_suite
"""

def getTestNames():
        
    def underscore_to_camelcase(value):
        def camelcase(): 
            while True:
                yield str.capitalize

        c = camelcase()
        return "".join(c.next()(x) if x else '_' for x in value.split("_"))
        
    db = {}
    for dirname, dirnames, filenames in os.walk('./test_for_real_world'):
        for filename in filenames:
            if filename.startswith("__"): continue
            if filename.endswith("pyc") or filename.endswith("class"): continue
            if not filename.startswith("test_for_real_world"): continue
            
            # test_context_history.py -> test_context_history
            file_name_without_extension = os.path.splitext(filename)[0]
            camel_case_name = underscore_to_camelcase(file_name_without_extension)
            db[file_name_without_extension] = camel_case_name

    importString = ""
    test_suiteString = ""
    for (key, value) in db.items():
        importString += "from %s import %s\n" % (key, value)
        test_suiteString += "test_suite.addTest(unittest.makeSuite(%s))\n    " % value
        
    generated_code = "%s%s" % (importString, suiteString.format(s = test_suiteString))
    return generated_code

if __name__ == "__main__":
    sys.path.insert(0,"./test_for_real_world")
    sys.path.insert(0,"./../context")

    #print getTestNames()
    exec(getTestNames())

    unittest.TextTestRunner().run(suite())
