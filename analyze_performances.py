# L'obiettivo di questo file è eseguire il multistart su un set di istanze di cui è noto il percorso ottimo
# Si potrà poi confrontare la soluzione trovata con la soluzione ottima, confrontando il multistart che 
# utiizza l'algoritmo deterministico con quello che utilizza l'algoritmo randomico
# Inoltre si potrà confrontare il multistart con un numero di inizi diverso
# Si può anche confrontare il multistart con due algoritmi per il neighborhood diversi
# Sarà necessario creare una cartella/nuovo dataset con le istanze di cui si conosce il percorso ottimo
# In seguito memorizzare i risultati ottenuti in un file
# Per eseguire il confronto tra le soluzioni è necessario eseguire il file analyze_performances.py

# QUindi in una funzione devo leggere il grafo e il percorso ottimo con le funzioni readTSPLIB, read_optimal_tour
# In seguuio devo eseguire il multistart con i due algoritmi, e poi con un numero di inizi diverso
# Infine devo memorizzare i risultati ottenuti in un file
# Per poi confrotare i risultati ottenuti

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
# - Eliminare commenti inutili
# - Aggiungere commenti per spiegare il codice
# - Modificare come vengano passati i parametri alle funzioni
# - Documentare le funzioni
# - Dare nomi più significativi alle variabili
# - Dare nomi più significativi alle funzioni
# - La lunghezza del percorso ottimo è calcolata male

def save_performances(performances, filename="performances.json"):
    """
    Salva il dizionario delle performances in un file JSON.
    Args:
        performances (dict): Dizionario delle performances da salvare.
        filename (str): Nome del file di output per le performances.
    """
    try:
        with open(filename, "w") as file:
            json.dump(performances, file, indent=4)
        print(f"Performance salvate correttamente in '{filename}'")
    except IOError as e:
        print(f"Errore nel salvataggio delle performances in '{filename}': {e}")

def load_performances(filename="performances.json"):
    """
    Carica il dizionario delle performances da un file JSON.
    Args:
        filename (str): Nome del file da cui caricare le performances.
    Returns:
        dict: Dizionario delle performances caricato dal file.
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
    Salva il dizionario degli optimal lengths in un file JSON.
    Args:
        optimal_lengths (dict): Dizionario degli optimal lengths da salvare.
        filename (str): Nome del file di output per gli optimal lengths.
    """
    try:
        with open(filename, "w") as file:
            json.dump(optimal_lengths, file, indent=4)
        print(f"Optimal lengths salvati correttamente in '{filename}'")
    except IOError as e:
        print(f"Errore nel salvataggio degli optimal lengths in '{filename}': {e}")

def load_optimal_lengths(filename="optimal_lengths.json"):
    """
    Carica il dizionario degli optimal lengths da un file JSON.
    Args:
        filename (str): Nome del file da cui caricare gli optimal lengths.
    Returns:
        dict: Dizionario degli optimal lengths caricato dal file.
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
    Stampa i risultati in modo leggibile.
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
    # Esempio results: defaultdict(<function <lambda> at 0x...>, {})
    
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
        # Esempio n_starts: 5, poi 10, poi 20 (a seconda di num_starts)
        
        for neighborhood_function in neighborhood_functions:
            neighborhood_function_name = neighborhood_function.__name__
            # Esempio neighborhood_function_name: "swap_neighborhood", "two_opt_neighborhood"
            
            # Inizializza un dizionario per le lunghezze di percorso di ciascuna funzione di inizializzazione
            path_length_for_function = {}
            # Esempio path_length_for_function: {} (inizialmente vuoto)

            for path_function in path_functions:
                # Esegui il multistart e ottieni la lunghezza del miglior percorso trovato
                best_path, best_path_length = multistart_local_search(
                    points, dist, path_function, neighborhood_function, n_starts
                )
                # Esempio best_path: [0, 2, 1, ..., 279] (un percorso)
                # Esempio best_path_length: 3062 (distanza totale del percorso)

                path_function_name = path_function.__name__
                # Esempio path_function_name: "nearest_neighbor_second", "nearest_neighbor_random"

                # Aggiungi il risultato per la funzione di percorso corrente
                path_length_for_function[path_function_name] = best_path_length
                # Esempio path_length_for_function:
                # {"nearest_neighbor_second": 3062, "nearest_neighbor_random": 3211}

            # Inserisci i risultati del neighborhood function corrente in results
            results[n_starts][neighborhood_function_name] = path_length_for_function
            # Il singolo risutltato è fatto così:
            #        "file_name": {
            #         number_of_starts: {
            #             neighborhood_function: {
            #                 "best_length_deterministic": 0,
            #                 "best_length_random": 0,
            #                 "optimal_length": 0
            #             }
            #         }
            #     } 
            # Esempio results:
            # {
            #   5: {
            #     "swap_neighborhood": {"nearest_neighbor_second": 3062, "nearest_neighbor_random": 3211},
            #     "two_opt_neighborhood": {"nearest_neighbor_second": 2779, "nearest_neighbor_random": 3195}
            #   },
            #   10: {
            #     "swap_neighborhood": {"nearest_neighbor_second": 3044, "nearest_neighbor_random": 3324},
            #     "two_opt_neighborhood": {"nearest_neighbor_second": 2719, "nearest_neighbor_random": 3158}
            #   },
            #   ...
            # }
            print_readable_dict(results)

    return results, optimal_length
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
#                 "best_length_deterministic": 0,
#                 "best_length_random": 0,
#                 "optimal_length": 0
#             }
#         }
#     }
# }
# Un esemmpio più concreto:
# results = {
#     "a280": {
#         2: {
#             "swap_neighborhood": {
#                 "best_length_deterministic": 0,
#                 "best_length_random": 0,
#                 "optimal_length": 0
#             },
#             "two_opt_neighborhood": {
#                 "best_length_deterministic": 0,
#                 "best_length_random": 0,
#                 "optimal_length": 0
#             }
#         },
#         10: {
#             "swap_neighborhood": {
#                 "best_length_deterministic": 0,
#                 "best_length_random": 0,
#                 "optimal_length": 0
#             },
#             "two_opt_neighborhood": {
#                 "best_length_deterministic": 0,
#                 "best_length_random": 0,
#                 "optimal_length": 0
#             }
#         }
#     }
# }


# Esempio di utilizzo

# results = analyze_single_file("a280.tsp", path_functions=[nearest_neighbor_second, nearest_neighbor_random], neighborhood_functions=[swap_neighborhood, two_opt_neighborhood], num_starts=[1,2,3])
all_results = analyze_performances("TSP_instances_clean/")
