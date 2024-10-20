from my_utils import *
from algorithm_metrics import *
from tsp_utils import *
from dataset_generator import *


import matplotlib.pyplot as plt

# Lista delle coordinate (x, y) dei punti del grafo
coordinates, distances = load_graph_data("./data/euclidean/NumVertices_1000/MaxVal_100/instance_13.csv")
#coordinates, distances = randomGraph2D(10, 0.5)


# Esegui la funzione per visualizzare il grafo e le distanze
# run_tests = True
# points, dist = coordinates, distances
# path = nearest_neighbor_first(points, dist, debug=False)
# print_in_square("Path", path)

# if run_tests:
#     if check_path(points, path):
#         print("Brute force is correct")
#     else:
#         print("Brute force is not correct")

#     path_length(dist, path, print_length=True)
#     reset_points(points)
#     research_path_time(points, dist, nearest_neighbor_first, print_time=True)
    #average_research_path_time(points, dist, nearest_neighbor_first, num_runs=1000)


# n= 10
# maxcoord = 100
# use_existing = False
# run_tests = True
# data_debug = False

# points, dist = get_or_create_graph_data(n, maxcoord, function=randomGraphGeo, use_existing=use_existing, debug=data_debug)

# path = nearest_neighbor_first(points, dist)
# print_in_square("Brute force", path)

# if run_tests:
#     if check_path(points, path):
#         print("Brute force is correct")
#     else:
#         print("Brute force is not correct")

#     path_length(dist, path, print_length=True)
#     reset_points(points)
#     research_path_time(points, dist, nearest_neighbor_first, print_time=True)
#     average_research_path_time(points, dist, nearest_neighbor_first, num_runs=1000)
