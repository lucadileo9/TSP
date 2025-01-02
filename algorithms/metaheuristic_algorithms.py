'''
This module contains implementations of various metaheuristic algorithms for solving the Traveling Salesman Problem (TSP).
The algorithms included are Simulated Annealing (SA) and Iterated Local Search (ILS).
Functions:
    simulated_annealing_easy(current_solution, dist, T_0=1000, alpha=0.95, max_iterations=10000, DEBUG=False):
        Perform a simplified version of the Simulated Annealing algorithm to find an optimized solution for the TSP.
        This function is a simplified version of the simulated_annealing function, because it execute only one iteration for each temperature.
    simulated_annealing(current_solution, dist, T_0=1000, alpha=0.95, max_iterations=10000, number_of_iterations_with_same_temperature=50, DEBUG=False, points=None):
        Perform the Simulated Annealing optimization algorithm to find a near-optimal solution for the TSP.
        This version starts from a given initial solution. It is used in the hybrid metaheuristic algorithm.
    complete_simulated_annealing(file_path, T_0=1000, alpha=0.95, max_iterations=10000, number_of_iterations_with_same_temperature=50, DEBUG=False):
        Perform the Simulated Annealing algorithm to solve the TSP using a TSPLIB file.
    iterated_local_search(file_path, max_iterations, DEBUG=False):
        Perform Iterated Local Search (ILS) to solve the TSP using a TSPLIB file.
Usage:
    Execute this module to test the implemented metaheuristic algorithms for solving the TSP.
    Example:
        python metaheuristic_algorithms.py
    This will run the Simulated Annealing and Iterated Local Search algorithms on a sample TSP instance and print the results.
    In this example, the sample TSP instance is read from the file "TSP/data/TSP_instances/a280.tsp".
'''
from tqdm import tqdm
import math
import random

from .perturbation import *
from .local_search_algorithms import local_search, local_search_optimized
from .neighborhood_generators import two_opt_single_neighbor, two_opt_neighborhood
from ..utils.algorithm_metrics import path_length
from ..utils.path_utils import generate_random_path, nearest_neighbor_second
from ..utils.tsp_utils import readTSPLIB


def simulated_annealing_easy(current_solution, dist, T_0=1000, alpha=0.95, max_iterations=10000, DEBUG=False):
    """
    Perform simulated annealing to find an optimized solution for the given problem.
    This function is a simplified version of the simulated_annealing function, because it execute only one iteration for each temperature.
    Parameters:
    current_solution (list): The initial solution to start the optimization process.
    dist (2D list): The distance matrix representing the problem space.
    T_0 (float, optional): The initial temperature for the annealing process. Default is 1000.
    alpha (float, optional): The cooling rate, a factor by which the temperature is multiplied each iteration. Default is 0.95.
    max_iterations (int, optional): The maximum number of iterations to perform. Default is 10000.
    DEBUG (bool, optional): If True, prints detailed debug information during the optimization process. Default is False.
    Returns:
    list: The best solution found during the optimization process.
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
                        number_of_iterations_with_same_temperature=50, DEBUG=False, points=None):
    """
    Perform the Simulated Annealing optimization algorithm to find a near-optimal solution for the TSP.
    This version starts from a given initial solution. It is used in the hybrid metaheuristic algorithm.
    Parameters:
        current_solution (list): The initial solution path.
        dist (2D list): The distance matrix representing the TSP.
        T_0 (float): The initial temperature. Default is 1000.
        alpha (float): The cooling rate. Default is 0.95.
        max_iterations (int): The maximum number of iterations. Default is 10000.
        number_of_iterations_with_same_temperature (int): Number of iterations to perform at each temperature level. Default is 50.
        DEBUG (bool): If True, print debug information. Default is False.
        points (list): List of points representing the TSP. Default is None.
    Returns:
        list: The best solution found.
    """
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
            if not check_path(points, current_solution, DEBUG=True):
                input("Nella funzione intermedia SA del ILS_SA, la soluzione intermedia non è valida. Premi invio per continuare...")

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


def complete_simulated_annealing(file_path, T_0=1000, alpha=0.95, max_iterations=10000, number_of_iterations_with_same_temperature=50, DEBUG=False):
    """
    Perform the Simulated Annealing algorithm to solve the Traveling Salesman Problem (TSP).
    Parameters:
        file_path (str): The path to the TSPLIB file containing the TSP instance.
        T_0 (float, optional): The initial temperature. Default is 1000.
        alpha (float, optional): The cooling rate. Default is 0.95.
        max_iterations (int, optional): The maximum number of iterations. Default is 10000.
        number_of_iterations_with_same_temperature (int, optional): The number of iterations to perform at the same temperature before cooling. Default is 50.
        DEBUG (bool, optional): If True, print debug information. Default is False.
    Returns:
        tuple: A tuple containing the best solution found and its cost.
    """
    # Inizializzazione
    n, points, dist = readTSPLIB(file_path)
    if n > 2000:
        current_solution = generate_random_path(n)
    else:
        current_solution = nearest_neighbor_second(points, dist)

    if not check_path(points, current_solution, DEBUG=True):
        input("Nella funzione SA, la soluzione iniziale non è valida. Premi invio per continuare...")
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
    
    # Calcolo delle iterazioni totali previste per tqdm
    with tqdm(total=max_iterations, desc="Simulated Annealing Progress") as pbar:
        while T > T_min and total_iterations < max_iterations:
            for iteration in range(number_of_iterations_with_same_temperature):
                total_iterations += 1
                pbar.update(1)  # Aggiorna la barra di progresso
                
                if DEBUG:  # Stampa periodica ogni 10 iterazioni
                    print(f"Temperatura attuale: {T:.4f}")

                # Genera il vicinato usando il metodo 2-opt
                neighbor_solution = two_opt_single_neighbor(current_solution)
                
                if not check_path(points, current_solution, DEBUG=True):
                    input("Nella funzione SA, una soluzione intermedia non è valida. Premi invio per continuare...")
                neighbor_cost = path_length(dist, neighbor_solution)

                # Calcolo della differenza di costo
                delta = neighbor_cost - current_cost

                # Decidi se accettare la nuova soluzione
                if delta < 0 or random.uniform(0, 1) < math.exp(-delta / T):
                    if DEBUG:
                        if delta < 0:
                            print(f"Nuova soluzione CORRENTE, perchè MIGLIORE di {delta}. Costo {neighbor_cost}")
                        else:
                            print(f"Nuova soluzione CORRENTE, anche se PEGGIORE di {delta}. Costo {neighbor_cost}")
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
    return best_solution, path_length(dist, best_solution)


def iterated_local_search(file_path, max_iterations, DEBUG=False):
    """
    Perform Iterated Local Search (ILS) to solve the Traveling Salesman Problem (TSP).
    Parameters:
        file_path (str): Path to the TSPLIB file containing the TSP instance.
        max_iterations (int): Maximum number of iterations for the ILS algorithm.
        DEBUG (bool): If True, print debug information. Default is False.
    Returns:
        tuple: A tuple containing the best solution found and its path length.
    """
    n, points, dist = readTSPLIB(file_path)

    if n > 2000:
        current_solution = generate_random_path(n)
    else:
        current_solution = nearest_neighbor_second(points, dist)

    if DEBUG:
        print("Costo della soluzione iniziale:", path_length(dist, current_solution))
        
        
    if not check_path(points, current_solution, DEBUG=True):
        input("Nella funzione ILS, la soluzione iniziale non è valida. Premi invio per continuare...")
        
    best_solution = local_search_optimized(dist, current_solution) 
    
    if not check_path(points, current_solution, DEBUG=True):
        input("Nella funzione ILS, la prima soluzione locale non è valida. Premi invio per continuare...")
    
    no_improvement_count = 0
    max_no_improvement = 20  # Numero massimo di iterazioni senza miglioramenti

    for iteration in tqdm(range(max_iterations), desc="Iterated Local Search Progress"):
        # Perturba la soluzione
        new_solution = multi_swap(best_solution, k=n//25 , points=points, DEBUG=DEBUG)
        if not check_path(points, current_solution, DEBUG=True):
            input("Nella funzione ILS, la soluzione perturbata locale non è valida. Premi invio per continuare...")

        # Applica SA alla soluzione perturbata
        if n > 500:
            new_solution =  local_search_optimized(dist, new_solution)
        else:
            new_solution = local_search(dist, new_solution, two_opt_neighborhood) 
            
        if not check_path(points, current_solution, DEBUG=True):
            input("Nella funzione ILS, la soluzione locale intermedia non è valida. Premi invio per continuare...")

        # Aggiorna la soluzione corrente e globale
        if path_length(dist, new_solution) < path_length(dist, best_solution):
            best_solution = new_solution
            no_improvement_count = 0  # Reset se troviamo un miglioramento
        else:
            no_improvement_count += 1

        if no_improvement_count >= max_no_improvement:
            if DEBUG:
                print(f"Stopping early at iteration {iteration} due to no improvement.")
            break

    return best_solution, path_length(dist, best_solution)

if __name__ == "__main__":
    # testiamo usando una istanza di esempio
    file_path = "TSP/data/TSP_instances/a280.tsp"

    best_solution, best_length = complete_simulated_annealing(file_path, T_0=1000, alpha=0.95, max_iterations=10000, number_of_iterations_with_same_temperature=50, DEBUG=False)
    print("Costo della soluzione migliore con simulated annealing:", best_length )
    
    # testiamo l'iterated local search
    best_solution, best_length = iterated_local_search(file_path, max_iterations=100)
    print("Costo della soluzione migliore con iterated local search:", best_length)