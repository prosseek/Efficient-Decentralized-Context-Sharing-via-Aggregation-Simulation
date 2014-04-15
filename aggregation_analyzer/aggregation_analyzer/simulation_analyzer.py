"""
For N data that has this format, get the average
avg={   'accuracy': [[100.0, 40.132999999999996]],
    'cohorst': [[7.0, 7, 0]],
    'identification_rate': [[100.0, 10, 10, 30.0, 3, 10]],
    'size': [([35, 20, 15], [35, 20, 15])],
    'speed': [[2.2, 2, 3]]}

{'identification_rate': {10: ((100.0, 100.0), (100.0, 100.0)),
                         20: ((100.0, 100.0), (100.0, 100.0)),
((100,0, 100.0) <- singles only com
 (100.0, 22.40) <- aggregations com (total rate, rate only with singles)

 'speed': {10: (11.084099999999992, 11.084099999999992),
           20: (4.6905, 4.6905),
 <- average speed for singles and aggregates (always singles first)
"""

import os
import glob
import pprint

from utils import avg_lists_column

def get_rate(key, lists, index):
    results = []
    for l in lists:
        #print l
        # {'identification_rate': [[100.0, 100, 100, 100.0, 100, 100]],
        # {'identification_rate': [95.05199999999999, 94, 100, 7.109, 6, 100]
        if type(l[key][0]) in (list, tuple):
            value = l[key][0]
        else:
            value = l[key]

        results.append(value[index])
    avg1 = 1.0*sum(results)/len(results)
    return avg1

def get_identification_rate(lists):
    # 'identification_rate': [[100.0, 10, 10, 30.0, 3, 10]]
    #  returns 0th and 3rd element average
    return (get_rate('identification_rate', lists, 0), get_rate('identification_rate', lists, 3))

def get_speed_rate(lists):
    return get_rate('speed', lists, 0)

def get_cohorts_rate(lists):
    return get_rate('cohorst', lists, 0)

def get_accuracy(lists):
    return (get_rate('accuracy', lists, 0), get_rate('accuracy', lists, 1))

def get_size(lists):
    #    'size': [([35, 20, 15], [35, 20, 15])],
    sends = []
    receives = []
    for l in lists:
        # There are two possibilities
        # 'size': ([78, 32, 46], [78, 32, 46]),
        # 'size': [([218, 218, 0], [218, 218, 0])],
        if type(l['size'][0][0]) in (list, tuple):
            value = l['size'][0]
        else:
            value = l['size']

        #print l['size']
        #value = l['size'][0]
        send_size = value[0]
        receive_size = value[1]

        sends.append(send_size)
        receives.append(receive_size)

    avg1 = avg_lists_column(sends)
    avg2 = avg_lists_column(receives)

    return avg1, avg2

class SimulationAnalyzer(object):
    def __init__(self, directory):
        pass

    def exec_file(self, file_path, globals):
        with open(file_path, "r") as f:
            result = f.read()
            f.close()
        exec(result) in globals

if __name__ == "__main__":
    pass