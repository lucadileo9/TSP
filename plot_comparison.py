import json
import matplotlib.pyplot as plt
import numpy as np
from metaeuristic_comparison import load_results_from_json

def plot_results(results):
    instances = list(results.keys())  # Nomi delle istanze
    algorithms = ["ILS", "SA", "ILSSA"]  # Algoritmi
    num_algorithms = len(algorithms)

    # Organizza i dati per il grafico
    values = {alg: [results[instance][alg] for instance in instances] for alg in algorithms}

    x = np.arange(len(instances))  # Posizioni delle istanze
    bar_width = 0.25  # Larghezza delle barre

    # Crea la figura
    plt.figure(figsize=(12, 6))

    # Disegna le barre
    for i, alg in enumerate(algorithms):
        plt.bar(x + i * bar_width, values[alg], width=bar_width, label=alg)

    # Personalizza il grafico
    plt.xlabel("Istanze", fontsize=12)
    plt.ylabel("Costo", fontsize=12)
    plt.title("Confronto tra algoritmi sulle istanze TSP", fontsize=14)
    plt.xticks(x + bar_width, instances, rotation=45, ha="right", fontsize=10)
    plt.legend(title="Algoritmi")
    plt.tight_layout()

    # Mostra il grafico
    plt.show()

def plot_grouped_results(results, group_size=10):
    instances = list(results.keys())  # Nomi delle istanze
    algorithms = ["ILS", "SA", "ILSSA"]  # Algoritmi
    num_algorithms = len(algorithms)

    # Calcola il numero di gruppi necessari
    num_groups = (len(instances) + group_size - 1) // group_size

    # Organizza i dati in gruppi
    grouped_instances = [instances[i:i + group_size] for i in range(0, len(instances), group_size)]

    # Crea la figura e i subplot
    fig, axes = plt.subplots(1, num_groups, figsize=(5 * num_groups, 6), constrained_layout=True)

    # Se c'è un solo gruppo, axes è un oggetto singolo, trasformalo in una lista
    if num_groups == 1:
        axes = [axes]

    # Disegna i grafici per ciascun gruppo
    for i, group in enumerate(grouped_instances):
        ax = axes[i]
        values = {alg: [results[instance][alg] for instance in group] for alg in algorithms}

        x = np.arange(len(group))  # Posizioni delle istanze nel gruppo
        bar_width = 0.25  # Larghezza delle barre

        # Disegna le barre per ogni algoritmo
        for j, alg in enumerate(algorithms):
            ax.bar(x + j * bar_width, values[alg], width=bar_width, label=alg)

        # Personalizza ogni subplot
        ax.set_title(f"Gruppo {i + 1}", fontsize=14)
        ax.set_xlabel("Istanze", fontsize=12)
        ax.set_ylabel("Costo", fontsize=12)
        ax.set_xticks(x + bar_width)
        ax.set_xticklabels(group, rotation=45, ha="right", fontsize=10)
        ax.legend(title="Algoritmi")
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Mostra la figura
    plt.suptitle("Confronto tra algoritmi sulle istanze TSP", fontsize=16)
    plt.show()

if __name__ == "__main__":


    # Percorso del file JSON
    results_file_path = "tsp_comparison_results.json"

    # Carica i risultati e genera il grafico
    results = load_results_from_json(results_file_path)
    plot_grouped_results(results, group_size=10)

    plot_results(results)
