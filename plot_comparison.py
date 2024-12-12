import argparse
import matplotlib.pyplot as plt
import json
import os
import numpy as np

def extract_number(folder_name):
    """Estrae il numero dalla stringa della cartella per ordinare in modo incrementale."""
    return int(''.join(filter(str.isdigit, folder_name)))

def plot_comparisons_by_dimension(base_folder):

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
    Plotta i risultati dei file JSON generati per ogni dimensione, in finestre separate.
    
    Args:
        base_folder (str): Cartella principale contenente le sottocartelle delle dimensioni.
        save_plots (bool): Se True, salva i grafici in una cartella dedicata.
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
    )
    
    # Parso gli argomenti dalla linea di comando
    args = parser.parse_args()
    
    # Stampo la cartella selezionata
    print(f"Cartella selezionata: {args.folder}")
    
    # Processo la cartella specificata
    # plot_comparisons_by_dimension_non_normalized(args.folder)
    # plot_comparisons_in_separate_windows_non_normalized(args.folder)
    # plot_comparisons_by_dimension(args.folder)
    plot_comparisons_in_separate_windows(args.folder)