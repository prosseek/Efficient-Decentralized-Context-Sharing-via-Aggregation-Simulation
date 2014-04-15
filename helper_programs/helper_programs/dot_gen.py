from aggregation_simulator.network import Network

def dot_gen(file_path):
    n = Network(file_path)
    n.dot_gen(file_path + ".dot")

if __name__ == "__main__":
    dot_gen("/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/analysis/pseudo_realworld_49_tree/pseudo_realworld_49_tree.txt")