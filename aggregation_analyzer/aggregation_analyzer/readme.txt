# Basic idea
1. Intelligently generate configuration file for `process_one_network_file.py`.
    1. It will read network_file_path
    2. Run simulation for singles/aggregations N times, write the simulation files in the prescribed directory
    3. Write down the report file at the prescribed directory
2. parallel_processing.py
    1. It does the same thing with 1, but in a parallel way
    2. The key is to generate different configuration files to be executed.

# Massive (nodes 10 to 100) simulation
1. mass_simulation/get_configs/get_configs_for_massive_simulation is the method to get configuration files
2. Run mass_simulation_analyzer_node_10_to_100.py
   It will read the report files to average to get a dictionary for plot

# Variety simulation (change - drop/disconnect/threshold)
1. Go to mass_simulation/get_configs.py and create whatever method to generate configuration. 
    1. Don't forget that we only need the test name for this setup. 
2.  Run various_simulation_analyzer.py to get the report