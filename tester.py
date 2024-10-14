# In this file there will be a function that takes as input the points of a graph and the path connecting them, and checks if the path is correct.
# Specifically, it checks that:
#  - no node is visited twice,
#  - the path is closed,
#  - all nodes are present,
#  - the nodes are part of the graph.
import timeit
from my_utils import reset_points

def check_path(points, path):
    """
    Validates a given path in a graph.

    This function performs several checks to ensure that the provided path is valid:
    1. The path must be closed (i.e., the first and last nodes must be the same).
    2. The path must contain all the nodes in the graph.
    3. The path must only contain nodes that are present in the graph.
    4. Each node in the path (except for the first and last) must appear only once.

    Parameters:
        points (list): A list of nodes in the graph.
        path (list): A list representing the path to be checked.

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    # check if the path is closed
    if path[0] != path[-1]:
        print("The path is not closed")
        return False
    # check if the path contains all the nodes
    for i in range(len(points)):
        if i not in path:
            print("The path doesn't contain all the nodes")
            return False
    # check if the path contains only the nodes in the graph
    for i in path:
        if i >= len(points):
            print("The path contains nodes not in the graph")
            return False
    # check if the path contains the nodes only once, except for the first and the last 
    for i in range(1, len(path) - 1):
        if path.count(path[i]) != 1:
            print("The path contains nodes more than once")
            return False
    return True

def path_length(dist, path):
    """
    Computes the length of a given path in a graph.

    This function calculates the total length of the given path by summing the distances between consecutive nodes.

    Parameters:
        dist (list): A 2D list representing the distances between nodes in the graph.
        path (list): A list representing the path for which the length is to be calculated.

    Returns:
        float: The total length of the path.
    """
    length = 0
    for i in range(len(path) - 1):
        length += dist[path[i],path[i + 1]]
    print("Path length:", round(length,2))

def make_readable_time(time):
    """
    Convert a time duration in seconds to a human-readable string format.

    Parameters:
    time (float): The time duration in seconds.

    Returns:
    str: A string representing the time duration in a more readable format, 
         using nanoseconds, microseconds, milliseconds, or seconds as appropriate.
    """
    if time < 1e-6:
        readable_time = f"{time * 1e9:.2f} nanoseconds"  # nanosecondi
    elif time < 1e-3:
        readable_time = f"{time * 1e6:.2f} microseconds"  # microsecondi
    elif time < 1:
        readable_time = f"{time * 1e3:.2f} milliseconds"  # millisecondi
    else:
        readable_time = f"{time:.2f} s"         # secondi
    return readable_time

def research_path_time(points, dist, function):
    """
    Measures the execution time of a given function on a set of parameters.

    This function calculates the time taken to execute the given function on the provided parameters.

    Parameters:
        points (list): A list of nodes in the graph.
        dist (list): A 2D list representing the distances between nodes in the graph.
        function (function): The function to be executed
    """
    start = timeit.default_timer()
    function(points, dist)
    end = timeit.default_timer()
    time=end-start
    readable_time = make_readable_time(time)    
    print("Execution time:", readable_time)

def average_research_path_time(points, dist, function, num_runs=1000):
    """
    Measures the execution time of a given function on a set of parameters.

    This function calculates the time taken to execute the given function multiple times
    and print the average time in a readble format.

    Parameters:
        points (list): A list of nodes in the graph.
        dist (list): A 2D list representing the distances between nodes in the graph.
        function (function): The function to be executed.
        num_runs (int): The number of times the function is executed to calculate the average time.
    
    Returns:
        print the average time in a readble format.
    """

    def wrapper():
        function(points, dist)
        reset_points(points)
        

    # Misura il tempo totale su num_runs esecuzioni e calcola la media
    total_time = timeit.timeit(wrapper, number=num_runs)
    avg_time = total_time / num_runs
    readable_time = make_readable_time(avg_time)
    
    print(f"Average execution time over {num_runs} runs: {readable_time}")