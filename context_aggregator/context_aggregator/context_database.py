"""context database

"""

class ContextDatabase(object):
    """database class"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.singles = None
        self.aggregates = None

    def update(self, singles, aggregates):
        self.singles = singles
        self.aggregates = aggregates


if __name__ == "__main__":
    import doctest
    doctest.testmod()


