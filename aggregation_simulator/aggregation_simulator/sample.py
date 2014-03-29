import os.path

class Sample(object):
    def __len__(self):
        return self.get_host_size()

    def get_host_size(self):
        return len(self.sample)

    def __init__(self):
        self.sample = {}

    def __getitem__(self, i):
        """

        [i] works as a dictionary access
        """
        return self.sample[i]

    def __setitem__(self, key, value):
        self.sample[key] = value

    def get_min(self):
        return min(self.sample.keys())

    def parse_sample_data(self, lines):

        sample = {}
        for l in lines:
            if len(l.strip()) == 0: continue
            id = int(l.split(":")[0])

            special_values = []
            values = []
            for i in l.split(":")[1].strip().split(','):
                if i.endswith("(*)"):
                    i = i.replace("(*)","")
                    special_values.append(True)
                else:
                    special_values.append(False)

                values.append(float(i))

            # If there is a special value
            if any(special_values):
                sample[id] = (values, special_values)
            else:
                sample[id] = values
        return sample

    def read(self, file_path):
        """
        >>> root_directory = os.path.dirname(os.path.abspath(__file__)) + "/../test_files/"
        >>> base_directory = os.path.join(root_directory, "normal/test1")

        >>> s = Sample()
        >>> file = os.path.abspath(base_directory + os.sep + "test1_sample.txt")
        >>> s.read(file)
        >>> s.sample == {0: [0.0, 1.0, 2.0, 3.0, 4.0], 1: [1.0, 2.0, 3.0, 4.0, 5.0], 2: [2.0, 3.0, 4.0, 5.0, 6.0]}
        True
        >>> s = Sample()
        >>> file = os.path.abspath(base_directory + os.sep + "test1_sample_with_special.txt")
        >>> s.read(file)
        >>> s.sample == {0: ([0.0, 1.0, 2.0, 3.0, 4.0], [True, False, False, False, False]), 1: ([1.0, 2.0, 3.0, 4.0, 5.0], [False, True, False, False, False]), 2: ([2.0, 3.0, 4.0, 5.0, 6.0], [False, False, True, False, False])}
        True
        """
        if not os.path.exists(file_path):
            raise RuntimeError("No such file as %s" % file_path)

        with open(file_path, "r") as f:
            lines = f.readlines()
            self.sample = self.parse_sample_data(lines)
            f.close()

    def get_average(self, index):
        """
        >>> root_directory = os.path.dirname(os.path.abspath(__file__)) + "/../test_files/"
        >>> base_directory = os.path.join(root_directory, "normal/test1")

        >>> s = Sample()
        >>> file = os.path.abspath(base_directory + os.sep + "test1_sample.txt")
        >>> s.read(file)
        >>> s.get_average(0) == 1.0
        True
        >>> s.get_average(1) == 2.0
        True
        >>> s.get_average(2) == 3.0
        True
        >>> base_directory = os.path.join(root_directory, "marked_sample/test1")
        >>> s = Sample()
        >>> file = os.path.abspath(base_directory + os.sep + "test1_sample.txt")
        >>> s.read(file)
        >>> s.get_average(0) == 1.0
        True
        >>> s.get_average(1) == 2.0
        True
        >>> s.get_average(2) == 3.0
        True
        """
        values = self.get_values(index)

        if type(values) is tuple:
            values = values[0]

        return 1.0*sum(values)/len(values)

    def get_values(self, index):
        """
        >>> root_directory = os.path.dirname(os.path.abspath(__file__)) + "/../test_files/"
        >>> base_directory = os.path.join(root_directory, "normal/test1")

        >>> s = Sample()
        >>> file = os.path.abspath(base_directory + os.sep + "test1_sample.txt")
        >>> s.read(file)
        >>> s.get_values(0)
        [0.0, 1.0, 2.0]
        >>> s.get_values(1)
        [1.0, 2.0, 3.0]
        >>> s.get_values(2)
        [2.0, 3.0, 4.0]

        >>> s = Sample()
        >>> file = os.path.abspath(base_directory + os.sep + "test1_sample_with_special.txt")
        >>> s.read(file)
        >>> s.get_values(0) == ([0.0, 1.0, 2.0],[True,False,False])
        True
        >>> s.get_values(1) == ([1.0, 2.0, 3.0],[False,True,False])
        True
        >>> s.get_values(2) == ([2.0, 3.0, 4.0],[False,False,True])
        True
        >>> s.get_values(3) == [3.0, 4.0, 5.0]
        True
        """
        result = []
        special_result = []
        sorted_keys = sorted(self.sample)
        for i in sorted_keys:
            value = None
            specials = None
            try:
                value, specials = self.sample[i]
            # TODO: Hack
            # when sample data doesn't have the special data, there is no specials
            # and ValueError Exception raised, this is the routine to mimic as if
            # there is a value for speicals.
            except ValueError:
                value = self.sample[i]
                specials = [False] * len(value)
            result.append(value[index])
            special_result.append(specials[index])
        if not any(special_result):
            return result
        else:
            return result, special_result

if __name__ == "__main__":
    import doctest
    doctest.testmod()