import re
import os
import shutil
import sys

# source_location = os.path.dirname(os.path.abspath(__file__)) + "/.."
# sys.path.insert(0, source_location)

from utils_report import report_generate
#from aggregation_simulator.utils_report import report_generate

class AggregationSimulator(object):
    @staticmethod
    def stop_simulation(hosts):
        if all([h.context_aggregator.is_nothing_to_send() for h in hosts]):
            return True
        else:
            return False

    @staticmethod
    def encode_key(from_id, to_id):
        return "%d_%d" % (from_id, to_id)

    @staticmethod
    def decode_key(input):
        regex = "(\d+)_(\d+)"
        result = re.match(regex, input)
        assert result is not None
        return int(result.group(1)), int(result.group(2))

    @staticmethod
    def run(config, timestamp=0):
        """
        Tests if the algorithm works fine
        """
        hosts = config["hosts"]
        neighbors = config["neighbors"]
        test_directory = config["test_directory"]

        assert hosts is not None
        assert neighbors is not None

        # if os.path.exists(test_directory):
        #     shutil.rmtree(test_directory)

        # configurations
        for h in hosts:
            h.context_aggregator.set_config(config)
            h.context_aggregator.set_config(config)
            h.context_aggregator.set_config(config)

        timestamp = timestamp

        count = 0
        while True:
            print "Iteration [%d]: at timestamp (%d)" % (count, timestamp)

            ## sample
            for h in hosts:
                n = neighbors[h.id]
                r = h.context_aggregator.process_to_set_output(neighbors=n, timestamp = timestamp, iteration=count)

            ## communication
            ### Check if there is anything to send
            if not AggregationSimulator.stop_simulation(hosts):
                from_to_map = {}
                ### We need neighbors computation code here
                for h in hosts:
                    if not h.context_aggregator.is_nothing_to_send():
                        ns = neighbors[h.id]
                        for n in ns:
                            sends = h.context_aggregator.send(neighbor=n, timestamp=timestamp)
                            for k, value in sends.items():
                                key = AggregationSimulator.encode_key(h.id, k)
                                from_to_map[key] = value

                #print from_to_map

                for i, value in from_to_map.items():
                    from_node, to_node = AggregationSimulator.decode_key(i)
                    h = filter(lambda i: i.id == to_node, hosts)[0]
                    h.context_aggregator.receive(from_node=from_node,contexts=value,timestamp=timestamp)

            for h in hosts:
                report_generate(h.context_aggregator, timestamp, count)

            if AggregationSimulator.stop_simulation(hosts):
                break

            count += 1