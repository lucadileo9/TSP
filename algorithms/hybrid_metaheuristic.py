'''
This module implements a hybrid metaheuristic algorithm combining Iterated Local Search (ILS) and Simulated Annealing (SA) 
to solve the Traveling Salesman Problem (TSP). The main function `ils_sa_tsp` reads a TSP instance from a TSPLIB file, 
generates an initial solution, and iteratively improves it using perturbation and simulated annealing.
Functions:
    ils_sa_tsp(file_path, iterations, DEBUG=False):
Usage:
    To execute this module, run it as a script. It will test the `ils_sa_tsp` function using a sample TSP instance file.
    Example:
        python hybrid_metaheuristic.py
    This will read the TSP instance from "TSP/data/new_instances/a280.tsp", run the ILS-SA algorithm for 10 iterations, 
    and print the best solution and its cost.à
    You can change the file path and number of iterations by modifying the arguments of the `ils_sa_tsp` function.
'''

from .perturbation import *
from .metaheuristic_algorithms import simulated_annealing
from tqdm import tqdm

from ..utils.algorithm_metrics import path_length
from ..utils.path_utils import generate_random_path, nearest_neighbor_second
from ..utils.tsp_utils import readTSPLIB

def ils_sa_tsp(file_path, iterations, DEBUG=False):
    """
    Perform Iterated Local Search (ILS) combined with Simulated Annealing (SA) to solve the Traveling Salesman Problem (TSP).
    Args:
        file_path (str): Path to the TSPLIB file containing the TSP instance.
        iterations (int): Number of iterations for the ILS algorithm.
        DEBUG (bool, optional): If True, print debug information. Default is False.
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
        input("Nella funzione ils_sa_tsp, la soluzione iniziale non è valida. Premi invio per continuare...")
    best_solution = simulated_annealing(current_solution, dist, T_0=1000, alpha=0.95, max_iterations=10000,
                        number_of_iterations_with_same_temperature=50, DEBUG=False, points=points)

    if not check_path(points, current_solution, DEBUG=True):
        input("Nella funzione ils_sa_tsp, la soluzione migliore non è valida. Premi invio per continuare...")
        
    no_improvement_count = 0
    max_no_improvement = iterations  # Numero massimo di iterazioni senza miglioramenti

    for iteration in tqdm(range(iterations), desc="ILS-SA"):
        # Calcola la fase corrente
        progress = iteration / iterations
        if progress < 0.5:
            phase = "aggressive"
        elif progress < 0.8:
            phase = "medium"
        else:
            phase = "soft"

        # Applica la perturbazione basata sulla fase
        new_solution = perturbation(best_solution, phase, points, n)
        #new_solution = multi_swap(best_solution, k=n//50 , points=points, DEBUG=False)
        
        if not check_path(points, current_solution, DEBUG=True):
            input("Nella funzione ils_sa_tsp, la soluzione perturbata non è valida. Premi invio per continuare...")
        # Applica SA alla soluzione perturbata
        new_solution = simulated_annealing(new_solution, dist, T_0=1000, alpha=0.95, max_iterations=10000,
                        number_of_iterations_with_same_temperature=50, DEBUG=False, points=points)
        
        if not check_path(points, current_solution, DEBUG=True):
            input("Nella funzione ils_sa_tsp, la soluzione intemerdia del SA non è valida. Premi invio per continuare...")
        
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
    # testiamo il simulated annealing
    file_path = "TSP/data/new_instances/a280.tsp"

    best_solution, best_length = ils_sa_tsp(file_path, 10)
    print("Soluzione migliore:", best_solution)
    print("Costo della soluzione migliore:", best_length)