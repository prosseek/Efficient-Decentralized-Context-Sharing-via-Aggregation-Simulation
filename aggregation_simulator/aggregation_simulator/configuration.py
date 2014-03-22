"""Configuration file reader and accessor

WARNING: After reading from the configuration file, the contents become read only.

The configuration file has the same format as ONE simulator's.

Example:

# GUI underlay image settings
GUI.UnderlayImage.fileName = data/helsinki_underlay.png

1. # means comment
2. NAMESPACE . ITEM  = value

The value is accessed with:
c = Configuration()
c.read(...)
c.get_int(NAMESPACE, ITEM)

"""
import os
import re
from utils import *

test_config_file = "test_config.txt"

class Configuration(object):
    def __init__(self):
        self.file_path = None
        self.configuration = {}

    def parse_assignment(self, l):
        """

        >>> c = Configuration()
        >>> c.parse_assignment("a = b")
        ('a', 'b')
        >>> c.parse_assignment("a =          b  ")
        ('a', 'b')
        """
        regex = "([^\s=]+)\s*=\s*([^\s]+)"
        g = re.search(regex, l)
        if not g:
            raise AttributeError("Wrong format %s" % l)
        else:
            variable = g.group(1)
            value = g.group(2)
        return variable, value

    def read(self, configuration_file):
        """

        >>> Configuration().read("/dumb")
        Traceback (most recent call last):
        ...
        IOError: No /dumb exists
        >>> Configuration().read("dumb")
        Traceback (most recent call last):
        ...
        IOError: No dumb exists
        >>> c = Configuration()
        >>> c.read(test_config_file)
        >>> c.file_path.endswith(test_config_file)
        True
        """
        # if the configuration is given as an absolute path, and it exists
        if os.path.isabs(configuration_file):
            if not os.path.exists(configuration_file):
                raise IOError("No %s exists" % configuration_file)
            else:
                configuration_path = configuration_file
        else: # it's relative path
            configuration_path = find_configuration_file(configuration_file)
            if configuration_path is None:
                raise IOError("No %s exists" % configuration_file)

        self.file_path = configuration_path

        with open(configuration_path, "r") as f:
            for l in f:
                if l.startswith('#'): continue
                try:
                    variable, value = self.parse_assignment(l)
                    self.configuration[variable] = value
                except AttributeError, e:
                    raise AttributeError(str(e) + "in file %s" % configuration_path)
    def get(self, namespace, key):
        """Return the value from namespace.key in string (raw format)

        >>> c = Configuration()
        >>> c.read(test_config_file)
        >>> c.get("test", "value")
        '15'
        >>> c.get("test", "float_value")
        '15.0'
        """
        key = namespace + "." + key
        if key in self.configuration:
            return self.configuration[key]
        else:
            return None

    def get_int(self, namespace, key):
        """

        >>> c = Configuration()
        >>> c.read(test_config_file)
        >>> c.get_int("test", "value")
        15
        >>> c.get_int("test", "value2")
        """

        result = self.get(namespace, key)
        if result is not None:
            try:
                return int(result)
            except ValueError:
                return None
        else:
            return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()