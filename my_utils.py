import random
import pickle
from tqdm import tqdm
import itertools
import math
import algorithm_metrics

def brute_force_tsp(points, dist):
    """
    Solves the TSP using brute force by exploring all permutations of points.

    Parameters
    ----------
    points : list of tuples
        Each tuple represents a point as (x, y, visited).
    dist : dict
        Dictionary of distances between points with keys as (i, j) representing 
        the indices of the points and values as the distances between them.

    Returns
    -------
    shortest_path : list
        The list of point indices representing the shortest path.
    min_distance : float
        The total distance of the shortest path.
    """
    n = len(points)
    if n>10:
        print("The number of points is too high to calculate the brute force solution.")
        return None
    # Generate all permutations of points (ignoring the 'visited' flag)
    permutations = itertools.permutations(range(n))
    
    # Variables to store the minimum distance and the corresponding path
    min_distance = float('inf')
    shortest_path = None

    # Total number of permutations
    total_permutations = math.factorial(n)

    # Explore each possible permutation with a progress bar
    for perm in tqdm(permutations, total=total_permutations, desc="Exploring permutations"):
        # Calculate the distance of this path
        current_distance = 0
        for i in range(n - 1):
            current_distance += dist.get((perm[i], perm[i + 1]), float('inf'))
        
        # Add distance to return to the starting point (TSP is a cycle)
        current_distance += dist.get((perm[-1], perm[0]), float('inf'))

        # Update the minimum distance and path if this one is shorter
        if current_distance < min_distance:
            min_distance = current_distance
            shortest_path = perm
    
    return list(shortest_path) + [shortest_path[0]]

def nearest_neighbor_first(points, dist, debug=False):
    """
    Implements the nearest neighbor heuristic for the Traveling Salesman Problem (TSP).
    Args:
        points (list of tuples): A list of points where each point is represented as a tuple (coordinate, visited_flag).
                                 The visited_flag is initially set to False for all points.
        dist (dict): A dictionary containing the distances between points. The keys are tuples (i, j) representing
                     the indices of the points, and the values are the distances between those points.
        debug (bool, optional): If set to True, enables debug mode with additional print statements for tracing
                                the algorithm's execution. Default is False.
    Returns:
        list: A list of point indices representing the path found by the nearest neighbor heuristic. The path starts
              and ends at the initial point (point 0).
    """

    n = len(points)
    path = []
    
    # Start from the first point (you can start from any point)
    current_point = random.randint(0, n - 1)
   # current_point = 0  # Forced to start at point 0
    last_point = current_point
    points[current_point] = (points[current_point][0], True)  # Mark as visited
    path.append(current_point)
    
    for _ in range(n - 1):
        # Find the nearest unvisited point
        nearest = None
        min_dist = float('inf')
        
        for i in range(n):
            if debug:
                print("_________________________________________________________")
                print("Current point: ", current_point)
                print(f"Point: {i}, to be tested")
                input("")  # This input is for debugging, you can remove it if not needed
            
            if not points[i][1]:  # If the point is not visited
                if debug:
                    print("Unvisited point")
                    print("Its distance is: ", dist[(i, current_point)])
                    input("")  # This input is also for debugging purposes
            
                if (i, current_point) in dist and dist[(i, current_point)] < min_dist:
                    if debug:
                        print("Smaller than the previous, so updating")
                        input("")
                    nearest = i
                    min_dist = dist[(current_point, i)]
        
        # Visit the nearest point
        if nearest is None:
            if debug:
                print("Error: No unvisited point found")
            break
        
        current_point = nearest
        points[current_point] = (points[current_point][0], True)  # Mark as visited
        path.append(current_point)
        
        if debug:
            print("*" * 50)
            print("New current point: ", current_point)
            print("*" * 50)
    
    # Return to the starting point
    path.append(last_point)
    return path

def nearest_neighbor_second(points, dist, debug=False):
    """
    Implements the nearest neighbor algorithm to find a path through a set of points.
    Args:
        points (list of tuples): A list of tuples where each tuple represents a point. 
                                 The second element of each tuple is a boolean indicating 
                                 whether the point has been visited.
        dist (dict): A dictionary where keys are tuples representing pairs of points 
                     (point1, point2) and values are the distances between those points.
        debug (bool, optional): If True, enables debug mode which prints intermediate 
                                steps and waits for user input. Default is False.
    Returns:
        list: A list of indices representing the path through the points, starting and 
              ending at the initial point.
    """
    nearest_neighbor_second.__name__ = "first" # Set the function name for the name of the file to save the data

    n = len(points)
    path = []
    
    # Start from the first point (you can start from any point)
    current_point = random.randint(0, n - 1)
    #current_point = 0
    last_point = current_point
    points[current_point] = (points[current_point][0], True)  # Mark as visited
    path.append(current_point)
    
    for _ in range(n - 1): 
        if debug:
            print("_________________________________________________________")
            print("Current point: ", current_point)
            print(f"Point: {_}, to be tested")
            input("")  # This input is for debugging, you can remove it if not needed
            
        neighbors = [(i, dist[(current_point, i)]) for i in range(n)  # For each point insert into the tuple a pair index of the point, distance { i, dist[(current_point, i)]) }
                     if not points[i][1] and (current_point, i) in dist]  # If the point has not been visited { points[i][1] } and if the current point and point i are connected to each other { (current_point, i) in dist }
        if debug:
            print("Neighbors: ", neighbors)
            input("")
        
        # Sort neighbors by distance (second element of tuple)
        if neighbors:
            neighbors.sort(key=lambda x: x[1])  # Sort neighbors by distance, i.e. the second element of the tuple { dist[(current_point, i)] }
            if debug:
                print("Neighbors sorted: ", neighbors)
                input("")
            nearest = neighbors[0][0]  # Get the nearest unvisited neighbor
        
            # Visit the nearest point
            current_point = nearest
            points[current_point] = (points[current_point][0], True)  # Mark as visited
            path.append(current_point)
            
        else:
            print("Error: No unvisited point found")
            break
        
        if debug:
            print("*" * 50)
            print("New current point: ", current_point)
            print("*" * 50)

    path.append(last_point)
    return path

def nearest_neighbor_random(points, dist, debug=False, itereations=20):
    """
    Generates a path using a nearest neighbor heuristic with a random element.
    Args:
        points (list of tuples): A list of points where each point is a tuple (coordinate, visited_flag).
        dist (dict): A dictionary with keys as tuples representing point pairs and values as distances between them.
        debug (bool, optional): If True, enables debug mode with print statements. Default is False.
    Returns:
        list: A list representing the path of visited points.
    Notes:
        - The function starts from the first point and iteratively selects the nearest unvisited neighbor.
        - If there are multiple nearest neighbors, it randomly chooses between the first and second nearest.
        - The function marks points as visited by setting the second element of the point tuple to True.
        - The path is returned as a list of point indices.
    """
    nearest_neighbor_random.__name__ = "random"
    n = len(points)

    current_point = random.randint(0, n - 1)
    last_point = current_point

    path_length = float('inf')
    best_path = []

    for _ in range(itereations):
        reset_points(points)  # Reset dei flag di visita all'inizio di ogni ciclo
        path = [last_point]
        current_point = last_point
        points[current_point] = (points[current_point][0], True)  # Marca come visitato

        for _ in range(n - 1):
            neighbors = [(i, dist[(current_point, i)]) for i in range(n)
                         if not points[i][1] and (current_point, i) in dist]

            if neighbors:
                neighbors.sort(key=lambda x: x[1])
                nearest = random.choice([neighbors[0][0], neighbors[1][0]]) if len(neighbors) > 1 else neighbors[0][0]

                current_point = nearest
                points[current_point] = (points[current_point][0], True)
                path.append(current_point)
            else:
                print("Errore: Nessun punto non visitato trovato")
                break

        # Valutazione del percorso attuale rispetto al migliore trovato
        if len(path) == n:
            current_path_length = algorithm_metrics.path_length(dist, path)
            if current_path_length < path_length:
                path_length = current_path_length
                best_path = path[:]

    best_path.append(last_point)
    return best_path


def get_or_create_graph_data(n=0, maxcoord=0, function=None, file_name='graph_data.pkl', use_existing=True, debug=False):
    """
    Generates or loads graph data for a Traveling Salesman Problem (TSP) instance.
    This function either loads existing graph data from a file or generates new data
    if the file does not exist or if `use_existing` is set to False. The graph data
    consists of points and distances between them.
    Parameters:
        n (int): The number of points (nodes) in the graph.
        maxcoord (int): The maximum coordinate value for the points.
        function (function): The function to generate the graph data. 
        file_name (str, optional): The name of the file to load from or save to. Defaults to 'graph_data.pkl'.
        use_existing (bool, optional): If True, attempts to load existing data from the file. If False, generates new data. Defaults to True.
        debug (bool, optional): If True, prints debug information. Defaults to False.
    Returns:
        tuple: A tuple containing:
            - points (list): A list of points (nodes) in the graph.
            - dist (list): A list of distances between the points.
    """
    if use_existing:
        try:
            # Try to load data from file
            with open(file_name, 'rb') as f:
                points, dist = pickle.load(f)
            if debug:
                print(f'Data loaded from {file_name}')
                print("Loaded points:", points)
                print("Loaded distances:", dist)
        except FileNotFoundError:
            # If the file doesn't exist, generate new data
            print(f'File {file_name} not found. Generating new data.')
            points, dist = function(n, maxcoord)
            # Save the new data to file
            with open(file_name, 'wb') as f:
                pickle.dump((points, dist), f)
            if debug:
                print(f'Data saved to {file_name}')
                print("Generated points:", points)
                print("Generated distances:", dist)
    else:
        # Generate new data without trying to load from file
        points, dist = function(n, maxcoord)
        # Save the new data to file
        with open(file_name, 'wb') as f:
            pickle.dump((points, dist), f)
        if debug:
            print(f'New data generated and saved to {file_name}')
            print("Generated points:", points)
            print("Generated distances:", dist)

    return points, dist

def print_in_square(title, content):
    """
    Prints the given title and content inside a square-like frame.
    Args:
        title (str): The title to be displayed at the top of the frame.
        content (str): The content to be displayed inside the frame.
    Example:
        >>> print_in_square("Title", "This is the content")
        ______________________
        | Title               |
        | This is the content |
        ______________________
    """
    # Divide the content into lines if it is too long
    max_length = max(len(title), 80)  # Limita la lunghezza massima di ogni riga
    words = str(content).split()
    
    # Suddivide il contenuto in righe della lunghezza massima
    content_lines = []
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= max_length:
            line += (word + " ")
        else:
            content_lines.append(line.strip())
            line = word + " "
    content_lines.append(line.strip())  # Aggiunge l'ultima riga

    # Costruisce il bordo superiore e inferiore
    border = "_" * (max_length + 4)
    
    # Stampa il frame
    print(border)
    print(f"| {title.ljust(max_length)} |")  # Stampa il titolo allineato a sinistra
    for line in content_lines:
        print(f"| {line.ljust(max_length)} |")  # Stampa ogni riga del contenuto
    print(border)

def reset_points(points):
    """
    Resets the visited flag for all points in the list.
    Args:
        points (list): A list of points where each point is represented as a tuple (coordinate, visited_flag).
    """
    for i in range(len(points)):
        points[i] = (points[i][0], False)
