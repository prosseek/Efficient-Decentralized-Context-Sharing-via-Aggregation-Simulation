"""Analysis of simulation and genration of gnuplot file

"""

class Network(object):
    def __init__(self, network_file=None):
        self.network = {}
        self.network_file = None
        if network_file is not None:
            self.network = self.read(network_file)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
__author__ = 'smcho'
