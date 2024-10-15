from my_utils import *
from tester import *
from tsp_utils import *
n = 10
maxcoord = 100
run_tests = True

points, dist = randomGraphGeo(n, 20)
print("Points", points); input(); print("Dist", dist); input()
path = nearest_neighbor_second(points, dist)
print_in_square("Path", path)
if run_tests:
    if check_path(points, path):
        print("Path 2 is correct")
    else:
        print("Path 2 is not correct")

    path_length(dist, path)
    reset_points(points)
    research_path_time(points, dist, nearest_neighbor_second)
    reset_points(points)
    average_research_path_time(points, dist, nearest_neighbor_second)