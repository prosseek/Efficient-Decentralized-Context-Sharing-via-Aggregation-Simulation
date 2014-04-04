#
# Configuration related methods
#

from utils_same import *
import copy

def process_default_values(config, defaults):
    """When the config doesn't specify some critical configuration information, the values are set here

    >>> config={"a":100}
    >>> defaults={"b":200}
    >>> r = process_default_values(config, defaults)
    >>> same(r, {'a': 100, 'b': 200})
    True
    """
    assert defaults is not None

    if config is None:
        result = {}
    else:
        result = copy.copy(config)

    for key in defaults:
        if key not in result:
            result[key] = defaults[key]

    return result

def add_to_config(config1, config2):
    """

    >>> c1 = {'a':100}
    >>> c2 = {'b':200}
    >>> r = add_to_config(c1, c2)
    >>> same(r, {'a': 100, 'b': 200})
    True
    """
    c = copy(config1)
    for i in config2:
        c[i] = config2[i]
    return c

if __name__ == "__main__":
    import doctest
    doctest.testmod()