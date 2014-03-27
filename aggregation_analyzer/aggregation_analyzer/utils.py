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