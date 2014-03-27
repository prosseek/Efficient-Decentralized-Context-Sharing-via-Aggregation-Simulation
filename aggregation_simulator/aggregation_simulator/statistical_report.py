from context.context import Context

def calculate_error(val1, val2):
    """val1 is always the correct value to be compared against

    """
    if type(val1) is list and type(val2) is list:
        assert len(val1) == len(val2)
        diff = 0.0
        for i, v1 in enumerate(val1):
            v2 = val2[i]
            diff += calculate_error(v1, v2) # abs(100.0(v1 - v2)/v1)
        return diff/len(val1) # return the average of % error
    else:
        # TODO: Check this error measure is correct
        # http://answers.yahoo.com/question/index?qid=20090616072756AAFSuaG
        if val1 != 0:
            return abs(100.0*(val1 - val2)/val1)
        else:
            if val2 == 0: return 0
            return abs(100.0*(val1 - val2)/val2)


def dict_to_list(dictionary, host_size, default_value='?'):
    """
    >>> d = {1:2, 2:3, 3:5}
    >>> size = 5
    >>> dict_to_list(d,size)
    ['?', 2, 3, 5, '?']
    """
    result = [default_value]*host_size
    for i,v in dictionary.items():
        result[i] = v
    return result

def estimate_average(singles, aggregates):
    """WARNING! It doesn't check the duplicate values in singles/aggregates

    >>> s1 = Context(value = 1.0, cohorts=[0])
    >>> s2 = Context(value = 2.0, cohorts=[1])
    >>> g1 = Context(value = 3.0, cohorts=[2,3,4])
    >>> g2 = Context(value = 4.0, cohorts=[5,6,7])
    >>> estimate_average({s1,s2},{g1,g2})
    3.0
    """
    count = 0
    values = 0

    # singles is a set of singles
    for s in singles:
        assert s.is_single()
        values += s.value
        count += 1

    # aggregates is a list of aggregates
    for a in aggregates:
        assert not a.is_single()
        count += len(a)
        values += (a.value*len(a))

    return 1.0*values/count

def get_identified_values(singles, aggregate, size, shift_index=0):
    """Given singles/aggregates, returns a list

    shift index is needed for node value that doesn't start from 0

    >>> s = {Context(value=3.0, cohorts={1})}
    >>> a = {Context(value=1.0, cohorts={3,5}), Context(value=2.0, cohorts={4,7})}
    >>> get_identified_values(s,a,10)
    ['?', 3.0, '?', '1.00(*)', '2.00(*)', '1.00(*)', '?', '2.00(*)', '?', '?']

    >>> s = {Context(value=3.0, cohorts={1})}
    >>> a = {Context(value=1.0, cohorts={3,5}), Context(value=2.0, cohorts={4,7})}
    >>> get_identified_values(s,a,10,shift_index=1)
    [3.0, '?', '1.00(*)', '2.00(*)', '1.00(*)', '?', '2.00(*)', '?', '?', '?']
    """
    result = ['?']*size
    for s in singles:
        v = s.value
        i = s.get_id()
        i -= shift_index
        result[i] = v
    for a in aggregate:
        items = a.get_cohorts_as_set()
        value = a.value
        for i in items:
            i -= shift_index
            result[i] = "%4.2f(*)" % value
    return result

def get_estimated_values(identified_values, average):
    """

    >>> a = ['?', 3.0, '?', '1.00(*)', '2.00(*)', '1.00(*)', '?', '2.00(*)', '?', '?']
    >>> get_estimated_values(a, 1.6)
    [1.6, 3.0, 1.6, 1.0, 2.0, 1.0, 1.6, 2.0, 1.6, 1.6]
    """

    result = [0]*len(identified_values)
    for i, v in enumerate(identified_values):
        if v == '?':
            result[i] = average
        elif type(v) in [float, int,long]:
            result[i] = v
        else:
            #print v
            result[i] = float(v.split('(')[0])
    return result


def get_cohorts_statistics(identified_aggregates):
    """Given aggregates, returns the number of cohorts (groups), and the number of elements in it

    >>> a = {Context(value=1.0, cohorts={1,2,3}), Context(value=2.0, cohorts={4,5,6,7})}
    >>> no_of_cohorts, no_of_ids = get_cohorts_statistics(a)
    >>> no_of_cohorts == 2 and no_of_ids == 7
    True
    """
    number_of_ids_from_cohorts = 0
    number_of_cohorts = 0
    for s in identified_aggregates:
        number_of_ids_from_cohorts += len(s)
        number_of_cohorts += 1
    return number_of_cohorts, number_of_ids_from_cohorts

class StatisticalReport(object):
    def __init__(self, report_object, timestamp, iteration):
        self.obj = report_object
        self.timestamp = timestamp
        self.iteration = iteration

    def run(self):
        result = ""


        # 1. get the number of received packets
        s,a = self.obj.input.get_number_of_contexts()
        result += "Received: %d (%d-%d)\n" % (s+a, s, a)

        # 2. get the number of sent packets
        s,a = self.obj.output.get_number_of_contexts()
        result += "Sent: %d (%d-%d)\n\n" % (s+a, s, a)

        # 3. calculate the accuracy
        sample = self.obj.get_sample()
        shift_index = sample.get_min()
        host_size = sample.get_host_size()
        if sample is not None:
            correct_values = sample.get_values(self.timestamp)
            result += "Correct values: %s\n" % correct_values
            correct_average = sample.get_average(self.timestamp)
            result += "Correct average: %s\n" % correct_average

            identified_singles = self.obj.get_singles(self.timestamp)
            identified_aggregates = list(self.obj.get_primes()) + list(self.obj.get_selected_non_primes())

            number_of_id_singles = len(identified_singles)
            number_of_cohorts, number_of_ids_from_cohorts = get_cohorts_statistics(identified_aggregates)
            identified_values = get_identified_values(identified_singles, identified_aggregates, host_size, shift_index=shift_index)

            average_number_per_cohort = 0 if number_of_cohorts == 0 else 1.0*number_of_ids_from_cohorts/number_of_cohorts
            number_of_id_aggregate = number_of_ids_from_cohorts + number_of_id_singles

            estimated_average = estimate_average(identified_singles, identified_aggregates)
            estimate_values = get_estimated_values(identified_values, average=estimated_average)
            average_error = calculate_error(correct_average, estimated_average)
            value_error = calculate_error(correct_values, estimate_values)
            result += "Identified values: %s\n" % identified_values
            result += "Estimated average: %s\n" % estimated_average
            result += "Estimated values: %s\n" % estimate_values
            result += "%% precision: avg(%4.2f%%) individual(%4.2f%%)\n" % (100 - average_error, 100 - value_error)
            result += "Identified rate: aggregate(%4.2f%%(%d/%d)) single(%4.2f%%(%d/%d))\n" % \
                      (100.0*number_of_id_aggregate/host_size, number_of_id_aggregate, host_size,
                       100.0*number_of_id_singles/host_size, number_of_id_singles, host_size)
            result += "Average number of cohorts: %4.2f(%d/%d)" % (average_number_per_cohort, number_of_ids_from_cohorts, number_of_cohorts)
        else:
            result += "No sample data found\n"


        return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()