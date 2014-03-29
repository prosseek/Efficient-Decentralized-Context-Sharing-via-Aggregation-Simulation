"""Find which node is connected to which node

This code is for data processing for the location file of sensor networks.
The original file is downloaded from [Intel Lab Data](http://db.csail.mit.edu/labdata/labdata.html)
"""
import math

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



if __name__ == "__main__":
    con("net1.txt")