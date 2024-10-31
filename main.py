import argparse
from my_utils import *
from algorithm_metrics import *
from tsp_utils import *

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Solve the Traveling Salesman Problem (TSP) with various algorithms.")
    
    # Boolean to use existing data or create new data
    parser.add_argument('-u_e','--use_existing', action='store_true', help="Boolean to indicate whether to use existing graph data.")
    
    # Number of points in the graph
    parser.add_argument('-n', type=int, default=10, help="Number of points in the graph.")
    
    # Maximum value for the coordinates
    parser.add_argument('-s', '--second_parametr', type=int, default=100, help="Second parameter of the function.")
    
    # Boolean to run tests
    parser.add_argument('-t', '--test',  action='store_true', help="Boolean to indicate whether to run tests.")
    
    # Boolean to test the data creation/loading
    parser.add_argument('-dd', '--data_debug', action='store_true', help="Boolean to indicate whether to print debug information.")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    print(args); 
    # Use the values passed from the command line
    n = args.n
    maxcoord = args.second_parametr
    use_existing = args.use_existing
    run_tests = args.test
    data_debug = args.data_debug

    #_____________________________________________
    points, dist = get_or_create_graph_data(function=randomEuclGraph, n=n, maxcoord=maxcoord, use_existing=use_existing, debug=data_debug)
    path = brute_force_tsp(points, dist)
    print_in_square("Brute force", path)

    if run_tests and path is not None:
        if check_path(points, path):
            print("Brute force is correct")
        else:
            print("Brute force is not correct")

        path_length(dist, path, print_length=True)
        reset_points(points)
        research_path_time(points, dist, brute_force_tsp, print_time=True)

       # reset_points(points)
       # average_research_path_time(points, dist, brute_force_tsp, num_runs=5)

    #_____________________________________________
    reset_points(points)
    path = nearest_neighbor_first(points, dist)
    print_in_square("Path 1", path)

    if run_tests:

        if check_path(points, path):
            print("Path 1 is correct")
        else:
            print("Path 1 is not correct")
        
        path_length(dist, path, print_length=True)

        reset_points(points)
        research_path_time(points, dist, nearest_neighbor_first, print_time=True)

        reset_points(points)
        average_research_path_time(points, dist, nearest_neighbor_first, print_time=True)

    #_____________________________________________
    reset_points(points)
    path = nearest_neighbor_second(points, dist)
    print_in_square("Path 2", path)
    
    if run_tests:
        if check_path(points, path):
            print("Path 2 is correct")
        else:
            print("Path 2 is not correct")

        path_length(dist, path, print_length=True)

        reset_points(points)
        research_path_time(points, dist, nearest_neighbor_second, print_time=True)

        reset_points(points)
        average_research_path_time(points, dist, nearest_neighbor_second, print_time=True)

    #_____________________________________________
    reset_points(points)
    path = nearest_neighbor_random(points, dist)
    print_in_square("Path 3", path)
    
    if run_tests:
        if check_path(points, path):
            print("Path 3 is correct")
        else:
            print("Path 3 is not correct")

        path_length(dist, path, print_length=True)

        reset_points(points)
        research_path_time(points, dist, nearest_neighbor_random, print_time=True)

        reset_points(points)
        average_research_path_time(points, dist, nearest_neighbor_random, print_time=True)


if __name__ == "__main__":
    main()
