def starts_with(name, keys):
    """

    >>> keys = ["abc", "def", "xyz"]
    >>> print starts_with("abcdef", keys)
    abc
    >>> starts_with("k", keys)
    """
    for key in keys:
        #if key.startswith(name): return key
        if name.startswith(key): return key
    return None

def readLocationFile(fileName):
    """
    Given locatin file, returns a dictionary that maps id -> [x,y]
    The x,y is measured in meters relative to the upper right corner of the lab.
    """
    result = {}
    with open(fileName, "r") as f:
        # Remove the '\n' 
        lines = map(lambda e: e.strip(), f.readlines())
        for l in lines:
            id, x, y = l.split(' ')
            result[int(id)] = [float(x),float(y)]
        return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()