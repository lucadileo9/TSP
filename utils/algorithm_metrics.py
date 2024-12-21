# In this file there will be a function that takes as input the points of a graph and the path connecting them, and checks if the path is correct.
# Specifically, it checks that:
#  - no node is visited twice,
#  - the path is closed,
#  - all nodes are present,
#  - the nodes are part of the graph.
import timeit

def check_path(points, path, DEBUG=False):
    """
    Validates a given path in a graph.

    Parameters:
        points (list): A list of nodes in the graph.
        path (list): A list representing the path to be checked.
        DEBUG (bool): Whether to print debug messages.

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    # Check if the path is closed
    if path[0] != path[-1]:
        if DEBUG:
            print("The path is not closed")
        return False

    # Check if the path contains all the nodes
    for i in range(len(points)):
        if i not in path:
            if DEBUG:
                print("The path doesn't contain all the nodes")
                # Find the missing node
                for j in range(len(points)):
                    if j not in path:
                        print(f"Missing node: {j}")
            return False

    # Check if the path contains only the nodes in the graph
    for i in path:
        if i >= len(points):
            if DEBUG:
                print("The path contains nodes not in the graph")
            return False

    # Check if the path contains the nodes only once, except for the first and the last
    for i in range(1, len(path) - 1):
        if path.count(path[i]) != 1:
            if DEBUG:
                print("The path contains nodes more than once")
            return False

    return True

def path_length(dist, path, print_length=False):
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
    if print_length:
        print("Path length:", round(length,2))
        return round(length,2)
    else:
        return round(length,2)
    
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

def research_path_time(points, dist, function, print_time=False, make_readable=True):
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
    if make_readable:
        readable_time = make_readable_time(time)
    else:
        readable_time = time    
        
    if print_time:
        print("Execution time:", readable_time)        

    return readable_time
    
def average_research_path_time(points, dist, function, num_runs=1000, print_time=False, make_readable=True):
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
        from .path_utils import reset_points
        function(points, dist)
        reset_points(points)
    # Misura il tempo totale su num_runs esecuzioni e calcola la media
    total_time = timeit.timeit(wrapper, number=num_runs)
    avg_time = total_time / num_runs
    if make_readable:
        readable_time = make_readable_time(avg_time)
    else:
        readable_time = avg_time
        
    if print_time:
        print(f"Average execution time over {num_runs} runs: {readable_time}")
    
    return readable_time
 
if __name__ == "__main__":
    # Test the check_path function
    points = [((56, 7), False), ((50, 76), False), ((15, 34), False), ((32, 88), False), ((94, 9), False)] 
    dist = {(0, 0): 0.0, (0, 1): 69.26, (0, 2): 49.09, (0, 3): 84.48, (0, 4): 38.05, (1, 0): 69.26, (1, 1): 0.0, (1, 2): 54.67, (1, 3): 21.63, (1, 4): 80.16, (2, 0): 49.09, (2, 1): 54.67, (2, 2): 0.0, (2, 3): 56.61, (2, 4): 82.86, (3, 0): 84.48, (3, 1): 21.63, (3, 2): 56.61, (3, 3): 0.0, (3, 4): 100.42, (4, 0): 38.05, (4, 1): 80.16, (4, 2): 82.86, (4, 3): 100.42, (4, 4): 0.0}
    path = [0, 1, 2, 3, 4,0]
    print(check_path(points, path, DEBUG=True))  # True

    # Test the path_length function
    print(path_length(dist, path, print_length=True))  

    # Test the make_readable_time function
    print(make_readable_time(1e-9))  # 1.00 nanoseconds
    print(make_readable_time(1e-6))  # 1.00 microseconds  
    print(make_readable_time(1e-3))  # 1.00 milliseconds
    print(make_readable_time(1))     # 1.00 s
    
    # lazy import
    from .path_utils import nearest_neighbor_first
    
    # Test the research_path_time function
    research_path_time(points, dist, nearest_neighbor_first, print_time=True, make_readable=True)
    
    # Test the average_research_path_time function
    average_research_path_time(points, dist, nearest_neighbor_first, num_runs=1000, print_time=True, make_readable=True) 