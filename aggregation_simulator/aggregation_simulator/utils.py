from utils_configuration import *
from network import Network

from sample import Sample

import os
import shutil
import distutils.core
import random

def check_drop(drop_rate):
    """returns True at the rate of drop_rate
    check_drop(0.2)
    """
    # This value should be around 200
    # print len(filter(lambda m: m < drop_rate, [random() for i in range(1000)]))
    return random.random() < drop_rate

if __name__ == "__main__":
    import doctest
    doctest.testmod()