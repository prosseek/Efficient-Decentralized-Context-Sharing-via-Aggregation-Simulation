"""context history

Takes care of anything related to context history sent and received
Assume all the data is in standard format
"""

from context.context import Context
from utils_same import *
import copy

class ContextHistory(object):
    """database class"""
    HOST_INDEX=-1
    class Container(object):
        """
        This is the information for one timestamp

        host maps to two sets of integer
        HOST_INDEX means the aggregation and single contexts so far

        example)
        node -1 -> [[1,3,4],[6,7,8,9,10])
        node 1 -> [[1,2,3],[5,7,8]]
        ...

        """

        def __init__(self):
            self.dictionary = {}

        def set(self, index, value):
            self.dictionary[index] = value

        def get(self, index):
            if index in self.dictionary:
                return self.dictionary[index]
            else:
                None

        def get_keys(self):
            return self.dictionary.keys()

        def to_string(self, display_mode=0, timestamp=""):
            keys = sorted(self.get_keys())
            result = ""
            for key in keys:
                context_ids = self.get(key)
                if key == ContextHistory.HOST_INDEX:
                    key_symbol = "*"
                else:
                    key_symbol = str(key)

                result += "%s:%s:[%s%s]\n" % (timestamp, key_symbol, str(sorted(list(context_ids[0]))), str(sorted(list(context_ids[1]))))
            result = result.replace(" ","")
            return result[0:len(result)-1]

    def __init__(self):
        """

        context_history is a map from node_id -> Container
        """
        self.context_history = {}

    def __str__(self):
        pass

    def to_string(self, display_mode=0, timestamp=None):
        """
        >>> h = ContextHistory()
        >>> h.set_history(ContextHistory.HOST_INDEX, [[0,1,10],[2,3,5,6]], timestamp=100)
        >>> h.set_history(1, [[1,2,3],[4,5,6,7]], timestamp=100)
        >>> h.set_history(2, [[1,2,3,5],[4,5,7,9]], timestamp=100)
        >>> print h.to_string(timestamp=100)
        100:*:[[0,1,10][2,3,5,6]]
        100:1:[[1,2,3][4,5,6,7]]
        100:2:[[1,2,3,5][4,5,7,9]]
        >>> h.set_history(ContextHistory.HOST_INDEX, [[0,1,10],[2,3,5,6]], timestamp=10)
        >>> h.set_history(1, [[1,2,3],[4,5,6,7]], timestamp=10)
        >>> h.set_history(2, [[1,2,3,5],[4,5,7,9]], timestamp=10)
        >>> print h.to_string()
        10:*:[[0,1,10][2,3,5,6]]
        10:1:[[1,2,3][4,5,6,7]]
        10:2:[[1,2,3,5][4,5,7,9]]
        100:*:[[0,1,10][2,3,5,6]]
        100:1:[[1,2,3][4,5,6,7]]
        100:2:[[1,2,3,5][4,5,7,9]]
        """
        sorted_key = sorted(self.context_history)
        if timestamp is None:
            result = ""
            for t in sorted_key:
                result += (self.to_string(display_mode=display_mode, timestamp=t) + "\n")
            return result[0:len(result)-1]

        elif timestamp == -1:
            if len(sorted_key) > 0:
                return self.to_string(display_mode=display_mode, timestamp=sorted_key[-1])
        else:
            container = self.context_history[timestamp]
            return container.to_string(timestamp=timestamp, display_mode=display_mode)

    #
    # Set/Get method
    #

    def add_to_history(self, node_number, value, timestamp=0):
        """
        appends the value of timestamp:node_number

        >>> h = ContextHistory()
        >>> input = [[0,1,2],[3,4,5,6,7]]
        >>> h.add_to_history(1, input, timestamp=10)
        >>> input = [[3,4,5],[3,4,5,6,7,8,9]]
        >>> h.add_to_history(1, input, timestamp=10)
        >>> same(h.get_history(node_number=1, timestamp=10),[[0, 1, 2, 3, 4, 5], [3, 4, 5, 6, 7, 8, 9]])
        True
        """
        container = self.check_and_get_container(timestamp)
        result = copy.copy(container.get(node_number))

        # Well, is it a good idea to have a None as a return value or specific data structure([[],[]])?
        # I guess, the most important thing is consistency. For this project, I chose to return None, so be careful
        # about the return value and do the proper conversion
        if result is None:
            result = [[],[]]
        singles = sorted(list(set(result[0]) | set(value[0])))
        aggregate = sorted(list(set(result[1]) | set(value[1])))
        self.set_history(node_number, [singles, aggregate], timestamp=timestamp)


    def set_history(self, node_number, value, timestamp=0):
        """

        set the history with value
        """
        assert type(value) is list
        assert type(value[0]) is list and type(value[1]) is list

        container = self.check_and_get_container(timestamp)
        container.set(node_number, value)

    def get(self, timestamp=0):
        """Returns the dictionary in standard format
        ex: {1:[[...],[...]], ...}

        >>> h = ContextHistory()
        >>> input = [[0,1,2],[3,4,5,6,7]]
        >>> h.set_history(ContextHistory.HOST_INDEX, input)
        >>> r = h.get()
        >>> same(r, {ContextHistory.HOST_INDEX:input})
        True
        """
        container = self.get_container(timestamp=timestamp)
        if container is not None:
            return container.dictionary
        return {}

    def set(self, dictionary, timestamp=0):
        """

        >>> h = ContextHistory()
        >>> input = {0:[[0,1,2],[3,4,5,6,7]]}
        >>> h.set(input, 5)
        >>> r = h.get(timestamp=5)
        >>> same(r, input)
        True
        """
        assert type(dictionary) is dict
        if timestamp not in self.context_history:
            self.context_history[timestamp] = ContextHistory.Container()
        self.get_container(timestamp).dictionary = dictionary

    def get_history(self, node_number, timestamp=0):
        """

        >>> h = ContextHistory()
        >>> input = [[0,1,2],[3,4,5,6,7]]
        >>> h.set_history(ContextHistory.HOST_INDEX, input)
        >>> r = h.get_history(ContextHistory.HOST_INDEX)
        >>> same(r, input)
        True
        >>> h.get_history(3, timestamp=5)
        >>> h.get_history(3)
        """
        container = self.get_container(timestamp=timestamp)
        if container is not None:
            return container.get(node_number)
        return None

    def get_container(self, timestamp=0):
        """Returns the container for timestamp

        Returned None means that there is no timestamp for it.
        """
        if timestamp in self.context_history:
            return self.context_history[timestamp]
        return None

    def check_and_get_container(self, timestamp=0):
        """
        It's get_container function, but it creates the container when there is none
        """
        if timestamp not in self.context_history:
            self.context_history[timestamp] = ContextHistory.Container()
        return self.get_container(timestamp)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

