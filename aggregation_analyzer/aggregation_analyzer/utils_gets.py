# def get_from_key(host_dictionary, key):
#     hosts = host_dictionary.keys()
#
#     result = []
#     for host in hosts:
#         report = host_dictionary[key]
#         values = report[key]
#         result.append(values)
#     return result
#
# def get_sizes(dictionary):
#     keys = sorted(dictionary.keys())
#
#     result_total = []
#     result_single = []
#     result_aggregate = []
#     for key in keys:
#         value = dictionary[key]
#         received = value["Received"]
#         size_total = received[0]
#         size_single = received[1]
#         size_aggregate = received[2]
#         result_total.append(size_total)
#         result_single.append(size_single)
#         result_aggregate.append(size_aggregate)
#     return result_total, result_single, result_aggregate
#
# def get_accuracy(dictionary):
#     keys = sorted(dictionary.keys())
#
#     avg_precision_total = []
#     single_precision_total = []
#
#     for key in keys:
#         value = dictionary[key]
#         received = value["Identified rate"]
#         avg_precision = received[0]
#         single_precision = received[1]
#
#         avg_precision_total.append(avg_precision)
#         single_precision_total.append(single_precision)
#     return avg_precision_total, single_precision_total