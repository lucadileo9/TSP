from tsp_utils import readTSPLIB, read_optimal_tour
from local_search import multistart_local_search
from neighborhood import swap_neighborhood, two_opt_neighborhood
from algorithm_metrics import path_length
from my_utils import nearest_neighbor_second, nearest_neighbor_random
from collections import defaultdict
from pathlib import Path
import json
import os

# TODO:
# - Modificare come vengano passati i parametri alle funzioni
# - Dare nomi più significativi alle variabili
# - Dare nomi più significativi alle funzioni


def save_performances(performances, filename="performances.json"):
    """
    Save the given performance data to a JSON file.
    Args:
        performances (dict): A dictionary containing performance data to be saved.
        filename (str, optional): The name of the file where the performance data will be saved. 
                                  Defaults to "performances.json".
    Raises:
        IOError: If there is an error in writing the file.
    Returns:
        None
    """  
    try:
        with open(filename, "w") as file:
            json.dump(performances, file, indent=4)
        print(f"Performance salvate correttamente in '{filename}'")
    except IOError as e:
        print(f"Errore nel salvataggio delle performances in '{filename}': {e}")

def load_performances(filename="performances.json"):
    """
    Load performance data from a JSON file.
    This function attempts to load performance data from the specified JSON file.
    If the file does not exist, it returns an empty dictionary and prints a warning message.
    If the file contains invalid JSON, it returns an empty dictionary and prints an error message.
    If there is an IOError during file access, it returns an empty dictionary and prints an error message.
    Args:
        filename (str): The path to the JSON file containing performance data. Defaults to "performances.json".
    Returns:
        dict: A dictionary containing the performance data, or an empty dictionary if an error occurs.
    """
    if not os.path.exists(filename):
        print(f"Attenzione: il file '{filename}' non esiste. Restituisco un dizionario vuoto.")
        return {}
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Errore di formattazione JSON nel file '{filename}'. Restituisco un dizionario vuoto.")
        return {}
    except IOError as e:
        print(f"Errore nel caricamento delle performances da '{filename}': {e}")
        return {}

def save_optimal_lengths(optimal_lengths, filename="optimal_lengths.json"):
    """
    Save the optimal lengths to a JSON file.
    Parameters:
    optimal_lengths (dict): A dictionary containing the optimal lengths to be saved.
    filename (str): The name of the file where the optimal lengths will be saved. Default is "optimal_lengths.json".
    Returns:
    None
    Raises:
    IOError: If there is an error in writing to the file.
    """
    try:
        with open(filename, "w") as file:
            json.dump(optimal_lengths, file, indent=4)
        print(f"Optimal lengths salvati correttamente in '{filename}'")
    except IOError as e:
        print(f"Errore nel salvataggio degli optimal lengths in '{filename}': {e}")

def load_optimal_lengths(filename="optimal_lengths.json"):
    """
    Load optimal lengths from a JSON file.
    This function attempts to load a dictionary of optimal lengths from a specified JSON file.
    If the file does not exist, it returns an empty dictionary and prints a warning message.
    If there is a JSON formatting error or an IOError, it also returns an empty dictionary and prints an error message.
    Args:
        filename (str): The path to the JSON file containing the optimal lengths. Defaults to "optimal_lengths.json".
    Returns:
        dict: A dictionary containing the optimal lengths if the file is successfully loaded, otherwise an empty dictionary.
    """
    if not os.path.exists(filename):
        print(f"Attenzione: il file '{filename}' non esiste. Restituisco un dizionario vuoto.")
        return {}   
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Errore di formattazione JSON nel file '{filename}'. Restituisco un dizionario vuoto.")
        return {}
    except IOError as e:
        print(f"Errore nel caricamento degli optimal lengths da '{filename}': {e}")
        return {}

def print_results(results):
    """
    Prints the results of the TSP performance analysis in a structured format.

    Args:
        results (dict): A dictionary containing the performance results. The structure of the dictionary is expected to be:
            {
                'dataset_name': {
                    'num_starts': {
                        'neighborhood': {
                            'path_type': length
                        }
                    }
                }
            }
            Where:
                - 'dataset_name' (str) is the name of the dataset.
                - 'num_starts' (int) is the number of starts.
                - 'neighborhood' (str) is the type of neighborhood used.
                - 'path_type' (str) is the type of path (e.g., 'best', 'average').
                - length (float) is the length of the path.
    """
    for dataset, data in results.items():
        print(f"\nDataset: {dataset}")
        for num_starts, neighborhood_data in data.items():
            print(f"  Starts: {num_starts}")
            for neighborhood, lengths in neighborhood_data.items():
                print(f"    Neighborhood: {neighborhood}")
                for path_type, length in lengths.items():
                    print(f"      {path_type}: {length}")

def print_readable_dict(d):
    """
    Prints a nested dictionary in a readable format.

    Args:
        d (dict): A dictionary where the keys are integers representing 
                  the number of starts, and the values are dictionaries 
                  mapping neighborhood names to another dictionary. This 
                  innermost dictionary maps method names to their respective 
                  values.

    Example:
        d = {
            1: {
                'neighborhood1': {
                    'method1': 10,
                    'method2': 20
                },
                'neighborhood2': {
                    'method1': 30,
                    'method2': 40
                }
            },
            2: {
                'neighborhood1': {
                    'method1': 50,
                    'method2': 60
                }
            }
        }
        print_readable_dict(d)
        # Output:
        # N_starts 1:
        #   neighborhood1:
        #     Method1: 10
        #     Method2: 20
        #   neighborhood2:
        #     Method1: 30
        #     Method2: 40
        #
        # N_starts 2:
        #   neighborhood1:
        #     Method1: 50
        #     Method2: 60
    """
    for key, neighborhoods in d.items():
        print(f"N_starts {key}:")
        for neighborhood, methods in neighborhoods.items():
            print(f"  {neighborhood}:")
            for method, value in methods.items():
                print(f"    {method.capitalize()}: {value}")
        print()

def analyze_single_file(dataset_file, best_path_file, path_functions=[], neighborhood_functions=[], num_starts=[5, 10, 20]):
    """
    Analyze the performances of the multistart local search algorithm on a single dataset file.
    Args:
        dataset_file (str): The path to the .tsp dataset file.
        path_functions (list): List of path initialization functions.
        neighborhood_functions (list): List of neighborhood functions.
        num_starts (list): List of random start values.
    Returns:
        dict: A dictionary containing the results for this dataset.
    """
    # Inizializza il dizionario dei risultati con defaultdict per gestire la struttura nidificata
    results = defaultdict(lambda: defaultdict(dict))
    
    # Leggi il grafo e calcola le distanze dai dati .tsp
    n, points, dist = readTSPLIB(dataset_file)
    # Esempio n: 280 (numero di nodi)
    # Esempio points: [(x1, y1), (x2, y2), ...] (coordinate dei punti)
    # Esempio dist: [[0, d1, d2, ...], [d1, 0, d3, ...], ...] (matrice delle distanze)
    
    # Leggi il cammino ottimo e calcola la lunghezza
    optimal_tour = read_optimal_tour(best_path_file ) 
    optimal_length = path_length(dist, optimal_tour)

    # Esegui il multistart con tutte le combinazioni di parametri
    for n_starts in num_starts:        
        for neighborhood_function in neighborhood_functions:
            neighborhood_function_name = neighborhood_function.__name__
            
            # Inizializza un dizionario per le lunghezze di percorso di ciascuna funzione di inizializzazione
            path_length_for_function = {}

            for path_function in path_functions:
                # Esegui il multistart e ottieni la lunghezza del miglior percorso trovato
                best_path, best_path_length = multistart_local_search(
                    points, dist, path_function, neighborhood_function, n_starts
                )
                path_function_name = path_function.__name__
                
                # Aggiungi il risultato per la funzione di percorso corrente
                path_length_for_function[path_function_name] = best_path_length
                # Esempio path_length_for_function:
                # {"nome_1": 1234, "nome_2": 5678}

            # Inserisci i risultati del neighborhood function corrente in results
            results[n_starts][neighborhood_function_name] = path_length_for_function
            # Il singolo risultato è fatto così:
            #         number_of_starts: {
            #             neighborhood_function: {
            #                 "best_length_deterministic": 0,
            #                 "best_length_random": 0,
            #             }
            #         }
            print_readable_dict(results)

    return results, optimal_length
            # Esempio results:
            # {
            #   5: {
            #     "swap_neighborhood": {"deterministic": 3062, "randomic": 3211},
            #     "two_opt_neighborhood": {"deterministic": 2779, "randomic": 3195}
            #   },
            #   10: {
            #     "swap_neighborhood": {"deterministic": 3044, "randomic": 3324},
            #     "two_opt_neighborhood": {"deterministic": 2719, "randomic": 3158}
            #   },
            #   ...
            # }
            # Esempio optimal_length:
            # 2579 , ossia la lunghezza del percorso ottimo per il file corrente

def analyze_performances(dataset_folder):
    """
    Analyze the performances of the multistart local search algorithm across multiple datasets in a single folder.
    Args:
        dataset_folder (str): The path to the folder containing both .tsp dataset files and .opt.tour optimal files.
    Returns:
        dict: A dictionary containing the analysis results and optimal path lengths for each dataset.
    """
    dataset_folder = Path(dataset_folder)
    all_results = {}
    optimal_lengths = {}

    # Filtra i file .tsp e crea un dizionario per i file .opt.tour con il nome base corretto
    tsp_files = [f for f in dataset_folder.glob("*.tsp")]
    # Rimuoviamo l'estensione completa ".opt.tour" per ottenere il nome base
    tour_files = {f.name.replace(".opt.tour", ""): f for f in dataset_folder.glob("*.opt.tour")}

    for tsp_file in tsp_files:
        base_name = tsp_file.stem  # Questo è il nome senza ".tsp"

        if base_name in tour_files:
            single_file_results, optimal_length = analyze_single_file(
                tsp_file,
                tour_files[base_name],
                path_functions=[nearest_neighbor_second],
                neighborhood_functions=[swap_neighborhood, two_opt_neighborhood],
                num_starts=[1]
            )
            all_results[base_name] = single_file_results
            optimal_lengths[base_name] = optimal_length
            print_results(all_results)
            print(optimal_lengths)
        else:
            print(f"Warning: No optimal tour file found for {tsp_file.name}")

    
    save_optimal_lengths(optimal_lengths)
    save_performances(all_results)
    return all_results, optimal_lengths

# Il dizionario con i risultati ottenuti sarà del tipo:
# results = {
#     "file_name": {
#         number_of_starts: {
#             neighborhood_function: {
#                 "deterministic": 0,
#                 "random": 0,
#             }
#         }
#     }
# }
# Un esemmpio più concreto:
 # Esempio
    # {
    #   "a280.tsp": {
    #     5: {
    #       "swap_neighborhood": {"nearest_neighbor_second": 3062, "nearest_neighbor_random": 3211},
    #       "two_opt_neighborhood": {"nearest_neighbor_second": 2779, "nearest_neighbor_random": 3195}
    #     },
    #     10: {
    #       "swap_neighborhood": {"nearest_neighbor_second": 3044, "nearest_neighbor_random": 3324},
    #      "two_opt_neighborhood": {"nearest_neighbor_second": 2719, "nearest_neighbor_random": 3158}
    #     },
    #     ...
    #   }
    # }

if __name__ == "__main__":
    # Esempio di utilizzo
    # results = analyze_single_file("a280.tsp", path_functions=[nearest_neighbor_second, nearest_neighbor_random], neighborhood_functions=[swap_neighborhood, two_opt_neighborhood], num_starts=[1,2,3])
    all_results = analyze_performances("TSP_instances_clean/")
    print_results(all_results)