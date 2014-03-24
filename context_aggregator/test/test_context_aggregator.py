import unittest
import sys
import os

source_location = os.path.dirname(os.path.abspath(__file__)) + "/../context"
sys.path.insert(0, source_location)

source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, source_location)

from context_aggregator.context_aggregator import ContextAggregator
from context_aggregator.sender_receiver import SenderReceiver

from context_aggregator.utils_same import *

class Host(object):
    def __init__(self, id):
        self.id = id
        self.context_aggregator = ContextAggregator()

def stop_simulation(hosts):
    if all([h.context_aggregator.output_dictionary() is None for h in hosts]):
        return True
    else:
        return False

class TestContextAggregator(unittest.TestCase):
    def setUp(self):
        pass

    def test_send(self):
        c0 = ContextAggregator(0)
        r = c0.process_to_set_output(neighbors=[1], timestamp = 0)
        self.assertTrue(same(r, {1: [[0], []]}))

        c1 = ContextAggregator(1)
        r = c1.process_to_set_output(neighbors=[0], timestamp = 0)
        self.assertTrue(same(r, {0: [[1], []]}))

        r0 = c0.send(timestamp=0)
        self.assertTrue(same(contexts_to_standard(r0[1]), [[0], []]))


    def atest1(self):
        """
        Tests if the algorithm works fine
        """
        h0 = Host(0)
        h1 = Host(1)
        h2 = Host(2)

        hosts = [h0, h1, h2]
        neighbors = {0:[1,2], 1:[0], 2:[0]}
        # The directory where the results are stored in file
        output_file = os.path.dirname(os.path.abspath(__file__)) + "/tmp/test1.txt"
        if os.path.exists(output_file):
            os.unlink(output_file)

        # configurations
        h0.context_aggregator.set_config({"sampled_data":[0,1,2,3,4], "output_file":output_file})
        h1.context_aggregator.set_config({"sampled_data":[1,2,3,4,5], "output_file":output_file})
        h2.context_aggregator.set_config({"sampled_data":[2,3,4,5,6], "output_file":output_file})

        sr = SenderReceiver()

        count = 0
        while True:
            print "[%d]:" % count

            ## sample
            for h in hosts:
                n = neighbors[h.id]
                h.context_aggregator.process_to_set_output(neighbors=n, timestamp = 0)
                # THINK! Is this necessary? Or do I need to put in the method?
                h.clear_input() # ready for input

            ## communication
            ### Check if there is anything to send
            if stop_simulation(hosts):
                break

            ### We need neighbors computation code here
            r0 = h0.context_aggregator.send()
            sr += r0
            r1 = h1.context_aggregator.send()
            sr += r1
            r2 = h2.context_aggregator.send()
            sr += r2

            ### We need to check if host receives the data or not
            h0.context_aggregator.receive(1, sr)
            h0.context_aggregator.receive(2, sr)
            h1.context_aggregator.receive(0, sr)
            h2.context_aggregator.receive(0, sr)

            for h in hosts:
                h0.context_aggregator.write()

            count += 1

if __name__ == "__main__":
    unittest.main(verbosity=2)