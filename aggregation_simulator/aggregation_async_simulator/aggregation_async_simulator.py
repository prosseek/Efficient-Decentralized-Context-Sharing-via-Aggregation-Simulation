__author__ = 'smcho'
import sys
import random

from event import Event
from channels import Channels
from aggregation_simulator.aggregation_simulator import AggregationSimulator

TIME_OUT = 300

class AggregationAsyncSimulator(object):
    def __init__(self):
        pass

    def event_queue_add(self, ev):
        self.event_queue.append(ev)
        self.event_queue = sorted(self.event_queue, key=lambda e: e.time)
        #print self.event_queue

    def get_next_event(self):
        event_queue = self.event_queue
        if len(event_queue):
            next_queue = event_queue[0]
            return next_queue.time
        else:
            return sys.maxint

    def process_normal(self): # , hosts, event_queue):
        print self.current_time
        for h in self.hosts.values():
            if h.state == "INIT":
                # 1. sample data
                h.sample()
                # 2. generate the output
                r = h.context_aggregator.process_to_set_output(neighbors=self.neighbors, timestamp = 0, iteration=0)

                # 2. change state to communication
                h.state = "COMMUNICATION"
                # 3. set timeout to forcefully switch to computation mode
                ev = Event(time=self.current_time + TIME_OUT, action="timeout", node=h)

                self.event_queue_add(ev)
                #self.event_queue.append(ev)

            elif h.state == "COMMUNICATION":
                if not h.send_all():
                    for n in self.neighbors[h.id]:
                        if self.channels.available(h.id, n) and not h.sent_already(n):
                            sends = h.send(n)
                            receive_time = self.current_time + 7 # random.randint(10,20)
                            node = self.hosts[n]
                            ev = Event(time=receive_time, action="receive", node=node, source_node=h)
                            print "EVENT %s\n" % ev
                            self.event_queue_add(ev)
                            #self.event_queue.append(ev)
                            #key = AggregationSimulator.encode_key(h.id, k)
                            for k, value in sends.items():
                                if value == set([]): continue
                                key = AggregationSimulator.encode_key(h.id, k)
                                self.from_to_map[key] = value
                                self.channels.use(h.id, n)
                                print "%d SEND: %s -> %s\n" % (self.current_time, h.id, n)

                if h.send_all() and h.receive_all():
                    h.state = "COMPUTATION"

            elif h.state == "COMPUTATION":
                print "%s >> Node %s in computation mode" % (self.current_time, h.id)
                # check if you are here because of timeout
                time_out = True
                if h.send_all() and h.receive_all(): time_out = False
                h.reset_history()
                h.context_aggregator.process_to_set_output(neighbors=self.neighbors[h.id], timestamp = 0, iteration=0)
                print "%s: process finished host(%d)" % (self.current_time, h.id)

                if h.is_output_empty():
                    h.state = "STEADY"
                else:
                    h.state = "COMMUNICATION"

            elif h.state == "STEADY":
                print "%s >> Node %s in steady mode" % (self.current_time, h.id)

    def process_event(self):
        event_queue = self.event_queue
        if len(event_queue):
            event = event_queue.pop(0)
            current_time = event.time
            node = event.node
            source_node = event.source_node
            node_state = node.state
            action = event.action
            if action == "timeout":
                if node_state == "COMMUNICATION": # I wait too long
                    node.state = "COMPUTATION"

            elif action == "receive":
                for i, value in self.from_to_map.items():
                    from_node, to_node = AggregationSimulator.decode_key(i)
                    if node.id == to_node and source_node.id == from_node:
                        self.current_time = current_time
                        node.receive(from_node=from_node,contexts=value,timestamp=0)
                        self.channels.restore(from_node, to_node)
                        print "%d RECEIVE: %s -> %s" % (current_time, source_node.id, node.id)
                        if node_state == "STEADY":
                            print "!! %s >> Mode back to COMMUNICATION " % node.id
                            node.state = "COMMUNICATION"
                self.process_normal()

    def run(self, config, timestamp=0):
        """
        Tests if the algorithm works fine
        """
        self.neighbors = config["neighbors"]
        test_directory = config["test_directory"]
        network = config["network"]
        hosts = config["hosts"]
        assert hosts is not None
        assert self.neighbors is not None

        self.hosts = {}
        # We need a hosts dictionary
        for h in hosts:
            id = h.id
            self.hosts[id] = h
            h.neighbors = self.neighbors[id]

        self.from_to_map = {}
        self.current_time = 0
        end_time = 500
        time_delta = 10
        #available_hosts = self.hosts
        self.event_queue = []

        self.channels = Channels(network.get_network())
        #print self.channels

        while self.current_time < end_time:
            self.process_normal()

            next_time = self.current_time + time_delta

            next_event_time = self.get_next_event()

            while self.current_time <= next_event_time < next_time:
                self.process_event()
                next_event_time = self.get_next_event()

            self.current_time = next_time

if __name__ == "__main__":
    import doctest
    doctest.testmod()