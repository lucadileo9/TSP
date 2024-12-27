'''
This script processes TSP (Traveling Salesman Problem) instances using various metaheuristic algorithms and compares their results.
Functions:
    load_optimal_solutions(file_path="solutions"):
        Load optimal solutions from a file.
    print_results(results):
        Print the comparison of metaheuristic results for different files.
    save_results_to_json(results, filename="tsp_comparison_results.json"):
        Save the given results to a JSON file.
    load_results_from_json(filename="tsp_comparison_results.json"):
        Load results from a JSON file.
    process_instances(instances_folder, optimal_solutions, output_file=None):
        Processes TSP instances and compares the results of different metaheuristic algorithms.
    process_all_folders(base_folder):
        Processes all folders within the given base folder.
Usage:
    Run the script with the desired folder containing TSP instances as an argument:
    python metaheuristic_comparison.py <folder_path>
    If no folder is specified, the default folder "TSP/data/EUC_2D" will be used.

'''
import argparse
import os
import json

from ..utils.tsp_utils import readTSPLIB
from ..utils.algorithm_metrics import path_length
from ..algorithms.metaheuristic_algorithms import iterated_local_search, complete_simulated_annealing
from ..algorithms.hybrid_metaheuristic import ils_sa_tsp

def load_optimal_solutions(file_path="solutions"):
    """
    Load optimal solutions from a file.

    The file should contain lines in the format:
    instance_name: optimal_value

    Args:
        file_path (str): The path to the file containing the optimal solutions. 
                         Default is "solutions".

    Returns:
        dict: A dictionary where the keys are instance names (str) and the values 
              are the corresponding optimal values (int).
    """
    optimal_solutions = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            instance_name = parts[0].strip()
            optimal_value = int(parts[1].strip())
            optimal_solutions[instance_name] = optimal_value
    return optimal_solutions


def print_results(results):
    """
    Print the comparison of metaheuristic results for different files.

    Args:
        results (dict): A dictionary where keys are file names and values are dictionaries
                        containing the distances for different metaheuristics ('ILS', 'SA', 'ILSSA')
                        and the 'Optimal Cost'.

    Example:
        results = {
            'file1.txt': {
                'ILS': 1234,
                'SA': 1250,
                'ILSSA': 1220,
                'Optimal Cost': 1200
            },
            'file2.txt': {
                'ILS': 2345,
                'SA': 2300,
                'ILSSA': 2320,
                'Optimal Cost': None
            }
        }
        print_results(results)
    """
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
    """
    Save the given results to a JSON file.

    Parameters:
        results (dict): The results to be saved, typically a dictionary containing the comparison data.
        filename (str): The name of the file where the results will be saved. Default is "tsp_comparison_results.json".

    Returns:
        None

    Side Effects:
        Writes the results to a JSON file and prints a confirmation message with the filename.
    """
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


def process_instances(instances_folder, optimal_solutions, output_file=None):
    """
    Processes TSP instances and compares the results of different metaheuristic algorithms.
    Args:
        instances_folder (str): The folder containing the TSP instance files.
        optimal_solutions (dict): A dictionary containing the optimal solutions for each instance.
        output_file (str, optional): The file path to save the results in JSON format. Defaults to None.
    Returns:
        dict: A dictionary containing the results of the metaheuristic algorithms for each instance.
    """
    results = {}
    
    # Leggi tutte le istanze
    instance_files = [f for f in os.listdir(instances_folder) if f.endswith('.tsp')]
    
    for file in instance_files:
        file_path = os.path.join(instances_folder, file)
        print(f"Processando l'istanza: {file}")
        
        # Leggi l'istanza
        # n, points, dist = readTSPLIB(file_path)
        
        # Calcola i risultati per ILS, SA e ILSSA
        ils_sa_result, ils_sa_cost = ils_sa_tsp(file_path, 100)
        sa_result, sa_cost = complete_simulated_annealing(file_path, T_0=1000, alpha=0.95, max_iterations=10000, number_of_iterations_with_same_temperature=50, DEBUG=False)
        ils_result, ils_cost= iterated_local_search(file_path, max_iterations=100)
        
        # Ottieni la soluzione ottima per l'istanza
        optimal_value = optimal_solutions.get(file.replace(".tsp", ""), None)
        
        # Memorizza i risultati nel dizionario
        results[file.replace(".tsp", "")] = {
            "ILS": ils_cost,
            "SA": sa_cost,
            "ILSSA": ils_sa_cost,
            "Optimal Cost": optimal_value
        }
    save_results_to_json(results, output_file)
    return results

def process_all_folders(base_folder):
    """
    Processes all folders within the given base folder. For each folder, it loads the optimal solutions
    from a "solutions.txt" file and processes the instances within the folder, saving the comparison
    results to a JSON file.
    Args:
        base_folder (str): The path to the base folder containing subfolders to process.
    Returns:
        None
    """
    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        if os.path.isdir(folder_path):
            # File delle soluzioni e file di output
            optimal_solutions_file = os.path.join(folder_path, "solutions.txt")
            output_file = os.path.join(folder_path, f"{folder}_comparison_results.json")
            
            optimal_solutions=load_optimal_solutions(optimal_solutions_file)
            # Processa le istanze nella cartella
            print(f"Processando la cartella: {folder}")
            process_instances(folder_path, optimal_solutions, output_file)


if __name__ == "__main__":
    # Configurazione argparse
    parser = argparse.ArgumentParser(description="Processa le cartelle in una directory specificata.")
    parser.add_argument(
        "folder", 
        type=str, 
        nargs="?", 
        default="TSP/data/EUC_2D", 
        help="La cartella da processare (default: TSP/data/EUC_2D)"
    )
    
    args = parser.parse_args()
    
    # Stampo la cartella selezionata che contiene le istanze, strutturate per dimensione
    print(f"Cartella selezionata: {args.folder}")
    
    # Processo la cartella specificata
    process_all_folders(args.folder)
