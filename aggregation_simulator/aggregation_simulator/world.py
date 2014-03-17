"""World is a singleton
"""
class Singleton:
    """
    # http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern

    >>> w = World()
    Traceback (most recent call last):
        ...
    TypeError: Singleton should be accessed through instance() method only
    >>> w1 = World.instance()
    >>> w2 = World.instance()
    >>> id(w1) == id(w2)
    True
    >>> w1 is w2
    True
    """
    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self, conf = None):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated(conf)
            return self._instance

    def __call__(self):
        raise TypeError("Singleton should be accessed through instance() method only")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class World(object):
    """World is a singleton, so the two instances should be the same

    """
    def __init__(self, conf):
        self.conf = conf

    def connected(self, from_node, to_node):
        return True

    def send(self, from_node, to_node, timestamp):
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
