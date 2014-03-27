from utils_configuration import *
from network import Network

from sample import Sample

import os
import shutil
import distutils.core

def get_sample_name(test_name):
    return test_name + "_sample.txt"

def make_ready_for_test(test_file_name, test_sub_name):
    """Given test name in test_files directory, and sub directory
    Returns the test_directory where the reports are recorded, and the sample file

    >>> result = make_ready_for_test("test1","aggregate")
    >>> len(result) == 2
    True
    """
    test_files_directory = get_test_files_directory()
    directory = os.path.join(test_files_directory, test_file_name)
    sample_name = get_sample_name(test_file_name)
    sample_file_path = os.path.join(directory, sample_name)

    net_file_path = os.path.join(directory, test_file_name + ".txt")
    dot_file_path = net_file_path + ".dot"

    if os.path.exists(net_file_path):
        if not os.path.exists(dot_file_path):
            n = Network(net_file_path)
            dumb = n.dot_gen(dot_file_path)


    # There should be sample files
    assert os.path.exists(sample_file_path)

    # get the target root file
    test_report_root_directory = get_test_report_root_directory()

    test_report_directory = test_report_root_directory + os.sep + test_file_name
    test_report_sub_directory = test_report_directory + os.sep + test_sub_name
    if os.path.exists(test_report_sub_directory):
        shutil.rmtree(test_report_sub_directory)
    os.makedirs(test_report_sub_directory)

    # http://stackoverflow.com/questions/15034151/copy-directory-contents-into-a-directory-with-python
    distutils.dir_util.copy_tree(directory, test_report_directory)

    sample = Sample()
    sample.read(sample_file_path)

    return test_report_sub_directory, sample

if __name__ == "__main__":
    import doctest
    doctest.testmod()