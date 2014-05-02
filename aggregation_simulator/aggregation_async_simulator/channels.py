__author__ = 'smcho'

class Channels(object):
    def __init__(self, network):
        self.channels = list(Channels.build_channels(network))
        self.in_use = []

    def __str__(self):
        return "AVAILABLE: " + str(self.channels) + "IN_USE" + str(self.in_use)

    @staticmethod
    def build_channels(network):
        """
        >>> network = {1:[2], 2:[1,3], 3:[2]}
        >>> print Channels.build_channels(network)
        set(['[1, 2]', '[2, 3]'])
        """
        nodes = network.keys()
        result = set()
        for node in nodes:
            neighbors = network[node]
            for neighbor in neighbors:
                pair = str(sorted([node, neighbor]))
                result.add(pair)
        return result

    def use(self, from_node, to_node):
        """
        >>> network = {1:[2], 2:[1,3], 3:[2]}
        >>> c = Channels(network)
        >>> c.available(1,2)
        True
        >>> c.use(1,2)
        >>> c.available(1,2)
        False
        >>> c.restore(1,2)
        >>> c.available(1,2)
        True
        """
        pair = str(sorted([from_node, to_node]))
        if pair in self.channels:
            self.in_use.append(pair)
            self.channels.remove(pair)

    def restore(self, from_node, to_node):
        pair = str(sorted([from_node, to_node]))
        if pair in self.in_use:
            self.channels.append(pair)
            self.in_use.remove(pair)

    def available(self, from_node, to_node):
        pair = str(sorted([from_node, to_node]))
        return pair in self.channels

if __name__ == "__main__":
    import doctest
    doctest.testmod()