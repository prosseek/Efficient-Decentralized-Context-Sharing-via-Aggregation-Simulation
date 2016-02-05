# Efficient Decentralized Context Sharing via Aggregation Simulation

Simulation analysis for the paper [Efficient Decentralized Context Sharing via Smart Aggregation](http://mpc.ece.utexas.edu/media/uploads/publishing/mass2014_grapevineaggregation.pdf). 

Bug
===
Something's wrong with speed calculation in aggregated

    def test_intel6_tree(self):
        network_dir = os.path.join(get_intel_test_dir(), "real_world_intel_6_tree")
        condition = 'normal'
        self.get(network_dir, condition, use_cache = False)
        # (([2862, 2862, 0], [2862, 2862, 0]), ([1570, 106, 1464], [1570, 106, 1464]))
        # ([100.0, 100.0], [99.76648148148149, 98.58425925925923])
        # ([100.0, 54, 54, 100.0, 54, 54], [93.41592592592593, 50, 54, 31.61870370370371, 17, 54])
        # ([26.11111111111111, 18, 34], [23.574074074074073, 18, 25]) <-- the speed should be the same, singles is right, aggregated is wrong.
        # ([0.0, 0, 0], [2.672407407407407, 33, 12])
