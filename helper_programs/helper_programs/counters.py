import glob
import os
import pprint

def counters(file_path, t):
    result = {}
    files = glob.glob(file_path + os.sep + "*.*")

    for i in range(10, 110, 10):
        tree_count = "%s%d_" % (t, i)
        trees = filter(lambda m: os.path.basename(m).startswith(tree_count) and os.path.basename(m).endswith(".txt"), files)
        result[i] = len(trees)

    pprint.pprint(result)


counters("/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/massive_data/10_100_10_10/tree", "tree")
counters("/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/massive_data/10_100_10_10/mesh", "mesh")
