from copy import copy

from aggregation_analyzer.read_reports import read_hosts_reports, get_data_from_iteration_key
from aggregation_analyzer.utils_location import *

def get_count_from_key(hosts_reports, key): # condition, name, kind, timestamp, key):
    #hosts_reports = read_hosts_reports(condition, name, kind, timestamp)
    result = {}
    for host in hosts_reports.keys():
        iteration_report = hosts_reports[host]

        data = get_data_from_iteration_key(iteration_report, key)
        result[host] = data
    return result

def sum_lists(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,3],[1,2,3]]
    >>> sum_lists(input) == [3,6,9]
    True
    """
    return map(sum, zip(*input))

def avg_lists(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,3],[1,2,3]]
    >>> avg_lists(input) == [1,2,3]
    True
    """
    r = map(sum, zip(*input))
    length = len(input)
    return map(lambda m: m/length, r)

def max_lists(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,5],[7,2,3]]
    >>> max_lists(input) == [7,2,5]
    True
    """
    r = map(lambda m: max(m), zip(*input))
    return r

def min_lists(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,5],[7,2,3]]
    >>> min_lists(input) == [1,2,3]
    True
    """
    r = map(lambda m: min(m), zip(*input))
    return r

def last_lists(input):
    """Sums a list of list column by column

    >>> input = [[1,2,3],[1,2,3],[1,2,3]]
    >>> last_lists(input) == [3,3,3]
    True
    """
    return map(lambda m: m[-1], input)

def get_hosts_and_reports(conditions, key):
    hosts_reports = read_hosts_reports(**conditions)
    r = get_count_from_key(hosts_reports, key)
    hosts = get_host_names(**conditions)
    return hosts, r

def sum_host_values_from_key(conditions, key):
    hosts, r = get_hosts_and_reports(conditions, key)
    result = []
    for host in hosts:
        result.append(sum_lists(r[host]))
    return result

def get_host_values_from_key(conditions, key, index):
    hosts, r = get_hosts_and_reports(conditions, key)
    result = []
    for host in hosts:
        result.append(r[host][index])
    return result

def last_host_values_from_key(conditions, key):
    return get_host_values_from_key(conditions, key, -1)

def first_host_values_from_key(conditions, key):
    return get_host_values_from_key(conditions, key, 0)

def get_index_with_true(input):
    """
    This example stops after 6 steps
    >>> input = [False, False, False, False, False, False, True, True, True]
    >>> get_index_with_true(input)
    6
    >>> input = [False, False, False, False, False, False, False, True, True]
    >>> get_index_with_true(input)
    7
    >>> input = [False, True, False, False, False, False, False, True, True]
    >>> get_index_with_true(input)
    7
    """
    reversed_input = copy(input)
    reversed_input.reverse()
    result = -1
    for i, value in enumerate(reversed_input):
        if value == False:
            result = i
            break
    if result == -1: raise RuntimeError("Input error: all values are True %s" % input)
    return len(input) - i

def last_non_null_host_values_from_key(conditions):
    hosts, r = get_hosts_and_reports(conditions, "null IO")
    result = []
    for host in hosts:
        last_value = get_index_with_true(r[host])
        result.append(last_value)
    return result