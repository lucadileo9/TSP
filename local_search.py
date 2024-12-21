from algorithm_metrics import path_length
from my_utils import nearest_neighbor_second, nearest_neighbor_random, reset_points, print_in_square
from neighborhood import swap_neighborhood, two_opt_neighborhood
from tsp_utils import readTSPLIB, read_optimal_tour
from tqdm import tqdm
from algorithm_metrics import path_length
    
def multistart_local_search(points, dist, path_function, neighborhood_function, num_starts=10):
    """
    Perform a multistart local search to find an optimized path.
    Args:
        points (list): A list of points representing the locations.
        dist (function): A function to calculate the distance between two points.
        path_function (function): A function to generate an initial path.
        neighborhood_function (function): A function to generate neighboring solutions.
        num_starts (int, optional): The number of random starts for the local search. Default is 10.
    Returns:
        tuple: A tuple containing the best path found and its length.
    """
    best_path = None
    best_length = float('inf')
    
    # Add a progress bar to show the progress on each start
    for _ in tqdm(range(num_starts), desc="Multistart Execution"):
        # Generate an initial path with the provided function
        reset_points(points)
        initial_path = path_function(points, dist)
        
        # Perform local search with this initial path
        current_path = local_search(dist, initial_path, neighborhood_function)
        current_length = path_length(dist, current_path)
        
        # Update the best path if the new solution is better
        if current_length < best_length:
            best_path = current_path
            best_length = current_length
    
    return best_path, best_length

# Pseudocode:
# Local Search (LS):
#  1. Start from an initial feasible solution
#  2. Look for possible improvements in a neighborhood of the
#  solution
#  3. iterates 2. until no improvement can be found (local
#  optimum)
def local_search(dist, path, neighborhood_function):
    """
    Performs a local search on a given path in the Traveling Salesman Problem (TSP) using a given neighborhood function.
    The local search iteratively explores the neighborhood of the current path and moves to the best neighbor that improves the path.
    The search continues until no neighbor can be found that improves the path.
    Args:
        dist (dict): A dictionary containing the pairwise distances between nodes.
        path (list): A list representing the current path of nodes in the TSP.
        neighborhood_function (function): A function that generates the neighborhood of a given path.
    Returns:
        list: The best path found during the local search.
    """
    # Initialize the current path with the one provided as a parameter
    current_path = path
    # Calculate the length of the initial path
    current_length = path_length(dist, path)
    # Set the 'improved' variable to True to enter the loop
    improved = True
    # This loop will continue as long as there are improvements in the path
    while improved:
        improved = False  # At the beginning of each iteration, assume no improvements
        # Obtain a list of "neighbors" (alternative paths) based on the current path
        neighbors = neighborhood_function(current_path)
        
        # For each neighbor, calculate the path length
        for neighbor in neighbors:
            neighbor_length = path_length(dist, neighbor)
            # If the neighbor has a shorter length (indicating an improvement)
            if neighbor_length < current_length:
                # Update the path and its length
                current_path = neighbor
                current_length = neighbor_length
                improved = True  # Indicate that there was an improvement, so the while loop will repeat

    # Return the improved path at the end of the algorithm
    return current_path

def local_search_optimized(dist, path):
    """
    Performs a local search on a given path in the Traveling Salesman Problem (TSP) using a given neighborhood function.
    The local search iteratively explores the neighborhood of the current path and moves to the best neighbor that improves the path.
    The search continues until no neighbor can be found that improves the path.
    Args:
        dist (dict): A dictionary containing the pairwise distances between nodes.
        path (list): A list representing the current path of nodes in the TSP.
        neighborhood_function (function): A function that generates the neighborhood of a given path.
    Returns:
        list: The best path found during the local search.
    """
    # Initialize the current path with the one provided as a parameter
    current_path = path
    # Calculate the length of the initial path
    current_length = path_length(dist, path)
    # Set the 'improved' variable to True to enter the loop
    improved = True
# in questa versione la funzione di vicinato è la 2-opt, è già inclusa ed è più efficiente
    while improved:
        improved = False
        for i in range(1, len(path) - 1):  # Evita il primo nodo e l'ultimo
            for j in range(i + 2, len(path) - 1):  # j è almeno due posizioni dopo i

                # Calcola solo la differenza di costo
                delta = calculate_delta(dist, current_path, i, j)
                
                if delta < 0:  # Miglioramento trovato
                    # Applica lo scambio solo se migliora
                    current_path = (
                        current_path[:i] +
                        current_path[i:j+1][::-1] +
                        current_path[j+1:]
                    )
                    current_length += delta  # Aggiorna la lunghezza
                    improved = True
                    break  # Esci dal ciclo per cercare di nuovo
            if improved:
                break

    # Return the improved path at the end of the algorithm
    return current_path

def calculate_delta(dist, path, i, j):
    """
    Calcola la differenza di costo (delta) causata dall'inversione tra i e j.
    """
    # Nodi coinvolti nell'inversione
    a, b = path[i-1], path[i]   # Arco entrante prima dello scambio
    c, d = path[j], path[j+1]   # Arco uscente prima dello scambio
    
    # Delta di costo
    delta = (dist[a,c] + dist[b,d]) - (dist[a,b] + dist[c,d])
    return delta


def local_search_with_counted_iterations(dist, path, neighborhood_function, iterations=100):
    """
    Performs a local search on a given path in the Traveling Salesman Problem (TSP) using a given neighborhood function.
    The local search iteratively explores the neighborhood of the current path and moves to the best neighbor that improves the path.
    The search continues for a number of iterations as long as an improvement is found at each iteration until no neighbor is found that improves the path.
    Args:
        dist (dict): A dictionary containing the pairwise distances between nodes.
        path (list): A list representing the current path of nodes in the TSP.
        neighborhood_function (function): A function that generates the neighborhood of a given path.
        iterations (int, optional): The number of iterations to perform. Default is 100.
    Returns:
        list: The best path found during the local search.
    """
    current_path = path
    current_length = path_length(dist, path)
    improved = True
    
    # Add a progress bar to show iterations
    for _ in (range(iterations)):
        improved = False
        neighbors = neighborhood_function(current_path)
        for neighbor in neighbors:
            neighbor_length = path_length(dist, neighbor)
            if neighbor_length < current_length:
                current_path = neighbor
                current_length = neighbor_length
                improved = True
        
        if not improved:
            break  # Exit the loop if there are no improvements

    return current_path


if __name__ == "__main__":
    # TO LOAD GRAPH DATA____________________________________
    # Obtain graph data
    n, points, dist = readTSPLIB("a280.tsp")
    # Obtain the optimal path
    perfect_path = read_optimal_tour("a280.opt.tour")
    
    # TO EXECUTE LOCAL SEARCH______________________________________
    # Calculate the initial path
    path = nearest_neighbor_random(points, dist)
    print("Initial Path Found")
    # Execute local search with the provided neighborhood
    optimized_path = local_search(dist, path, two_opt_neighborhood)
    # Print results
    print("Initial Path Length:", path_length(dist, path))
    print_in_square("Initial path", path)
    
    print("Optimized Path Length:", path_length(dist, optimized_path))
    print_in_square("Optimized path", path)
    
    print("Perfect Path Length:", path_length(dist, perfect_path))
    print_in_square("Perfect path", path)
    input("Press ENTER to execute multistart local search...")
    
    
    # TO EXECUTE MULTISTART LOCAL SEARCH__________________________
    best_path, best_length = multistart_local_search(points, dist, nearest_neighbor_second, two_opt_neighborhood, num_starts=10)
    print("Best Path Length with nearest neighbor:", best_length)
    
    best_path, best_length = multistart_local_search(points, dist, nearest_neighbor_random , two_opt_neighborhood, num_starts=10)
    print("Best Path Length with nearest neighbor random:", best_length)

    print("Perfect Path Length:", path_length(dist, perfect_path))
