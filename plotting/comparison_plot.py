'''
This script generates comparison plots for different optimization algorithms (ILS, SA, ILSSA) against the optimal cost
for various instances of the Traveling Salesman Problem (TSP). The script reads JSON files containing the comparison
results from subdirectories within a specified base folder. Each subdirectory represents a different problem dimension
and contains a JSON file with the comparison results.
Functions:
    extract_number(folder_name):
    plot_comparisons_by_dimension(base_folder):
        Plots comparison bar charts for different dimensions based on JSON results. Generates subplots for each dimension,
        with bars representing the normalized costs of ILS, SA, and ILSSA, and scatter points for the optimal cost.
    plot_comparisons_in_separate_windows(base_folder, save_plots=False):
        Plots comparison graphs for different dimensions in separate windows or saves the plots to a specified folder.
        Normalizes the costs with respect to the optimal cost.
    plot_comparisons_by_dimension_non_normalized(base_folder):
        Plots comparison of costs for different optimization algorithms across multiple dimensions without normalizing the costs.
        Generates subplots for each dimension, with bars representing the costs of ILS, SA, and ILSSA, and scatter points for the optimal cost.
    plot_comparisons_in_separate_windows_non_normalized(base_folder):
        Plots comparison results from JSON files in separate windows for each dimension folder without normalizing the costs.
        Generates bar plots for each dimension folder, displaying the costs of the algorithms and the optimal cost for each instance.
Usage:
    Run the script with the following command:
        python comparison_plot.py <folder> [--save_plots]
    Arguments:
        folder (str): The base folder containing subdirectories for each dimension. Default is "TSP/data/EUC_2D".
        --save_plots: If specified, saves the plots to a folder named '<base_folder>_plot'. Otherwise, displays the plots in separate windows.

'''
import argparse
import matplotlib.pyplot as plt
import json
import os
import numpy as np

def extract_number(folder_name):
    """
    Extracts and returns the first sequence of digits found in the given folder name.

    Args:
        folder_name (str): The name of the folder from which to extract the number.

    Returns:
        int: The extracted number as an integer.

    Raises:
        ValueError: If no digits are found in the folder name.
    """
    return int(''.join(filter(str.isdigit, folder_name)))

def plot_comparisons_by_dimension(base_folder):
    """
    Plots comparison bar charts for different dimensions based on JSON results.
    This function reads JSON files from subdirectories within the specified base folder.
    Each subdirectory represents a different dimension and contains a JSON file with
    comparison results for various instances. The function generates bar charts comparing
    the normalized costs of different algorithms (ILS, SA, ILSSA) against the optimal cost.
    Parameters:
        base_folder (str): The path to the base folder containing subdirectories for each dimension.
        The JSON files should be named in the format "{dimension}_comparison_results.json" and
        should contain a dictionary where keys are instance names and values are dictionaries
        with keys "ILS", "SA", "ILSSA", and "Optimal Cost".
        Example JSON structure:
        {
            "instance1": {
                "ILS": 1234,
                "SA": 5678,
                "ILSSA": 91011,
                "Optimal Cost": 1000
            },
            "instance2": {
                "ILS": 2345,
                "SA": 6789,
                "ILSSA": 101112,
                "Optimal Cost": 2000
            }
        }
        The function generates a subplot for each dimension, with bars representing the
        normalized costs of ILS, SA, and ILSSA, and scatter points for the optimal cost.
    Returns:
        None
    """

    dimension_folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    dimension_folders = sorted(dimension_folders, key=extract_number)  # Ordina per dimensione
    
    num_dimensions = len(dimension_folders)
    fig, axes = plt.subplots(1, num_dimensions, figsize=(15, 6), sharey=True)
    
    for i, folder in enumerate((dimension_folders)):
        json_file = os.path.join(base_folder, folder, f"{folder}_comparison_results.json")
        
        if not os.path.exists(json_file):
            print(f"File JSON non trovato per la cartella {folder}")
            continue
        
        with open(json_file, "r") as f:
            results = json.load(f)
        
        instances = list(results.keys())
        ils_costs = [results[inst]["ILS"] / results[inst]["Optimal Cost"] for inst in instances]
        sa_costs = [results[inst]["SA"] / results[inst]["Optimal Cost"] for inst in instances]
        ils_sa_costs = [results[inst]["ILSSA"] / results[inst]["Optimal Cost"] for inst in instances]
        optimal_costs = [1] * len(instances)  # Valore normalizzato dell'ottimo
        
        x = np.arange(len(instances))
        bar_width = 0.2
        
        axes[i].bar(x - bar_width, ils_costs, width=bar_width, label="ILS", color="blue")
        axes[i].bar(x, sa_costs, width=bar_width, label="SA", color="green")
        axes[i].bar(x + bar_width, ils_sa_costs, width=bar_width, label="ILSSA", color="red")
        
        # Aggiungi punti per l'ottimo
        axes[i].scatter(x, optimal_costs, color="black", label="Optimal Cost", zorder=5)
        
        axes[i].set_title(folder)
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(instances, rotation=45, ha="right")
        
        if i == 0:
            axes[i].set_ylabel("Costo Normalizzato")
    
    axes[0].legend()
    plt.tight_layout()
    plt.show()
    
    
def plot_comparisons_in_separate_windows(base_folder, save_plots=False):
    """
    Plots comparison graphs for different dimensions in separate windows.
    This function reads JSON files containing comparison results for different dimensions,
    normalizes the costs with respect to the optimal cost, and plots the results in separate
    windows or saves the plots to a specified folder.
    Parameters:
        base_folder (str): The base folder containing subfolders for each dimension. Each subfolder
                        should contain a JSON file named '<dimension>_comparison_results.json'.
        save_plots (bool): If True, saves the plots to a folder named '<base_folder>_plot'. If False,
                        displays the plots in separate windows. Default is False.
    Returns:
        None
    """
    # Ottieni tutte le sottocartelle (dimensioni)
    dimension_folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    dimension_folders = sorted(dimension_folders, key=extract_number)  # Ordina per dimensione

    # Crea la cartella per i plot se necessario
    if save_plots:
        plot_folder = f"{base_folder}_plot"
        os.makedirs(plot_folder, exist_ok=True)

    for folder in dimension_folders:
        json_file = os.path.join(base_folder, folder, f"{folder}_comparison_results.json")

        if not os.path.exists(json_file):
            print(f"File JSON non trovato per la cartella {folder}")
            continue

        # Carica i risultati
        with open(json_file, "r") as f:
            results = json.load(f)

        # Estrai dati
        instances = list(results.keys())
        ils_costs = [results[inst]["ILS"] for inst in instances]
        sa_costs = [results[inst]["SA"] for inst in instances]
        ils_sa_costs = [results[inst]["ILSSA"] for inst in instances]
        optimal_costs = [results[inst]["Optimal Cost"] for inst in instances]

        # Calcola i valori normalizzati (rispetto alla soluzione ottima)
        normalized_ils = [ils / opt if opt else None for ils, opt in zip(ils_costs, optimal_costs)]
        normalized_sa = [sa / opt if opt else None for sa, opt in zip(sa_costs, optimal_costs)]
        normalized_ils_sa = [ils_sa / opt if opt else None for ils_sa, opt in zip(ils_sa_costs, optimal_costs)]

        # Crea una nuova finestra per questa dimensione
        plt.figure(figsize=(10, 6))

        # Plot delle barre
        x = np.arange(len(instances))  # Indici delle istanze
        bar_width = 0.2

        plt.bar(x - bar_width, normalized_ils, width=bar_width, label="ILS", color="blue")
        plt.bar(x, normalized_sa, width=bar_width, label="SA", color="green")
        plt.bar(x + bar_width, normalized_ils_sa, width=bar_width, label="ILSSA", color="red")

        # Aggiungi punti per l'ottimo
        plt.scatter(x, [1] * len(instances), color="black", label="Optimal Cost", zorder=5)

        # Titolo, asse e legenda
        plt.title(f"Confronto per dimensione: {folder}")
        plt.xticks(x, instances, rotation=45, ha="right")
        plt.ylabel("Costo Normalizzato")
        plt.legend()

        # Layout
        plt.tight_layout()

        # Salva il grafico o mostra
        if save_plots:
            plot_path = os.path.join(plot_folder, f"{folder}_plot.png")
            plt.savefig(plot_path)
            print(f"Grafico salvato in: {plot_path}")
        else:
            plt.show()

        # Chiudi la figura per evitare memory leak
        plt.close()
def plot_comparisons_by_dimension_non_normalized(base_folder):
    """
    Plots comparison of costs for different optimization algorithms across multiple dimensions.
    This function reads JSON files from subdirectories within the specified base folder. Each subdirectory
    corresponds to a different problem dimension and contains a JSON file with comparison results for 
    different optimization algorithms (ILS, SA, ILSSA) and the optimal cost. The function generates a 
    bar plot for each dimension, comparing the costs of the algorithms and the optimal cost.
    The costs are not normalized in this version of the plot. (i.e., found cost / optimal cost)
    Parameters:
        base_folder (str): The path to the base folder containing subdirectories for each dimension. Each 
                        subdirectory should contain a JSON file named '{dimension}_comparison_results.json'.
        The JSON file structure should be as follows:
        {
            "instance_name_1": {
                "ILS": cost_value,
                "SA": cost_value,
                "ILSSA": cost_value,
                "Optimal Cost": cost_value
            },
            "instance_name_2": {
                "ILS": cost_value,
                "SA": cost_value,
                "ILSSA": cost_value,
                "Optimal Cost": cost_value
            },
            ...
        }
        The function will create a subplot for each dimension, with bars representing the costs of ILS, SA, 
        and ILSSA algorithms, and scatter points for the optimal costs.
    Returns:
        None
    """
    
    dimension_folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    dimension_folders = sorted(dimension_folders, key=extract_number)  # Ordina per dimensione
    
    num_dimensions = len(dimension_folders)
    fig, axes = plt.subplots(1, num_dimensions, figsize=(15, 6), sharey=True)
    
    for i, folder in enumerate((dimension_folders)):
        json_file = os.path.join(base_folder, folder, f"{folder}_comparison_results.json")
        
        if not os.path.exists(json_file):
            print(f"File JSON non trovato per la cartella {folder}")
            continue
        
        with open(json_file, "r") as f:
            results = json.load(f)
        
        instances = list(results.keys())
        ils_costs = [results[inst]["ILS"] for inst in instances]
        sa_costs = [results[inst]["SA"] for inst in instances]
        ils_sa_costs = [results[inst]["ILSSA"] for inst in instances]
        optimal_costs = [results[inst]["Optimal Cost"] for inst in instances]
        
        x = np.arange(len(instances))
        bar_width = 0.2
        
        axes[i].bar(x - bar_width, ils_costs, width=bar_width, label="ILS", color="blue")
        axes[i].bar(x, sa_costs, width=bar_width, label="SA", color="green")
        axes[i].bar(x + bar_width, ils_sa_costs, width=bar_width, label="ILSSA", color="red")
        
        # Aggiungi punti per l'ottimo
        axes[i].scatter(x, optimal_costs, color="black", label="Optimal Cost", zorder=5)
        
        axes[i].set_title(folder)
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(instances, rotation=45, ha="right")
        
        if i == 0:
            axes[i].set_ylabel("Costo Assoluto")
    
    axes[0].legend()
    plt.tight_layout()
    plt.show()


def plot_comparisons_in_separate_windows_non_normalized(base_folder):
    """
    Plots comparison results from JSON files in separate windows for each dimension folder.
    This function reads JSON files containing comparison results for different optimization algorithms
    (ILS, SA, ILSSA) and the optimal cost for various instances. It generates bar plots for each dimension
    folder, displaying the costs of the algorithms and the optimal cost for each instance.
    Parameters:
        base_folder (str): The base directory containing dimension folders with JSON comparison results.
        The JSON file for each dimension folder should be named as "{folder}_comparison_results.json" and
        should contain a dictionary with instance names as keys and another dictionary as values. The inner
        dictionary should have the following keys:
            - "ILS": Cost obtained by the ILS algorithm.
            - "SA": Cost obtained by the SA algorithm.
            - "ILSSA": Cost obtained by the ILSSA algorithm.
            - "Optimal Cost": The optimal cost for the instance.
        Example JSON structure:
        {
            "instance1": {
                "ILS": 123,
                "SA": 150,
                "ILSSA": 130,
                "Optimal Cost": 120
            },
            "instance2": {
                "ILS": 200,
                "SA": 210,
                "ILSSA": 205,
                "Optimal Cost": 195
            }
        }
        The function generates a bar plot for each dimension folder, with bars representing the costs of
        the ILS, SA, and ILSSA algorithms, and scatter points representing the optimal costs.
        Note:
        - The function assumes that the dimension folders are named in a way that allows sorting by dimension
        using the `extract_number` function.
        - The function displays the plots using `plt.show()`, which will open a new window for each plot.
    Returns:
        None
    """
    dimension_folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    dimension_folders = sorted(dimension_folders, key=extract_number)  # Ordina per dimensione

    for folder in dimension_folders:
        json_file = os.path.join(base_folder, folder, f"{folder}_comparison_results.json")
        
        if not os.path.exists(json_file):
            print(f"File JSON non trovato per la cartella {folder}")
            continue
        
        with open(json_file, "r") as f:
            results = json.load(f)
        
        instances = list(results.keys())
        ils_costs = [results[inst]["ILS"] for inst in instances]
        sa_costs = [results[inst]["SA"] for inst in instances]
        ils_sa_costs = [results[inst]["ILSSA"] for inst in instances]
        optimal_costs = [results[inst]["Optimal Cost"] for inst in instances]
        
        x = np.arange(len(instances))
        bar_width = 0.2
        
        plt.figure(figsize=(10, 6))
        plt.bar(x - bar_width, ils_costs, width=bar_width, label="ILS", color="blue")
        plt.bar(x, sa_costs, width=bar_width, label="SA", color="green")
        plt.bar(x + bar_width, ils_sa_costs, width=bar_width, label="ILSSA", color="red")
        
        # Aggiungi punti per l'ottimo
        plt.scatter(x, optimal_costs, color="black", label="Optimal Cost", zorder=5)
        
        plt.title(f"Confronto per dimensione: {folder}")
        plt.xticks(x, instances, rotation=45, ha="right")
        plt.ylabel("Costo Assoluto")
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera i plot di una cartella specifica.")
    parser.add_argument(
        "folder", 
        type=str, 
        nargs="?", 
        default="TSP/data/EUC_2D"
    )
    # l'utente può anche decidere se salvare i plot in una cartella dedicata
    parser.add_argument(
        "--save_plots", 
        action="store_true", 
        help="Salva i plot in una cartella dedicata."
    )
    
    # Parso gli argomenti dalla linea di comando
    args = parser.parse_args()
    
    # Stampo la cartella selezionata
    print(f"Cartella selezionata: {args.folder}")
    
    # Processo la cartella specificata
    # plot_comparisons_by_dimension_non_normalized(args.folder)
    # plot_comparisons_in_separate_windows_non_normalized(args.folder)
    # plot_comparisons_by_dimension(args.folder)
    plot_comparisons_in_separate_windows(args.folder, args.save_plots)