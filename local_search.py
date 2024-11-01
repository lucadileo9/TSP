from algorithm_metrics import path_length
from my_utils import get_or_create_graph_data, print_in_square, nearest_neighbor_second, brute_force_tsp, reset_points
from neighborhood import swap_neighborhood, two_opt_neighborhood
from tsp_utils import readTSPLIB, read_optimal_tour
from tqdm import tqdm
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
    
    # Aggiungi una barra di caricamento per mostrare il progresso su ogni start
    for _ in tqdm(range(num_starts), desc="Esecuzione Multistart"):
        # Genera un percorso iniziale con la funzione passata
        reset_points(points)
        initial_path = path_function(points, dist)
        
        # Esegui la local search con questo percorso iniziale
        current_path = local_search(dist, initial_path, neighborhood_function)
        current_length = path_length(dist, current_path)
        
        # Aggiorna il miglior percorso se la nuova soluzione è migliore
        if current_length < best_length:
            best_path = current_path
            best_length = current_length
    
    return best_path, best_length


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
    # Inizializziamo il percorso attuale con quello passato come parametro
    current_path = path
    # Calcoliamo la lunghezza del percorso iniziale
    current_length = path_length(dist, path)
    # Impostiamo la variabile 'improved' su True per entrare nel ciclo
    improved = True

    i=1
    # Questo ciclo continuerà fino a quando non ci saranno miglioramenti nel percorso
    while improved:
        # print con flush per vedere l'iterazione corrente
        print("Iterazione: ", i , end="\r", flush=True)
        i+=1
        improved = False  # All'inizio di ogni iterazione, supponiamo che non ci siano miglioramenti
        # Otteniamo una lista di "vicini" (percorsi alternativi) basati sul percorso attuale
        neighbors = neighborhood_function(current_path)
        
        # Per ogni vicino, calcoliamo la lunghezza del percorso
        for neighbor in neighbors:
            neighbor_length = path_length(dist, neighbor)
            # Se il vicino ha una lunghezza minore (quindi è un miglioramento)
            if neighbor_length < current_length:
                # Aggiorniamo il percorso e la sua lunghezza
                current_path = neighbor
                current_length = neighbor_length
                improved = True  # Indichiamo che c'è stato un miglioramento, quindi il ciclo while ripeterà

    # Restituiamo il percorso migliorato alla fine dell'algoritmo
    return current_path

if __name__ == "__main__":
    # Ottieni i dati del grafo
    n, points, dist = readTSPLIB("a280.tsp")
    # Ottiene il percorso ottimale
    perfect_path = read_optimal_tour("a280.opt.tour")
    # Calcola il percorso iniziale
    # path = nearest_neighbor_second(points, dist)
    # print("Initial Path Found")
    # # Esegui la ricerca locale con la neighborhood passata
    # optimized_path = local_search(dist, path, two_opt_neighborhood)
    
    # # Stampa i risultati
    # print("Initial Path Length:", path_length(dist, path))
    # print("Optimized Path Length:", path_length(dist, optimized_path))
    # print("Perfect Path Length:", path_length(dist, perfect_path))
    best_path, best_length = multistart_local_search(points, dist, two_opt_neighborhood, num_starts=10)
    print("Best Path Length:", best_length)
    print("Perfect Path Length:", path_length(dist, perfect_path))
