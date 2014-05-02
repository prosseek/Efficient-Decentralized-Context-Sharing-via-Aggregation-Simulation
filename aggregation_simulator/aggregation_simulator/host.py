import sys
import os

# source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
# sys.path.insert(0, source_location)

from context_aggregator.context_aggregator import ContextAggregator

class Host(object):
    def __init__(self, id, neighbors = None):
        self.id = id
        self.context_aggregator = ContextAggregator(id)
        self.state = "INIT"
        if neighbors is None:
            self.neighbors = []
        else:
            self.neighbors = neighbors

        self.send_history = {}
        self.receive_history = {}
        self.reset_history()

    def is_output_empty(self):
        return self.context_aggregator.output.is_empty()

    def sent_already(self, neighbor):
        return self.send_history[neighbor]

    def reset_history(self):
        for n in self.neighbors:
            self.send_history[n] = False
        for n in self.neighbors:
            self.receive_history[n] = False

    def send_all(self):
        for i in self.send_history.values():
            if i == False: return False
        return True

    def receive_all(self):
        for i in self.receive_history.values():
            if i == False: return False
        return True

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def sample(self):
        self.context_aggregator.sample()

    def send(self, neighbor):
        # set the flag that this node sends context to neighbor
        self.send_history[neighbor] = True
        if self.send_all(): print "Node %s - send all!" % self.id
        return self.context_aggregator.send(neighbor)

    # node.receive(from_node=from_node,contexts=value,timestamp=0)
    def receive(self, from_node, contexts, timestamp=0):
        self.receive_history[from_node] = True
        if self.receive_all(): print "Node %s - receive all!" % self.id
        self.context_aggregator.receive(from_node, contexts)

    # def get_neighbors(self):
    #     return self.neighbors