import os
import glob
import re

from aggregation_simulator.utils_configuration import get_test_report_root_directory, get_configuration, CONFIGURATION_FILE_FOR_TEST

def get_host_names(condition, name, kind):
    test_root_dir = get_test_report_root_directory()
    directory = test_root_dir + os.sep + condition + os.sep + name + os.sep + kind + os.sep
    files = os.listdir(directory)

    r = {}
    for file in files:
        base_name = os.path.basename(file)
        p = re.search("host(\d+)", base_name)
        if p:
            r[int(p.group(1))] = p.group(0)

    result = []
    for key in sorted(r.keys()):
        result.append(r[key])
    return result

# def get_report_root_directory():
#     test_root_dir = get_test_report_root_directory()
#     report_dir = os.path.join(test_root_dir, "report")
#     if not os.path.exists(report_dir):
#         os.makedirs(report_dir)
#     return report_dir

def get_test_location(condition, name, kind, host, timestamp=0):
    test_root_dir = get_test_report_root_directory()
    timestamp = "%04d" % timestamp
    return test_root_dir + os.sep + condition + os.sep + name + os.sep + kind + os.sep + host + os.sep + timestamp

def get_img_report_root_directory():
    return get_configuration(CONFIGURATION_FILE_FOR_TEST, "TestDirectory","img_report_root_directory")

if __name__ == "__main__":
    import doctest
    doctest.testmod()