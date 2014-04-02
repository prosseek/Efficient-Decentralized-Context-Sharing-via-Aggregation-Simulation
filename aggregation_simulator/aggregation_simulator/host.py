import sys
import os

# source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
# sys.path.insert(0, source_location)

from context_aggregator.context_aggregator import ContextAggregator

class Host(object):
    def __init__(self, id):
        self.id = id
        self.context_aggregator = ContextAggregator(id)