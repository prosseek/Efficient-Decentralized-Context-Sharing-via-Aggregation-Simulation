"""Simulator


"""
import sys
import os

from world import World
from configuration import *

DEFAULT_CONFIG_NAME="test_config.txt"

class Simulator(object):
    def __init__(self, world, configuration):
        self.world = world
        self.configuration = configuration

    def update(self):
        raise Exception("Error!")

    def run(self):
        simulation_time = 0
        end_time = 10
        simulation_cancelled = False

        print "Simulation start"

        while simulation_time < end_time and not simulation_cancelled:
            try:
                world.update()
                self.update()
            except Exception:
                break

        print "Simulation end"

if __name__ == "__main__":
    if len(sys.argv) == 1:
        config_file = DEFAULT_CONFIG_NAME
    else:
        config_file = sys.argv[1]

    configuration = Configuration()
    configuration.read(config_file)

    world = World()
    sim = Simulator(world, configuration)
    sim.run()