import random
import sys
import copy

from aggregation_simulator.network import Network

class TreeGen:
    def __init__(self): 
        pass

    @staticmethod
    def get_depth(tree):
        last_element = tree[len(tree)-1]
        #print last_element
        parent = last_element[1]
        depth = 0

        while parent is not None:
            index = tree.index(filter(lambda x: x[0] == parent, tree)[0])
            #print index
            parent = tree[index][1]
            depth += 1
        return depth
        
    def _generate(self, node_size, max_depth, max_width):
        self.node_size = node_size
        self.max_width = max_width
        self.max_depth = max_depth
        
        # depth is in (1 .. max_depth - 1)
        # When users give max_depth 3, users expect the range from 1 to 3 (not 0 to 2)
        # Instead of depth = random.randrange(1, self.max_depth+1)
        depth = random.randrange(self.max_depth) + 1
        tree = []
        index = 0
        tree.append((0, None))
        count = 1  # There is 1 node
        current_depth = 1
        parent = 0
        
        while count < node_size and current_depth <= depth:
            width = random.randrange(self.max_width)

            current_depth = TreeGen.get_depth(tree)
            # critical condition
            # When depth + 1 is the same as current generated node
            # The width should be 1
            if (current_depth + 1) == count and width == 0:
                width = 1
            
            if width > 0:
                if count + width > node_size:
                    width = node_size - count
                
                for j in range(width):  
                    tree.append((count, parent))
                    count += 1
                
            index += 1
            current_depth = TreeGen.get_depth(tree)
                        
            if index < len(tree):
                parent = tree[index][0]
            else:
                raise Exception("not enough node generated")
                
        return tree, depth
        
    def generate(self, node_size, max_depth, max_width, max_attempt = 5):
        assert node_size > 0
        assert max_depth != 1
        assert max_width != 1
        max_node_size = (max_width**max_depth - 1)/(max_width - 1)
        if max_node_size < node_size:
            print >>sys.stderr, "Increase the width or depth"
            #sys.exit(0)
            raise Exception("Too much node to create")
        #print max_width
        tree = []
        count = 0
        while count < max_attempt:
            try:
                tree, depth = self._generate(node_size, max_depth=max_depth, max_width=max_width)
                generated_tree_size = len(tree)
                if generated_tree_size == node_size:
                    return tree, depth
            except Exception, e:
                count += 1
        return [], 0

    @staticmethod
    def format_converter(tree):
        """
        The tree as an input is the format [(0,None), (1,0)...]
        This code converts this format into the dictionary tree format
        {0:[1,2], 1:[3,4] ...}
        """
        result = {}
        for element in tree:
            node = element[0]
            parent = element[1]
            # find the elements in a tree whose parent is this node
            nodes = filter(lambda x: x[1] == node, tree)
            if len(nodes):  # When connection is found
                result[node] = []
                for n in nodes:
                    result[node].append(n[0])
        return result

    @staticmethod
    def get_two_node_values(range):
        a = 1
        b = 1
        while a == b:
            a = random.randrange(1, range+1)
            b = random.randrange(1, range+1)

        return min(a,b), max(a,b)

    @staticmethod
    def get_new_link_set_from_tree(tree, number_of_links):
        """
        Given a tree (in a dictionary format), return a set of nodes in a tuple format (FROM, TO)
        that has `number_of_links` elements
        """
        iteration_count = 0
        node_size = len(tree)

        result = set()
        while len(result) < number_of_links:
            iteration_count += 1
            node1, node2 = TreeGen.get_two_node_values(node_size)
            if not TreeGen.linked_nodes(tree, node1, node2):
                result.add((node1, node2))

            if iteration_count > node_size:
                print >> sys.stderr, "node_size(%d) iter_count(%d)" % (node_size, iteration_count)
                raise Exception("Too many iterations")
        print "link size %d" % len(result)
        return result

    @staticmethod
    def linked_nodes(tree, node1, node2):
        """
        Check if node1 and node2 is connected in tree
        """
        if node1 in tree:
            return node2 in tree[node1]
        else:
            raise Exception("node1 (%d) is not in a tree" % node1)

    @staticmethod
    def tree_to_mesh(tree, percentage = 0.2):
        """
        Given a tree, randomly selects nodes to connect them.
        The third parameter percentage is % of numbers to be connected.
        When the number of node is 100, and percentage is 0.2, the 20 nodes are newly connected
        """
        assert percentage < 0.9  # Let's make it less than 90%.
        node_size = len(tree)
        # there should be at least one links
        additional_node_size = max(1, int(node_size * percentage + 0.5))

        links = TreeGen.get_new_link_set_from_tree(tree, additional_node_size)

        mesh = copy.deepcopy(tree)

        for link in links:
            a = link[0]
            b = link[1]
            mesh[a].append(b)
            mesh[b].append(a)

        return mesh
            
if __name__ == "__main__":
    # import unittest
    # sys.path.append("../test")
    # from testTreeGen import *
    # 
    # unittest.main(verbosity=2)
    t = Network('/Users/smcho/code/PyCharmProjects/contextAggregator/test_files/massive_data/10_100_10_80/tree/tree20_10_100_90.txt')
    #print t.networkTopology
    print TreeGen.tree_to_mesh(t.networkTopology, 0.8)