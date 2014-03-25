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
from aggregation_simulator.sample_data import SampleData

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

    def test_with_file_output(self):
        """
        Tests if the algorithm works fine
        """
        root_directory = os.path.dirname(os.path.abspath(__file__)) + "/tmp/"
        test_name = "test1"
        base_directory = os.path.join(root_directory, test_name)
        sample_file = os.path.join(base_directory, "sample.txt")
        network_file = os.path.join(base_directory, "network.txt")

        sample = SampleData()
        sample.read(sample_file)

        h0 = Host(0)
        h1 = Host(1)
        h2 = Host(2)
        hosts = [h0, h1, h2]
        neighbors = {0:[1], 1:[0,2], 2:[1]}

        # The directory where the results are stored in file
        test_kind = "aggregation"
        test_directory = os.path.join(base_directory, test_kind)
        if os.path.exists(test_directory):
            shutil.rmtree(test_directory)

        #config = {ContextAggregator.PM:ContextAggregator.SINGLE_ONLY_MODE}
        # configurations
        h0.context_aggregator.set_config({"sample":sample, "test_directory":test_directory})
        h1.context_aggregator.set_config({"sample":sample, "test_directory":test_directory})
        h2.context_aggregator.set_config({"sample":sample, "test_directory":test_directory})

        #sr = SenderReceiver()

        timestamp = 3

        count = 0
        while True:
            print "Iteration [%d]: at timestamp (%d)" % (count, timestamp)

            ## sample
            for h in hosts:
                n = neighbors[h.id]
                r = h.context_aggregator.process_to_set_output(neighbors=n, timestamp = timestamp)

            ## communication
            ### Check if there is anything to send
            if not stop_simulation(hosts):
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

            for h in hosts:
                h.context_aggregator.write(timestamp, count)

            if stop_simulation(hosts):
                break

            count += 1

if __name__ == "__main__":
    unittest.main(verbosity=2)