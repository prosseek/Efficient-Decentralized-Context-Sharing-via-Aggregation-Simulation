import os
from connection_analyzer import *
from aggregation_simulator.network import Network

def generate_network_file(dictionary, file_path, minus_one=False):
    keys = sorted(dictionary)

    with open(file_path, "w") as f:
        for key in keys:
            values = dictionary[key]
            str = ""
            for value in values:
                #print value, values
                value = value -1 if minus_one else value
                str += ("%d " % value)

            str = str[0:len(str)-1] # remove the last ','
            key = key - 1 if minus_one else key
            f.write("%d: %s\n" % (key, str))
        f.close()

def con(location_file, file_path,limit=10):
    result = readLocationFile(location_file)
    #print result
    result = connected(result, connection_limit=limit)
    #print result
    generate_network_file(result, file_path, minus_one=False)
    network = Network()
    network.read(file_path)
    network.dot_gen(file_path + ".dot")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    location_file = os.path.join(current_dir, "mote_locs.txt")
    con(location_file, "network10.txt", 10)
    con(location_file, "network6.txt", 6)
