def get_sizes(dictionary):
    keys = sorted(dictionary.keys())

    result_total = []
    result_single = []
    result_aggregate = []
    for key in keys:
        value = dictionary[key]
        received = value["Received"]
        size_total = received[0]
        size_single = received[1]
        size_aggregate = received[2]
        result_total.append(size_total)
        result_single.append(size_single)
        result_aggregate.append(size_aggregate)
    return result_total, result_single, result_aggregate