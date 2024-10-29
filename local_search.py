from algorithm_metrics import path_length
from my_utils import get_or_create_graph_data, print_in_square, nearest_neighbor_second, brute_force_tsp
from neighborhood import swap_neighborhood, two_opt_neighborhood
from tsp_utils import readTSPLIB, read_optimal_tour
# Pseudocode:
# Generate an initial solution x X; continue := true
#  2. while continue do
#  3.
#  Find x : f(x) = minf(x)x N(x)
#  4.
#  5.
#  if f(x) < f(x) then set x := x
#  else continue := false
from algorithm_metrics import path_length
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
    current_path = path
    current_length = path_length(dist, path)
    improved = True
    while improved:
        improved = False
        neighbors = neighborhood_function(current_path)
        for neighbor in neighbors:
            neighbor_length = path_length(dist, neighbor)
            if neighbor_length < current_length:
                current_path = neighbor
                current_length = neighbor_length
                improved = True
                
    return current_path

if __name__ == "__main__":
    # Ottieni i dati del grafo
    n, points, dist = readTSPLIB("a280.tsp")
    # Ottiene il percorso ottimale
    perfect_path = read_optimal_tour("a280.opt.tour")
    # Calcola il percorso iniziale
    path = nearest_neighbor_second(points, dist)
    print("Initial Path Found")
    # Esegui la ricerca locale con la neighborhood passata
    optimized_path = local_search(dist, path, two_opt_neighborhood)
    
    # Stampa i risultati
    print("Initial Path Length:", path_length(dist, path))
    print("Optimized Path Length:", path_length(dist, optimized_path))
    print("Perfect Path Length:", path_length(dist, perfect_path))

