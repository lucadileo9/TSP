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
