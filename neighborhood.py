from algorithm_metrics import path_length
from my_utils import get_or_create_graph_data, print_in_square, nearest_neighbor_second
# Pseudocode:
# procedure 2optSwap(route, v1, v2) {
#     1. take route[start] to route[v1] and add them in order to new_route
#     2. take route[v1+1] to route[v2] and add them in reverse order to new_route
#     3. take route[v2+1] to route[start] and add them in order to new_route
#     return new_route;
# }

def two_opt_neighborhood(path):
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
        for j in range(i + 2, n - 1):  # j inizia da i + 2 per evitare di scambiare nodi consecutivi e finisce a n - 1 per evitare il nodo di arrivo
            new_path = path[:i] + path[i:j+1][::-1] + path[j+1:] # Dallo start fino a i {path[:i]}, poi da i+1 a j in ordine inverso {path[i:j+1][::-1]}, infine da j+1 fino alla fine {path[j+1:]}
            neighbors.append(new_path)

    return neighbors

# Esempio di utilizzo
points, dist = get_or_create_graph_data(function=print, use_existing=True)
path = nearest_neighbor_second(points, dist)
print_in_square("Path", path)
neighbors = two_opt_neighborhood(path)

# Stampa i vicini generati
for neighbor in neighbors:
    print(neighbor)
    path_length(dist, neighbor, print_length=True)
