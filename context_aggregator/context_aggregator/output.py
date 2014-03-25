"""input

"""

from context.context import Context
from inputoutput import InputOutput
from utils_standard import contexts_to_standard

class Output(InputOutput):
    """database class

    """
    def __init__(self):
        self.dictionary = {}


if __name__ == "__main__":
    import doctest
    doctest.testmod()


