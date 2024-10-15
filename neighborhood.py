# Swap: Per ogni nodo del percorso, scambia la posizione del nodo corrente con il successivo.

# Valutazione: Dopo ogni swap, calcola la lunghezza totale del percorso (distanza complessiva).

# Insieme di soluzioni: Aggiungi la nuova soluzione ottenuta dallo swap a un insieme di soluzioni (o vicinato). Alla fine, potrai scegliere la soluzione migliore all'interno di questo insieme.

# Quindi facciamo una funzione che prenda in input un percorso. Per ogni nodo del percorso (tranne l'ultimo), scambia la posizione del nodo corrente con il successivo
# Poi una sottofunzione che calcoli la lunghezza del percorso. E la inseriamo in un insieme di soluzioni. 

def swap_path(path):
    """
    For each node in the path, swap the position of the current node with the next node.
    
    Parameters:
        path (list): A list of nodes in the graph.
    
    Returns:
        list: A list of paths obtained by swapping the position of nodes in the path.
    """
    swap_paths = []
    for i in range(len(path)-1):
        new_path = path.copy()
        new_path[i], new_path[i+1] = new_path[i+1], new_path[i]
        swap_paths.append(new_path)
    return swap_paths

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
    total_length = 0
    for i in range(len(path)-1):
        total_length += dist[path[i]][path[i+1]]
    return total_length