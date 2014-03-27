import os
from utils import readLocationFile

value = [23.64, 23.50, 23.28, 23.48, 22.86, 22.86, 22.73, 22.50, 22.66, 22.50, 21.52, 21.03, 21.36, 22.49, 22.76, 23.34, 23.60, 23.23, 24.01, 23.87, 24.07, 24.42, 24.59, 25.00, 25.20, 24.95, 25.19, 25.24, 24.95, 25.06, 24.53, 24.38, 24.21, 24.64, 24.92, 25.22, 24.91, 24.40, 24.57, 25.05, 25.05, 25.21, 25.18, 26.25, 24.79, 23.88, 25.77, 24.17, 24.79, 24.30, 23.96, 23.87, 23.16, 22.11]
location_file = os.path.dirname(os.path.abspath(__file__)) + "/../test_files/mote_locs.txt"

if os.path.exists(location_file):
    l = readLocationFile(location_file)
