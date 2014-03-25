import os.path

class SampleData(object):
    def __len__(self):
        return self.get_host_size()

    def get_host_size(self):
        return len(self.sample)

    def __init__(self):
        self.sample = {}

    def __getitem__(self, i):
        """
        >>> root_directory = os.path.dirname(os.path.abspath(__file__)) + "/../test/tmp/"
        >>> base_directory = os.path.join(root_directory, "test1/aggregation/")

        >>> s = SampleData()
        >>> file = os.path.abspath(base_directory + ".." + os.sep + "sample.txt")
        >>> s.read(file)
        >>> s[0]
        [0, 1, 2, 3, 4]
        """
        return self.sample[i]

    def __setitem__(self, key, value):
        self.sample[key] = value

    def read(self, file_path):
        """
        >>> root_directory = os.path.dirname(os.path.abspath(__file__)) + "/../test/tmp/"
        >>> base_directory = os.path.join(root_directory, "test1/aggregation/")

        >>> s = SampleData()
        >>> file = os.path.abspath(base_directory + ".." + os.sep + "sample.txt")
        >>> s.read(file)
        >>> s.sample
        {0: [0, 1, 2, 3, 4], 1: [1, 2, 3, 4, 5], 2: [2, 3, 4, 5, 6]}
        """
        if not os.path.exists(file_path):
            raise RuntimeError("No such file as %s" % file_path)

        with open(file_path, "r") as f:
            lines = f.readlines()
            for l in lines:
                id = int(l.split(":")[0])
                values = [int(i) for i in l.split(":")[1].split(',')]
                self.sample[id] = values
            f.close()

    def get_average(self, index):
        """
        >>> root_directory = os.path.dirname(os.path.abspath(__file__)) + "/../test/tmp/"
        >>> base_directory = os.path.join(root_directory, "test1/aggregation/")

        >>> s = SampleData()
        >>> file = os.path.abspath(base_directory + ".." + os.sep + "sample.txt")
        >>> s.read(file)
        >>> s.get_average(0) == 1.0
        True
        >>> s.get_average(1) == 2.0
        True
        >>> s.get_average(2) == 3.0
        True
        """
        values = self.get_values(index)
        return 1.0*sum(values)/len(values)

    def get_values(self, index):
        """
        >>> root_directory = os.path.dirname(os.path.abspath(__file__)) + "/../test/tmp/"
        >>> base_directory = os.path.join(root_directory, "test1/aggregation/")

        >>> s = SampleData()
        >>> file = os.path.abspath(base_directory + ".." + os.sep + "sample.txt")
        >>> s.read(file)
        >>> s.get_values(0)
        [0, 1, 2]
        >>> s.get_values(1)
        [1, 2, 3]
        >>> s.get_values(2)
        [2, 3, 4]
        """

        assert index < len(self.sample[self.sample.keys()[0]])
        result = []
        sorted_keys = sorted(self.sample)
        for i in sorted_keys:
            value = self.sample[i]
            result.append(value[index])
        return result