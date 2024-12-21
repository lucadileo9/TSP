import random

from utils.path_utils import print_in_square

def swap_neighborhood(path, print_neighbors=False):
    """
    Generate all possible neighbors of a path by swapping two nodes.
    
    Args:
        path (list): The current path (a list of node indices).
    
    Returns:
        list: A list of paths, each created by swapping two nodes in the original path.
    """
    neighbors = []
    n = len(path)
    
    # For each pair of nodes (i, j), perform a swap
    for i in range(1, n - 1):        # Avoid swapping the start and end nodes (0 and last)
        for j in range(i + 1, n - 1):
            # Create a copy of the path to avoid modifying the original
            new_path = path[:]
            # Perform the swap
            new_path[i], new_path[j] = new_path[j], new_path[i]
            # Add the new path to the neighborhood
            neighbors.append(new_path)
    if print_neighbors:
        print_in_square("Path", path)
        print("Swap Neighborhood:")
        for neighbor in neighbors:
            print(neighbor)
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
    # Generate all possible 2-opt neighbors
    for i in range(1, n - 2): # i starts from 1 to avoid the start node and ends at n - 2 to avoid the second-to-last node, as the last node (typically the starting node again) cannot be swapped with any other node
        for j in range(i + 3, n - 1):  # if j started from i it would swap a node with itself, if it started from i+1 it would swap two consecutive nodes, if it started from i+2 it would swap two nodes with only one node in between, not creating a true path inversion but rather a swap
            # and ends at n - 1 to avoid the end node
            new_path = path[:i] + path[i:j+1][::-1] + path[j+1:] # From start to i {path[:i]}, then from i+1 to j in reverse order {path[i:j+1][::-1]}, and finally from j+1 to the end {path[j+1:]}
            neighbors.append(new_path)
            
    if print_neighbors:
        print_in_square("Path", path)
        print("2-opt Neighborhood:")
        for neighbor in neighbors:
            print(neighbor)
    return neighbors


def two_opt_single_neighbor(path):
    """
    Genera un singolo vicino casuale utilizzando la mossa 2-opt su un dato percorso,
    assicurandosi di non modificare il primo e l'ultimo nodo.
    La mossa 2-opt scambia l'ordine dei nodi tra due indici casuali del percorso.

    Args:
        path (list): Un percorso rappresentato come lista di nodi.
    
    Returns:
        list: Un percorso che rappresenta un vicino ottenuto con una mossa 2-opt.
    """
    n = len(path)
    # Seleziona casualmente due indici validi i e j, rispettando i vincoli di 2-opt
    i = random.randint(1, n - 3)  # i parte da 1 e termina a n-3 per evitare il primo e il penultimo nodo
    j = random.randint(i + 1, n - 2)  # j è almeno 1 posizione avanti rispetto a i e termina prima dell'ultimo nodo

    # Crea il nuovo percorso invertendo i nodi tra i e j
    new_path = path[:i] + path[i:j+1][::-1] + path[j+1:]

    return new_path
def swap_single_neighbor(path):
    """
    Genera un singolo vicino casuale effettuando uno swap di due nodi in un percorso.
    Lo swap coinvolge due nodi scelti casualmente, evitando il primo e l'ultimo nodo.

    Args:
        path (list): Il percorso attuale (una lista di indici di nodi).

    Returns:
        list: Un percorso modificato in cui due nodi sono stati scambiati.
    """
    n = len(path)
    
    # Controlla che il percorso abbia almeno 3 nodi da poter scambiare
    if n < 4:
        raise ValueError("Il percorso è troppo corto per applicare la mossa di swap.")

    # Seleziona casualmente due indici validi per il swap
    while True:
        i = random.randint(1, n - 2)  # i può essere qualsiasi nodo eccetto il primo e l'ultimo
        j = random.randint(1, n - 2)  # j è anch'esso tra 1 e n-2
        if i != j:  # Assicura che i due indici siano diversi
            break

    # Crea una copia del percorso per effettuare lo swap
    new_path = path[:]
    new_path[i], new_path[j] = new_path[j], new_path[i]

    return new_path

if __name__ == "__main__":
    path = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0]
    # print_in_square("Path", path)
    print("2-opt Neighborhood:")
    two_opt_neighborhood(path, print_neighbors=True)
    print("Swap Neighborhood:")
    swap_neighborhood(path, print_neighbors=True)
    print("Swap Single Neighbor:")
    print(swap_single_neighbor(path))
    print("2-opt Single Neighbor:")
    print(two_opt_single_neighbor(path))
    