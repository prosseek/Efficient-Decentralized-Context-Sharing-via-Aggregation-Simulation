__author__ = 'smcho'

class Event(object):
    def __init__(self, time, action, node, source_node=None):
        self.time = time
        self.action = action
        self.node = node
        self.source_node = source_node

    def __str__(self):
        if self.action == "receive":
            return "@[{0}]: node ({1} -> {2}) {3}".format(self.time, self.source_node.id, self.node.id, self.action)
        else:
            return "@[{0}]: node ({1}) {2}".format(self.time, self.node.id, self.action)