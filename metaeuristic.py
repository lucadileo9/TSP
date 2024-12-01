from tsp_utils import readTSPLIB
from my_utils import nearest_neighbor_second
from algorithm_metrics import path_length
from neighborhood import two_opt_single_neighbor, two_opt_neighborhood
from perturbation import *
import math
import random

# TODO:
# - Calcolare il numero di iterazioni che ils_sa_tsp fa
# - CAPIRE MEGLIO IL CODICE


# In questo file costruiremo un'metaeuristica per risolvere il problema del commesso viaggiatore (TSP) su un'istanza TSPLIB.
# L'idea è fare un algoritmo ibrido tra due metaeuristiche: Simulated Annealing e Iterated Local Search.


def simulated_annealing_easy(current_solution, dist, T_0=1000, alpha=0.95, max_iterations=10000, DEBUG=False):
    """
    Esegue l'algoritmo di Simulated Annealing per il TSP.

    Args:
        current_solution (list): Soluzione iniziale (percorso).
        dist (list): Matrice delle distanze.
        T_0 (float): Temperatura iniziale.
        alpha (float): Fattore di raffreddamento (0 < alpha < 1).
        max_iterations (int): Numero massimo di iterazioni.
        debug (bool): Se True, attiva le stampe di debug.

    Returns:
        list: La migliore soluzione trovata.
    """
    # Inizializzazione
    T = T_0  # Temperatura iniziale
    current_cost = path_length(dist, current_solution)  # Calcolo del costo iniziale

    # La migliore soluzione trovata
    best_solution = current_solution
    best_cost = current_cost

    if DEBUG:
        print(f"Temperatura iniziale: {T_0}")
        print(f"Soluzione iniziale: {current_solution} con costo {current_cost}")

    for iteration in range(max_iterations):
        if DEBUG:  # Stampa periodica ogni 10 iterazioni
            print(f"Temperatura attuale: {T:.4f}")

        # Genera il vicinato usando il metodo 2-opt
        neighbor_solution = two_opt_single_neighbor(current_solution)
        neighbor_cost = path_length(dist, neighbor_solution)

        # Calcolo della differenza di costo
        delta = neighbor_cost - current_cost

        # Decidi se accettare la nuova soluzione
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / T):
            if DEBUG:
                if delta < 0:
                    print(f"Nuova soluzione CORRENTE, perchè MIGLIORE di {delta}. Costo {neighbor_cost}")
                else:
                    print(f"Nuova soluzione CORRENTE, anche se  PEGGIORE di {delta}. Costo {neighbor_cost}")
            # Accetta la nuova soluzione
            current_solution = neighbor_solution
            current_cost = neighbor_cost

            # Aggiorna la migliore soluzione trovata
            if current_cost < best_cost:
                best_solution = current_solution
                best_cost = current_cost
                if DEBUG:
                    print(f"Nuova soluzione GENERALE con costo {best_cost}")
        else:
            if DEBUG:
                print(f"Nuova soluzione SCARTATA, perchè PEGGIORE di {delta}. Costo {neighbor_cost}")
                            
        # Aggiorna la temperatura
        T = T * alpha
        input()

    # Ritorna la migliore soluzione trovata

    return best_solution

def simulated_annealing(current_solution, dist, T_0=1000, alpha=0.95, max_iterations=10000,
                        number_of_iterations_with_same_temperature=10, DEBUG=False):
    # Inizializzazione
    T = T_0  # Temperatura iniziale
    current_cost = path_length(dist, current_solution)  # Calcolo del costo iniziale

    # La migliore soluzione trovata
    best_solution = current_solution
    best_cost = current_cost
    
    total_iterations = 0
    T_min = 0.0001  # Temperatura minima
    
    if DEBUG:
        print(f"Temperatura iniziale: {T_0}")
        print(f"Soluzione iniziale: {current_solution} con costo {current_cost}")
    
    while T > T_min and total_iterations < max_iterations:
        for iteration in range(number_of_iterations_with_same_temperature):
            total_iterations += 1
            if DEBUG:  # Stampa periodica ogni 10 iterazioni
                print(f"Temperatura attuale: {T:.4f}")

            # Genera il vicinato usando il metodo 2-opt
            neighbor_solution = two_opt_single_neighbor(current_solution)
            neighbor_cost = path_length(dist, neighbor_solution)

            # Calcolo della differenza di costo
            delta = neighbor_cost - current_cost

            # Decidi se accettare la nuova soluzione
            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / T):
                if DEBUG:
                    if delta < 0:
                        print(f"Nuova soluzione CORRENTE, perchè MIGLIORE di {delta}. Costo {neighbor_cost}")
                    else:
                        print(f"Nuova soluzione CORRENTE, anche se  PEGGIORE di {delta}. Costo {neighbor_cost}")
                # Accetta la nuova soluzione
                current_solution = neighbor_solution
                current_cost = neighbor_cost

                # Aggiorna la migliore soluzione trovata
                if current_cost < best_cost:
                    best_solution = current_solution
                    best_cost = current_cost
                    if DEBUG:
                        print(f"Nuova soluzione GENERALE con costo {best_cost}")
            else:
                if DEBUG:
                    print(f"Nuova soluzione SCARTATA, perchè PEGGIORE di {delta}. Costo {neighbor_cost}")
        # Aggiorna la temperatura
        T = T * alpha

    # Ritorna la migliore soluzione trovata

    return best_solution

def ils_sa_tsp(file_path, max_iterations, T_0, alpha):
    n, points, dist = readTSPLIB(file_path)

    current_solution = nearest_neighbor_second(points, dist)
    print("Costo della soluzione iniziale:", path_length(dist, current_solution))
    best_solution = simulated_annealing(current_solution,dist,  T_0, alpha, max_iterations)

    no_improvement_count = 0
    max_no_improvement = 10  # Numero massimo di iterazioni senza miglioramenti


    for iteration in range(1):
        # Perturba la soluzione
        new_solution = three_opt_randomized(best_solution, points)

        # Applica SA alla soluzione perturbata
        new_solution = simulated_annealing(new_solution, dist, T_0=1000, alpha=0.95, max_iterations=10000,
                        number_of_iterations_with_same_temperature=10, DEBUG=False)

        
        # Aggiorna la soluzione corrente e globale
        if path_length(dist, new_solution) < path_length(dist, best_solution):
            best_solution = new_solution
            no_improvement_count = 0  # Reset se troviamo un miglioramento
        else:
            no_improvement_count += 1

        if no_improvement_count >= max_no_improvement:
            print(f"Stopping early at iteration {iteration} due to no improvement.")
            break

    return best_solution


if __name__ == "__main__":
    # testiamo il simulated annealing
    file_path = "new_instances/fnl4461.tsp"
    n, points, dist = readTSPLIB(file_path)
    # print("Points:", points)
    max_iterations = 1000
    T_0 = 1000
    alpha = 0.95
    # best_solution = simulated_annealing(points, T_0, alpha, max_iterations)
    best_solution = ils_sa_tsp(file_path, max_iterations, T_0, alpha)
    # print("Soluzione migliore:", best_solution)
    print("Costo della soluzione migliore:", path_length(dist, best_solution))