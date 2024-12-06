
from tsp_utils import readTSPLIB
from my_utils import nearest_neighbor_second
from algorithm_metrics import path_length
from perturbation import *
from metaeuristic import simulated_annealing
from tqdm import tqdm
# In questo file costruiremo un'metaeuristica per risolvere il problema del commesso viaggiatore (TSP) su un'istanza TSPLIB.

def ils_sa_tsp(file_path, iterations, DEBUG=False):
    n, points, dist = readTSPLIB(file_path)

    current_solution = nearest_neighbor_second(points, dist)
    if DEBUG:
        print("Costo della soluzione iniziale:", path_length(dist, current_solution))
    
    best_solution = simulated_annealing(current_solution, dist, T_0=1000, alpha=0.95, max_iterations=10000,
                        number_of_iterations_with_same_temperature=10, DEBUG=False)

    no_improvement_count = 0
    max_no_improvement = 10  # Numero massimo di iterazioni senza miglioramenti

    for iteration in tqdm(range(iterations), desc="Iterations"):
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
            if DEBUG:
                print(f"Stopping early at iteration {iteration} due to no improvement.")
            break

    return best_solution, path_length(dist, best_solution)


if __name__ == "__main__":
    # testiamo il simulated annealing
    file_path = "new_instances/pcb3038.tsp"
    n, points, dist = readTSPLIB(file_path)

    best_solution = ils_sa_tsp(file_path, 10)
    # print("Soluzione migliore:", best_solution)
    print("Costo della soluzione migliore:", path_length(dist, best_solution))