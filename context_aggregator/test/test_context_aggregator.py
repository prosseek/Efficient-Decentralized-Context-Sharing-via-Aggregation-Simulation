import unittest
import sys
import os
import re
import shutil


source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.context_aggregator import ContextAggregator
from context_aggregator.sender_receiver import SenderReceiver

from context_aggregator.utils_same import *

def encode_key(from_id, to_id):
    return "%d_%d" % (from_id, to_id)

def decode_key(input):
    regex = "(\d+)_(\d+)"
    result = re.match(regex, input)
    assert result is not None
    return int(result.group(1)), int(result.group(2))

class Host(object):
    def __init__(self, id):
        self.id = id
        self.context_aggregator = ContextAggregator(id)

def stop_simulation(hosts):
    if all([h.context_aggregator.is_nothing_to_send() for h in hosts]):
        return True
    else:
        return False

class TestContextAggregator(unittest.TestCase):
    def setUp(self):
        pass

    def test_send(self):
        """
        Three nodes are connected in serial

        0 <-> 1 <-> 2

        The test_for_real_world is to check if each one samples data and send correctly.
        The sent data is stored in r0,r1,r2
        """
        c0 = ContextAggregator(0)
        r = c0.process_to_set_output(neighbors=[1], timestamp = 0)
        self.assertTrue(same(r, {1: [[0], []]}))

        c1 = ContextAggregator(1)
        r = c1.process_to_set_output(neighbors=[0,2], timestamp = 0)
        self.assertTrue(same(r, {0: [[1], []], 2:[[1],[]]}))

        c2 = ContextAggregator(2)
        r = c2.process_to_set_output(neighbors=[1], timestamp = 0)
        self.assertTrue(same(r, {1: [[2], []]}))

        # First round
        ## c0 sends contexts to neighbors, s0 contains the contexts in standard form
        r0 = c0.send(timestamp=0)
        s0 = contexts_to_standard(r0[1])
        self.assertTrue(same(s0, [[0], []]))

        r1 = c1.send(neighbor=0, timestamp=0)
        s1 = contexts_to_standard(r1[0])
        self.assertTrue(same(s1, [[1], []]))

        r1 = c1.send(neighbor=2, timestamp=0)
        s1 = contexts_to_standard(r1[2])
        self.assertTrue(same(s1, [[1], []]))

        r2 = c2.send(timestamp=0)
        s2 = contexts_to_standard(r2[1])
        self.assertTrue(same(s2, [[2], []]))

    def test_receive(self):
        c0 = ContextAggregator(0)
        c0.process_to_set_output(neighbors=[1], timestamp = 0)
        c1 = ContextAggregator(1)
        c1.process_to_set_output(neighbors=[0,2], timestamp = 0)
        c2 = ContextAggregator(2)
        c2.process_to_set_output(neighbors=[1], timestamp = 0)

        # First round
        ## c0 sends contexts to neighbors, s0 contains the contexts in standard form
        r0_1 = c0.send(neighbor=1, timestamp=0)
        r1_0 = c1.send(neighbor=0, timestamp=0)
        r1_2 = c1.send(neighbor=2, timestamp=0)
        r2_1 = c2.send(neighbor=1, timestamp=0)

        c1.receive(from_node=0, contexts=r0_1[1], timestamp=0)
        c0.receive(from_node=1, contexts=r1_0[0], timestamp=0)
        c2.receive(from_node=1, contexts=r1_2[2], timestamp=0)
        c1.receive(from_node=2, contexts=r2_1[1], timestamp=0)

        r1 = c1.get_received_data(from_node=0)
        self.assertEqual(contexts_to_standard(r1), [[0],[]])
        r0 = c0.get_received_data(from_node=1)
        self.assertEqual(contexts_to_standard(r0), [[1],[]])
        r1 = c1.get_received_data(from_node=2)
        self.assertEqual(contexts_to_standard(r1), [[2],[]])
        r2 = c2.get_received_data(from_node=1)
        self.assertEqual(contexts_to_standard(r2), [[1],[]])

    def test_run_dataflow_aggregate(self):
        # at timestamp = 0
        c0 = ContextAggregator(0)
        c1 = ContextAggregator(1)
        c2 = ContextAggregator(2)

        # First round
        ## compute
        c0.process_to_set_output(neighbors=[1], timestamp = 0)
        c1.process_to_set_output(neighbors=[0,2], timestamp = 0)
        c2.process_to_set_output(neighbors=[1], timestamp = 0)

        ## communication
        r0_1 = c0.send(neighbor=1, timestamp=0)
        r1_0 = c1.send(neighbor=0, timestamp=0)
        r1_2 = c1.send(neighbor=2, timestamp=0)
        r2_1 = c2.send(neighbor=1, timestamp=0)

        c1.receive(from_node=0, contexts=r0_1[1], timestamp=0)
        c0.receive(from_node=1, contexts=r1_0[0], timestamp=0)
        c2.receive(from_node=1, contexts=r1_2[2], timestamp=0)
        c1.receive(from_node=2, contexts=r2_1[1], timestamp=0)

        r1_0 = c1.get_received_data(from_node=0)
        r0_1 = c0.get_received_data(from_node=1)
        r1_2 = c1.get_received_data(from_node=2)
        r2_1 = c2.get_received_data(from_node=1)

        self.assertTrue(contexts_to_standard(r1_0), [[0],[]])
        self.assertTrue(contexts_to_standard(r0_1), [[1],[]])
        self.assertTrue(contexts_to_standard(r1_2), [[2],[]])
        self.assertTrue(contexts_to_standard(r2_1), [[1],[]])

        # Second round
        ## compute
        o0 = c0.process_to_set_output(neighbors=[1], timestamp = 0)
        o1 = c1.process_to_set_output(neighbors=[0,2], timestamp = 0)
        o2 = c2.process_to_set_output(neighbors=[1], timestamp = 0)

        self.assertTrue(contexts_to_standard(c0.get_singles(timestamp=0)) == [[0,1],[]])
        self.assertTrue(contexts_to_standard(c1.get_singles(timestamp=0)) == [[0,1,2],[]])
        self.assertTrue(contexts_to_standard(c2.get_singles(timestamp=0)) == [[1,2],[]])

        self.assertTrue(o0 == {1: [[], []]})
        self.assertTrue(o1 == {0: [[], [0, 1, 2]], 2:[[], [0, 1, 2]]})
        self.assertTrue(o2 == {1: [[], []]})

        ## communication
        self.assertTrue(c0.is_nothing_to_send())
        self.assertTrue(c2.is_nothing_to_send())

        r1_0 = c1.send(neighbor=0, timestamp=0)
        r1_2 = c1.send(neighbor=2, timestamp=0)
        self.assertTrue(contexts_to_standard(r1_0[0]) == [[],[0,1,2]])
        self.assertTrue(contexts_to_standard(r1_2[2]) == [[],[0,1,2]])

        c0.receive(from_node=1, contexts=r1_0[0], timestamp=0)
        c2.receive(from_node=1, contexts=r1_2[2], timestamp=0)

        r0_1 = c0.get_received_data(from_node=1)
        r2_1 = c2.get_received_data(from_node=1)

        self.assertTrue(contexts_to_standard(r0_1) == [[],[0,1,2]])
        self.assertTrue(contexts_to_standard(r2_1) == [[],[0,1,2]])

        # Third iteration
        o0 = c0.process_to_set_output(neighbors=[1], timestamp = 0)
        o1 = c1.process_to_set_output(neighbors=[0,2], timestamp = 0)
        o2 = c2.process_to_set_output(neighbors=[1], timestamp = 0)

        self.assertTrue(contexts_to_standard(c0.get_singles(timestamp=0)) == [[0,1,2],[]])
        self.assertTrue(contexts_to_standard(c1.get_singles(timestamp=0)) == [[0,1,2],[]])
        self.assertTrue(contexts_to_standard(c2.get_singles(timestamp=0)) == [[0,1,2],[]])

        # It still tries to send single context of its own
        self.assertTrue(o0 == {1: [[], []]})
        #self.assertTrue(o1 == {0: [[], []], 2:[[], []]})
        self.assertTrue(o1 == {})
        self.assertTrue(o2 == {1: [[], []]})

        self.assertTrue(c0.is_nothing_to_send())
        self.assertTrue(c1.is_nothing_to_send())
        self.assertTrue(c2.is_nothing_to_send())

    def test_run_dataflow_single_only(self):
        # at timestamp = 0
        config = {ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE}
        c0 = ContextAggregator(id=0, config=config)
        c1 = ContextAggregator(id=1, config=config)
        c2 = ContextAggregator(id=2, config=config)

        # First round
        ## compute
        c0.process_to_set_output(neighbors=[1], timestamp = 0)
        c1.process_to_set_output(neighbors=[0,2], timestamp = 0)
        c2.process_to_set_output(neighbors=[1], timestamp = 0)

        ## communication
        r0_1 = c0.send(neighbor=1, timestamp=0)
        r1_0 = c1.send(neighbor=0, timestamp=0)
        r1_2 = c1.send(neighbor=2, timestamp=0)
        r2_1 = c2.send(neighbor=1, timestamp=0)

        c1.receive(from_node=0, contexts=r0_1[1], timestamp=0)
        c0.receive(from_node=1, contexts=r1_0[0], timestamp=0)
        c2.receive(from_node=1, contexts=r1_2[2], timestamp=0)
        c1.receive(from_node=2, contexts=r2_1[1], timestamp=0)

        r1_0 = c1.get_received_data(from_node=0)
        r0_1 = c0.get_received_data(from_node=1)
        r1_2 = c1.get_received_data(from_node=2)
        r2_1 = c2.get_received_data(from_node=1)

        self.assertTrue(contexts_to_standard(r1_0), [[0],[]])
        self.assertTrue(contexts_to_standard(r0_1), [[1],[]])
        self.assertTrue(contexts_to_standard(r1_2), [[2],[]])
        self.assertTrue(contexts_to_standard(r2_1), [[1],[]])

        # Second round
        ## compute
        o0 = c0.process_to_set_output(neighbors=[1], timestamp = 0)
        o1 = c1.process_to_set_output(neighbors=[0,2], timestamp = 0)
        o2 = c2.process_to_set_output(neighbors=[1], timestamp = 0)

        self.assertTrue(contexts_to_standard(c0.get_singles(timestamp=0)) == [[0,1],[]])
        self.assertTrue(contexts_to_standard(c1.get_singles(timestamp=0)) == [[0,1,2],[]])
        self.assertTrue(contexts_to_standard(c2.get_singles(timestamp=0)) == [[1,2],[]])

        self.assertTrue(o0 == {1: [[], []]})
        self.assertTrue(o1 == {0: [[2], []], 2:[[0], []]})
        self.assertTrue(o2 == {1: [[], []]})

        ## communication
        self.assertTrue(c0.is_nothing_to_send())
        self.assertTrue(c2.is_nothing_to_send())

        r1_0 = c1.send(neighbor=0, timestamp=0)
        r1_2 = c1.send(neighbor=2, timestamp=0)
        self.assertTrue(contexts_to_standard(r1_0[0]) == [[2],[]])
        self.assertTrue(contexts_to_standard(r1_2[2]) == [[0],[]])

        c0.receive(from_node=1, contexts=r1_0[0], timestamp=0)
        c2.receive(from_node=1, contexts=r1_2[2], timestamp=0)

        r0_1 = c0.get_received_data(from_node=1)
        r2_1 = c2.get_received_data(from_node=1)

        self.assertTrue(contexts_to_standard(r0_1) == [[2],[]])
        self.assertTrue(contexts_to_standard(r2_1) == [[0],[]])

        # Third iteration
        o0 = c0.process_to_set_output(neighbors=[1], timestamp = 0)
        o1 = c1.process_to_set_output(neighbors=[0,2], timestamp = 0)
        o2 = c2.process_to_set_output(neighbors=[1], timestamp = 0)

        self.assertTrue(contexts_to_standard(c0.get_singles(timestamp=0)) == [[0,1,2],[]])
        self.assertTrue(contexts_to_standard(c1.get_singles(timestamp=0)) == [[0,1,2],[]])
        self.assertTrue(contexts_to_standard(c2.get_singles(timestamp=0)) == [[0,1,2],[]])

        self.assertTrue(o0 == {1: [[], []]})
        #self.assertTrue(o1 == {0: [[], []], 2:[[], []]})
        self.assertTrue(o1 == {}) # {0: [[], []], 2:[[], []]})
        self.assertTrue(o2 == {1: [[], []]})

        self.assertTrue(c0.is_nothing_to_send())
        self.assertTrue(c1.is_nothing_to_send())
        self.assertTrue(c2.is_nothing_to_send())

    def test1(self):
        """
        Tests if the algorithm works fine
        """
        h0 = Host(0)
        h1 = Host(1)
        h2 = Host(2)

        hosts = [h0, h1, h2]
        neighbors = {0:[1], 1:[0,2], 2:[1]}

        #config = {ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE}
        # configurations
        h0.context_aggregator.set_config({"sampled_data":[0,1,2,3,4]})
        h1.context_aggregator.set_config({"sampled_data":[1,2,3,4,5]})
        h2.context_aggregator.set_config({"sampled_data":[2,3,4,5,6]})

        #sr = SenderReceiver()

        timestamp = 5
        count = 0
        while True:
            print "Iteration [%d]: at timestamp (%d)" % (count, timestamp)

            ## sample
            for h in hosts:
                n = neighbors[h.id]
                r = h.context_aggregator.process_to_set_output(neighbors=n, timestamp = timestamp)

            ## communication
            ### Check if there is anything to send
            if stop_simulation(hosts):
                break

            from_to_map = {}
            ### We need neighbors computation code here
            for h in hosts:
                if not h.context_aggregator.is_nothing_to_send():
                    ns = neighbors[h.id]
                    for n in ns:
                        sends = h.context_aggregator.send(neighbor=n, timestamp=timestamp)
                        for k, value in sends.items():
                            key = encode_key(h.id, k)
                            from_to_map[key] = value

            #print from_to_map

            for i, value in from_to_map.items():
                from_node, to_node = decode_key(i)
                h = filter(lambda i: i.id == to_node, hosts)[0]
                h.context_aggregator.receive(from_node=from_node,contexts=value,timestamp=timestamp)

            count += 1

if __name__ == "__main__":
    unittest.main(verbosity=2)