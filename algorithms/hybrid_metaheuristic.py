

from perturbation import *
from metaheuristic_algorithms import simulated_annealing
from tqdm import tqdm

from utils.algorithm_metrics import path_length
from utils.path_utils import generate_random_path, nearest_neighbor_second
from utils.tsp_utils import readTSPLIB
# In questo file costruiremo un'metaeuristica per risolvere il problema del commesso viaggiatore (TSP) su un'istanza TSPLIB.

def ils_sa_tsp(file_path, iterations, DEBUG=False):
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
    file_path = "new_instances/fl3795.tsp"

    best_solution, best_length = ils_sa_tsp(file_path, 10)
    print("Soluzione migliore:", best_solution)
    print("Costo della soluzione migliore:", best_length)