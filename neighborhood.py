from algorithm_metrics import path_length
from my_utils import get_or_create_graph_data, print_in_square, nearest_neighbor_second, brute_force_tsp
from local_search import local_search

def swap_neighborhood(path):
    """
    Generate all possible neighbors of a path by swapping two nodes.
    
    Args:
        path (list): The current path (a list of node indices).
    
    Returns:
        list: A list of paths, each created by swapping two nodes in the original path.
    """
    neighbors = []
    n = len(path)
    
    # Per ogni coppia di nodi (i, j) esegui uno swap
    for i in range(1, n - 1):        # Evita di scambiare il nodo di partenza e arrivo (0 e ultimo)
        for j in range(i + 1, n - 1):
            # Crea una copia del percorso per evitare modifiche sull'originale
            new_path = path[:]
            # Esegui lo swap
            new_path[i], new_path[j] = new_path[j], new_path[i]
            # Aggiungi il nuovo percorso al vicinato
            neighbors.append(new_path)
    
    return neighbors


# Pseudocode:
# procedure 2optSwap(route, v1, v2) {
#     1. take route[start] to route[v1] and add them in order to new_route
#     2. take route[v1+1] to route[v2] and add them in reverse order to new_route
#     3. take route[v2+1] to route[start] and add them in order to new_route
#     return new_route;
# }
def two_opt_neighborhood(path, print_neighbors=False):
    """
    Generates the 2-opt neighborhood for a given path in the Traveling Salesman Problem (TSP).
    The 2-opt neighborhood is created by reversing the order of nodes between two indices in the path.
    This function generates all possible 2-opt neighbors by considering all pairs of indices (i, j) 
    where 1 <= i < j - 1 < len(path) - 1.
    Args:
        path (list): A list representing the current path of nodes in the TSP.
    Returns:
        list: A list of paths, each representing a neighbor obtained by a 2-opt move.
    """
    neighbors = []
    n = len(path)
    # Genera tutti i possibili vicini 2-opt
    for i in range(1, n - 2): # i inizia da 1 per evitare il nodo di partenza e finisce a n - 2 per evitare il penultimo nodo, infatti non è possibilie scambiare l'ultimo nodo (che è tipicamente di nuovo il nodo di partenza) con alcun altro nodo
        for j in range(i + 3, n - 1):  # se j iniziasse da i scambierebbe un nodo con sé stesso, se iniziasse da i+1 scambierebbe due nodi consecutivi, se iniziasse da i+2 scambierebbe due nodi con un solo nodo in mezzo, non facendo quindi una vera e propria iversione di percorso, ma uno swap
            # e finisce a n - 1 per evitare il nodo di arrivo
            new_path = path[:i] + path[i:j+1][::-1] + path[j+1:] # Dallo start fino a i {path[:i]}, poi da i+1 a j in ordine inverso {path[i:j+1][::-1]}, infine da j+1 fino alla fine {path[j+1:]}
            neighbors.append(new_path)
            
    if print_neighbors:
        print_in_square("Path", path)
        print("2-opt Neighborhood:")
        for neighbor in neighbors:
            print(neighbor)
    return neighbors


if __name__ == "__main__":
    # Ottieni i dati del grafo
    points, dist = get_or_create_graph_data( use_existing=True)
    path = nearest_neighbor_second(points, dist)
    brute_force_path = brute_force_tsp(points, dist)
    print_in_square("Initial Path", path)
    print("Initial Path Length:", path_length(dist, path))

    optimized_path = local_search(dist, path, swap_neighborhood)
    # Stampa i risultati
    print_in_square("Brute Force Path", brute_force_path)
    path_length(dist, brute_force_path, print_length=True)
    print_in_square("Optimized Path", optimized_path)
    path_length(dist, optimized_path, print_length=True)

