"""host.py

Hosts for simulation of the node
"""
from context_aggregator.context_aggregator import ContextAggregator
from aggregation_simulator.world import World

class Host(object):
    """

    >>> h3 = Host(3)
    >>> h3.id == 3
    True
    >>> h1 = Host(1)
    >>> h1.id != h3.id
    True

    h1.world is h3.world
    True
    """
    def __init__(self, id):
        self.id = id
        self.dataflow = ContextAggregator()
        #self.world = World.instance()

    # def send(self, timestamp=0):
    #     output_dictionary = self.dataflow.get_output()
    #     for index in output_dictionary:
    #         from_node = self.id
    #         to_node = index
    #         if self.world.connected(from_node=from_node, to_node=to_node):
    #             contexts = output_dictionary[index]
    #             self.world.send(from_node=from_node, to_node=to_node, contexts=contexts)
    #
    # def receive(self, index, contexts, timestamp=0):
    #     self.dataflow.receive_data(index, contexts)
    #
    # def process(self, timestamp=0):
    #     self.dataflow.run_dataflow(timestamp)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

