"""Given a pseudo real life data with size X,Y,
this program generates a location file (mote_locs.txt) and
"""
import os
import random
from utils import *

current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_dir = current_dir + os.sep + ".." + os.sep + "mote_loc_data" + os.sep + "pdf"
file1 = os.path.join(pdf_dir, "alpha_0.1.txt")
file5 = os.path.join(pdf_dir, "alpha_0.5.txt")
ad_file1 = os.path.join(pdf_dir, "alpha_0.1.txt.txt")
ad_file5 = os.path.join(pdf_dir, "alpha_0.5.txt.txt")

loc_data = os.path.join(pdf_dir, "mote_locs.txt")
sample_data = os.path.join(pdf_dir, "sensor.500.txt")

def get_position(length, count):
    """

    >>> length = 10
    >>> count = 2
    >>> result = get_position(length, count)
    >>> len(result) == 2
    True
    """
    # 1. find count locations
    partition_length = length / count

    r = []
    for i in range(count):
        start = i * partition_length
        end = start + partition_length - 1
        middle = 1.0*(start + end)/2.0
        position = middle

        r.append(position)
    return r

def get_disturbance(disturbance_range = 1.0):
    # shift data to have a range from -0.5 to 0.5
    r = random.random() - 0.5
    # amplify it
    result = r*disturbance_range
    return result

def get_index_position(position, length):
    """

    >>> get_index_position(3.5, 10)
    4
    >>> get_index_position(-2.0, 10)
    0
    >>> get_index_position(10.5, 10)
    9
    """
    new_postion = int(position + 0.5)
    if new_postion < 0: new_postion = 0
    if new_postion >= length: new_postion = length - 1
    return new_postion

def get_positions(length, count, disturbance_range=1.0):
    """

    >>> length = 10
    >>> count = 2
    >>> result, result2 = get_positions(length, count)
    >>> len(result) == 2*2
    True
    >>> len(result2) == 2*2
    True
    """
    x = get_position(length, count)
    y = get_position(length, count)

    result = []
    result2 = []
    # maximum value 1.0 will shift the location by this value
    for j, y_val in enumerate(y):
        for i, x_val in enumerate(x):
            disturbance = get_disturbance(disturbance_range)
            x_position = x_val + disturbance
            x_int_position = get_index_position(x_position, length)
            disturbance = get_disturbance(disturbance_range)
            y_position = y_val + disturbance
            y_int_position = get_index_position(y_position, length)
            result.append((x_position, y_position))
            result2.append((x_int_position, y_int_position))
    return result, result2

def run():
    """
    >>> run()
    """
    print pdf_dir
    loc_data = os.path.join(pdf_dir, "mote_locs_49.txt")
    sample_data = os.path.join(pdf_dir, "sensor.49.txt")
    lines = readlines(ad_file5)

    row_count = len(lines)
    col_count = len(lines[0])
    # 50 -> 50x50 = 2500
    # 22 -> 22x22 = 484
    res, res2 = get_positions(row_count, 7, disturbance_range=3.0)

    f_loc = open(loc_data, "w")
    f_sample = open(sample_data, "w")

    for i, val in enumerate(res2):
        x = val[0]
        y = val[1]
        value = lines[y][x]
        host = i + 1
        f_loc.write("%d %d %d\n" % (host, x, y))
        f_sample.write("%d: %5.3f\n" % (host, value))

    f_loc.close()
    f_sample.close()
if __name__ == "__main__":
    import doctest
    doctest.testmod()