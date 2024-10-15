from my_utils import *
from tester import *
n = 10
maxcoord = 100
run_tests = False

points, dist = get_or_create_graph_data(n, maxcoord, use_existing=False, debug=True)
path = nearest_neighbor_second(points, dist)
print_in_square("Path 2", path)
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
