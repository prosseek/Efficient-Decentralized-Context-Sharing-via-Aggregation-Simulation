class World(object):
    def __init__(self):
        pass

    def update_hosts(self):
        pass

    def update(self):
        self.update_hosts()

if __name__ == "__main__":
    import doctest
    doctest.testmod()