import math

def same_tree(t1, t2):
    """
    >>> t1 = {0:[1,2,3], 1:[0], 2:[0], 3:[0]}
    >>> t2 = {1:[0], 0:[1,2,3], 3:[0], 2:[0]}
    >>> same_tree(t1, t2)
    True
    """
    return unicode(t1) == unicode(t2)

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

def distance(x1, x2):
    """
    Given x, y in a list returns the distance between them
    """
    return math.sqrt((x2[0]-x1[0])**2 + (x2[1]-x1[1])**2)

def connected(dictionary, connection_limit=5):
    """
    Given dictionary, shows what nodes are connected to what node
    """
    result = {}
    for node1, location1 in dictionary.items():
        result[node1] = []
        for node2,location2 in dictionary.items():
            if node1 == node2: continue
            leng = distance(location1, location2)
            #if node1 == 34 and node2 == 35: print leng
            if leng < connection_limit:
                result[node1].append(node2)
            else:
                pass
    return result

def readlines(file_path):
    lines = []
    with open(file_path, "r") as f:
        while True:
            line = f.readline()
            if not line: break
            lines.append(map(float, line.strip().split('\t')))
    return lines

def writelines(file_path, lines):
    with open(file_path, "w") as f:
        for line in lines:
            r = "\t".join(map(str, line))
            f.write(r + "\n")
        f.close()