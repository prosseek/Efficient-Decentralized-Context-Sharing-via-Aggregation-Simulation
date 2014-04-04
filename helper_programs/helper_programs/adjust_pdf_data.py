from sample_from_pdf import *
from utils import *

def get_min_max(lines):
    min_in_list = min(map(min, lines))
    max_in_list = max(map(max, lines))
    return max_in_list, min_in_list

def run(file_path, middle_value, min_value, max_value):
    lines = readlines(file_path)
    #for line in lines:
    max_in_list, min_in_list = get_min_max(lines)

    result = []
    for line in lines:
        r = []
        for l in line:
            if l == middle_value or l == max_in_list or l == min_in_list:
                pass
            if l < middle_value:
                adjust = (1.0*middle_value - min_value)/(1.0*middle_value - min_in_list)*(l - min_in_list) + min_value
            else:
                adjust = (1.0*max_value - middle_value)/(1.0*max_in_list - middle_value)*(l - middle_value) + middle_value
            r.append(adjust)
        result.append(r)
    return result

if __name__ == "__main__":
    file = file5
    r = run(file, 100, 65, 150)
    mn,mx = get_min_max(r)
    print mn, mx
    writelines(file + ".txt", r)