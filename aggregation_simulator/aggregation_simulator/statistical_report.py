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
        return abs(100.0*(val1 - val2)/val1)

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
        host_size = sample.get_host_size()
        if sample is not None:
            correct_values = sample.get_values(self.timestamp)
            result += "Correct values: %s\n" % correct_values
            correct_average = sample.get_average(self.timestamp)
            result += "Correct average: %4.2f\n" % correct_average

            d = {}
            identified_singles = self.obj.get_singles(self.timestamp)
            identified_aggregates = list(self.obj.get_primes()) + list(self.obj.get_selected_non_primes())

            number_of_id_singles = len(identified_singles)
            for s in identified_singles:
                v = s.value
                i = s.id
                d[i] = v

            number_of_ids_from_cohorts = 0
            number_of_cohorts = 0
            for s in identified_aggregates:
                number_of_ids_from_cohorts += len(s)
                number_of_cohorts += 1

            average_number_per_cohort = 0 if number_of_cohorts == 0 else 1.0*number_of_ids_from_cohorts/number_of_cohorts
            number_of_id_aggregate = number_of_ids_from_cohorts + number_of_id_singles

            result += "Identified values: %s\n" % dict_to_list(d, host_size)
            estimated_average = estimate_average(identified_singles, identified_aggregates)
            result += "Estimated average: %s\n" % estimated_average
            estimate_values = dict_to_list(d, host_size, default_value=estimated_average)
            result += "Estimated values: %s\n" % estimate_values
            result += "Error rate: avg(%4.2f%%) individual(%4.2f%%)\n" % (calculate_error(correct_average, estimated_average), calculate_error(correct_values, estimate_values))
            result += "Identified rate: aggregate(%4.2f%%(%d/%d)) single(%4.2f%%(%d/%d))\n" % \
                      (100.0*number_of_id_aggregate/host_size, number_of_id_aggregate, host_size,
                       100.0*number_of_id_singles/host_size, number_of_id_singles, host_size)
            result += "Average number of cohorts: %4.2f%%(%d/%d)" % (average_number_per_cohort, number_of_ids_from_cohorts, number_of_cohorts)
        else:
            result += "No sample data found\n"


        return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()