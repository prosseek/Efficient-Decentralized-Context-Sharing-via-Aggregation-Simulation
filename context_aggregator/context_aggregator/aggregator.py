"""aggregator

In this class, we use list as a main container class.
"""
import copy
from utils import *

class Aggregator(object):
    def __init__(self, contexts):
        self.contexts = contexts