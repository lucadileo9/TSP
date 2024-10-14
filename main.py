# Traveling Salesman Problem (TSP): Given a weighted graph G = (V, E), find the Hamiltonian circuit with the minimum weight.
# What I need to do is: (find the instances)
# 1) Initialization: Start from a random node in the graph.
# 2) Build the path: At each iteration, choose the next node to visit (among the 𝑘 closest nodes, sorted according to a greedy rule like the minimum distance).
# 3) Randomization: Randomly select the next node to visit among these 𝑘 nodes, to introduce uncertainty.
# Not executing this step could lead to a deterministic algorithm.
# 4) Continue: Repeat the process until all nodes are covered.
# 5) Close the circuit by returning to the starting node.

from my_utils import *
from tester import *
n = 10
maxcoord = 100

#_____________________________________________
points, dist = get_or_create_graph_data(n, maxcoord, use_existing=False, debug=False)
path = nearest_neighbor_first(points, dist)
print_in_square("Path 1", path)


if check_path(points, path):
    print("Path 1 is correct")
else:
    print("Path 1 is not correct")
    
reset_points(points)
research_path_time(points, dist, nearest_neighbor_first)

reset_points(points)
average_research_path_time(points, dist, nearest_neighbor_first)

path_length(dist, path)

    
#_____________________________________________
points, dist = get_or_create_graph_data(n, maxcoord, use_existing=True, debug=False)
path = nearest_neighbor_second(points, dist)
print_in_square("Path 2", path)
if check_path(points, path):
    print("Path 2 is correct")
else:
    print("Path 2 is not correct")
    
reset_points(points)
research_path_time(points, dist, nearest_neighbor_first)

reset_points(points)
average_research_path_time(points, dist, nearest_neighbor_first)

path_length(dist, path)


#_____________________________________________
points, dist = get_or_create_graph_data(n, maxcoord, use_existing=True, debug=False)
path = nearest_neighbor_random(points, dist)
print_in_square("Path 3", path)
if check_path(points, path):
    print("Path 3 is correct")
else:
    print("Path 3 is not correct")

reset_points(points)
research_path_time(points, dist, nearest_neighbor_first)

reset_points(points)
average_research_path_time(points, dist, nearest_neighbor_first)

path_length(dist, path)

