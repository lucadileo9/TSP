import os
from tsp_utils import readTSPLIB
from algorithm_metrics import path_length
from metaeuristic import iterated_local_search, complete_simulated_annealing
from hybrid_metaeuristic import ils_sa_tsp
import json

def load_optimal_solutions(file_path="solutions"):
    optimal_solutions = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            instance_name = parts[0].strip()
            optimal_value = int(parts[1].strip())
            optimal_solutions[instance_name] = optimal_value
    return optimal_solutions


def print_results(results):
    for file_name, distances in results.items():
        print(f"{file_name}:")
        print(f"  ILS: {distances['ILS']}")
        print(f"  SA: {distances['SA']}")
        print(f"  ILSSA: {distances['ILSSA']}")
        if distances['Optimal Cost'] is not None:
            print(f"  Optimal Cost: {distances['Optimal Cost']}")
        else:
            print(f"  Optimal Cost: N/A")

def save_results_to_json(results, filename="tsp_comparison_results.json"):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Risultati salvati in {filename}")

def load_results_from_json(filename="tsp_comparison_results.json"):
    try:
        with open(filename, 'r') as f:
            results = json.load(f)
        return results
    except FileNotFoundError:
        print(f"Il file {filename} non è stato trovato.")
        return {}
    except json.JSONDecodeError:
        print(f"Errore nel leggere il file {filename}. Assicurati che sia un file JSON valido.")
        return {}


def process_instances(instances_folder, optimal_solutions):
    results = {}
    
    # Leggi tutte le istanze
    instance_files = [f for f in os.listdir(instances_folder) if f.endswith('.tsp')]
    
    for file in instance_files:
        file_path = os.path.join(instances_folder, file)
        
        # Leggi l'istanza
        # n, points, dist = readTSPLIB(file_path)
        
        # Calcola i risultati per ILS, SA e ILSSA
        ils_result, ils_cost = ils_sa_tsp(file_path, 10)
        sa_result, sa_cost = complete_simulated_annealing(file_path, T_0=1000, alpha=0.95, max_iterations=10000, number_of_iterations_with_same_temperature=10, DEBUG=False)
        ils_sa_result, ils_sa_cost= iterated_local_search(file_path, max_iterations=100)
        
        # Ottieni la soluzione ottima per l'istanza
        optimal_value = optimal_solutions.get(file.replace(".tsp", ""), None)
        
        # Memorizza i risultati nel dizionario
        results[file.replace(".tsp", "")] = {
            "ILS": ils_cost,
            "SA": sa_cost,
            "ILSSA": ils_sa_cost,
            "Optimal Cost": optimal_value
        }
    save_results_to_json(results, "tsp_comparison_results.json")
    return results

if __name__ == "__main__":
    # instances_folder = "new_instances"

    # solutions_file_path = os.path.join(instances_folder, "solutions")

    # optimal_solutions = load_optimal_solutions(solutions_file_path)

    # instances_folder = "new_instances_filtered"

    # # Elabora le istanze e ottieni i risultati
    # results = process_instances(instances_folder, optimal_solutions)
    
    # # Stampa i risultati
    # print_results(results)
    result = load_results_from_json()
    print_results(result)

