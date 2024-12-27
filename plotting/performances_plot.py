'''
This module provides functions to plot the performance of different TSP algorithms based on various datasets, starting points, neighborhoods, and strategies.
'''
import matplotlib.pyplot as plt
import numpy as np

from ..analysis.analyze_performances import load_optimal_path_lengths, load_performance_data

def abbreviate(label):
    """
    Abbreviates a given label based on predefined mappings.

    This function takes a string label and replaces specific substrings with their
    abbreviated forms according to a predefined mapping dictionary.

    Args:
        label (str): The label to be abbreviated.

    Returns:
        str: The abbreviated label.
    """
    mapping = {
        "swap_neighborhood": "swap",
        "two_opt_neighborhood": "2opt",
        "deterministic": "det",
        "randomic": "rand",
        "start=": "s=",
    }
    for full, short in mapping.items():
        label = label.replace(full, short)
    return label

def first_plot(data, optimal_lengths):
    """
    Plots the performance of different TSP algorithms based on various datasets, starting points, neighborhoods, and strategies.
    Parameters:
    data (dict): A nested dictionary containing the tour lengths for each dataset, start, neighborhood, and strategy.
                 Example structure:
                 {
                     "dataset1": {
                         "1": {
                             "swap_neighborhood": {
                                 "deterministic": value,
                                 "randomic": value
                             },
                             "two_opt_neighborhood": {
                                 "deterministic": value,
                                 "randomic": value
                         },
                         ...
                     },
                     ...
    optimal_lengths (dict): A dictionary containing the optimal tour lengths for each dataset.
                            Example structure:
                            {
                                "dataset1": optimal_value,
                                ...
    Returns:
        None: This function does not return any value. It displays a bar plot with the tour lengths and optimal lengths.
    """
    datasets = list(data.keys())
    neighborhoods = ["swap_neighborhood", "two_opt_neighborhood"]
    strategies = ["deterministic", "randomic"]
    starts = ["1", "2", "5", "10"]

    color_map = {
        ("swap_neighborhood", "deterministic"): "blue",
        ("swap_neighborhood", "randomic"): "lightblue",
        ("two_opt_neighborhood", "deterministic"): "green",
        ("two_opt_neighborhood", "randomic"): "lightgreen",
    }

    
    x_labels = []
    values = []
    optimal = []
    colors = []

    for dataset in datasets:
        for start in starts:
            for neighborhood in neighborhoods:
                for strategy in strategies:
                    x_labels.append(abbreviate(f"{dataset}\ns={start}\n{neighborhood}\n{strategy}"))
                    values.append(data[dataset][start][neighborhood][strategy])
                    optimal.append(optimal_lengths[dataset])
                    colors.append(color_map[(neighborhood, strategy)])

    x = np.arange(len(x_labels))

    # Grafico senza label per la barra principale
    plt.figure(figsize=(18, 8))
    plt.bar(x, values, color=colors, alpha=0.7)
    plt.plot(x, optimal, color="red", linestyle="--", marker="o", label="Optimal Length")

    # Etichette leggibili sull'asse x
    plt.xticks(x, x_labels, rotation=45, ha="right", fontsize=8)
    plt.ylabel("Tour Length")
    plt.title("TSP Performance by Dataset, Start, Neighborhood, and Strategy")

    # Creare una legenda personalizzata
    custom_legend = [
        ("swap_neighborhood - deterministic", "blue"),
        ("swap_neighborhood - randomic", "lightblue"),
        ("two_opt_neighborhood - deterministic", "green"),
        ("two_opt_neighborhood - randomic", "lightgreen"),
    ]
    for label, color in custom_legend:
        plt.bar(0, 0, color=color, label=label)  # Barre invisibili per la legenda

    # Mostrare solo la legenda personalizzata e la linea ottimale
    plt.legend(loc="upper left", fontsize=10)
    plt.tight_layout()
    plt.show()


def second_plot(data, optimal_lengths, max_charts_per_figure=4):
    """
    Plots the performance of different TSP algorithms across multiple datasets.
    Parameters:
        data (dict): A dictionary where keys are dataset names and values are dictionaries
                    containing start points and their corresponding path lengths for different
                    neighborhoods and search types.
        optimal_lengths (dict): A dictionary where keys are dataset names and values are the
                                optimal path lengths for those datasets.
        max_charts_per_figure (int, optional): The maximum number of charts to display per figure.
                                            Default is 4.
    The function generates bar plots for each dataset, showing the path lengths for different
    neighborhoods and search types. It also includes a horizontal line indicating the optimal
    path length. The plots are displayed in multiple figures if the number of datasets exceeds
    the maximum charts per figure.
    """
    datasets = list(data.keys())
    total_datasets = len(datasets)
    num_figures = (total_datasets + max_charts_per_figure - 1) // max_charts_per_figure  # Calcola il numero di figure
    
    # Colori distinti per accoppiare vicinato e tipo di ricerca
    colors = {
        "swap_neighborhood": {"deterministic": "blue", "randomic": "lightblue"},
        "two_opt_neighborhood": {"deterministic": "green", "randomic": "lightgreen"},
    }
    
    # Legenda personalizzata
    custom_legends = [
        ("swap_neighborhood - deterministic", "blue"),
        ("swap_neighborhood - randomic", "lightblue"),
        ("two_opt_neighborhood - deterministic", "green"),
        ("two_opt_neighborhood - randomic", "lightgreen"),
    ]
    
    for fig_index in range(num_figures):
        fig, axs = plt.subplots(2, 2, figsize=(16, 12))
        axs = axs.flatten()
        
        start_index = fig_index * max_charts_per_figure
        end_index = min(start_index + max_charts_per_figure, total_datasets)
        
        for i, dataset_index in enumerate(range(start_index, end_index)):
            dataset = datasets[dataset_index]
            starts = data[dataset]
            optimal_length = optimal_lengths[dataset]
            
            ax = axs[i]
            bar_width = 0.2
            x_positions = np.arange(len(starts))
            offset = 0
            
            for neighborhood, search_results in starts[next(iter(starts))].items():
                for search_type, _ in search_results.items():
                    lengths = [
                        starts[start][neighborhood][search_type]
                        for start in starts
                    ]
                    ax.bar(
                        x_positions + offset,
                        lengths,
                        bar_width,
                        label=f"{neighborhood} - {search_type}" if fig_index == 0 and i == 0 else "",
                        color=colors[neighborhood][search_type]
                    )
                    offset += bar_width

            # Aggiungi linea per la lunghezza ottima
            ax.axhline(optimal_length, color="red", linestyle="--", linewidth=1.5, label="Optimal Path Length")

            ax.set_title(f"File: {dataset}", fontsize=6, pad=15)  # Aggiunge padding al titolo
            ax.set_xlabel("N° Starts", fontsize=6, labelpad=10)  # Riduce la dimensione e aggiunge padding
            ax.set_ylabel("Path Length", fontsize=6, labelpad=10)
            ax.tick_params(axis="both")
            ax.set_xticks(x_positions + bar_width)
            ax.set_xticklabels(starts.keys())
        
        # Rimuove eventuali assi vuoti
        for ax in axs[end_index - start_index:]:
            ax.remove()
        
        # Legenda condivisa
        handles = [plt.Line2D([0], [0], color=color, lw=4) for _, color in custom_legends] + \
                  [plt.Line2D([0], [0], color="red", lw=2, linestyle="--")]
        labels = [desc for desc, _ in custom_legends] + ["Optimal Path Length"]
        fig.legend(handles, labels, loc="upper center", ncol=5, fontsize="small", frameon=False)
        
        # Aggiusta layout per evitare sovrapposizioni
        plt.subplots_adjust(hspace=64)  # Aumenta lo spazio tra i subplot
        fig.tight_layout(rect=[0, 0, 1, 0.95])  # Aggiusta il layout complessivo
        plt.show()

if __name__ == "__main__":
    data = load_performance_data()
    optimal_lengths = load_optimal_path_lengths()

    first_plot(data, optimal_lengths)
    second_plot(data, optimal_lengths)