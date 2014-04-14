import os
import shutil

from aggregation_analyzer.utils_location import *
from aggregation_simulator.network import Network

def remove_dirs(test_name):
   r = get_reports_dir()
   s = get_sims_dir()

   for i in [r,s]:
       j = i + os.sep + test_name
       if os.path.exists(j):
           shutil.rmtree(j)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
