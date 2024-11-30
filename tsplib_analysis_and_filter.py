import os
import shutil

from tsp_utils import readTSPLIB

# Funzione 1: Parsing del file TSPLIB
def parse_tsplib_instance(file_path):
    """Parsa un file TSPLIB e restituisce le informazioni principali."""
    info = {
        "NAME": os.path.basename(file_path),
        "TYPE": None,
        "EDGE_WEIGHT_TYPE": None,
        "EDGE_WEIGHT_FORMAT": None,
    }
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("TYPE"):
                info["TYPE"] = line.split(":")[1].strip()
            elif line.startswith("EDGE_WEIGHT_TYPE"):
                info["EDGE_WEIGHT_TYPE"] = line.split(":")[1].strip()
            elif line.startswith("EDGE_WEIGHT_FORMAT"):
                info["EDGE_WEIGHT_FORMAT"] = line.split(":")[1].strip()
    
    return info

# Funzione 2: Analisi dei file TSPLIB in una directory
def analyze_tsplib_directory(directory):
    """Analizza una directory di file TSPLIB e restituisce un riepilogo."""
    summary = {
        "total_instances": 0,
        "types": {},
        "edge_weight_types": {},
        "edge_weight_formats": {},
        "missing_edge_weight_format": 0
    }
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".tsp"):
            summary["total_instances"] += 1
            instance_info = parse_tsplib_instance(file_path)
            
            # Controlla i formati mancanti
            if instance_info["EDGE_WEIGHT_FORMAT"] is None:
                summary["missing_edge_weight_format"] += 1

            # Aggiorna le statistiche per TYPE
            instance_type = instance_info["TYPE"]
            if instance_type:
                summary["types"][instance_type] = summary["types"].get(instance_type, 0) + 1
            
            # Aggiorna le statistiche per EDGE_WEIGHT_TYPE
            edge_weight_type = instance_info["EDGE_WEIGHT_TYPE"]
            if edge_weight_type:
                summary["edge_weight_types"][edge_weight_type] = summary["edge_weight_types"].get(edge_weight_type, 0) + 1
            
            # Aggiorna le statistiche per EDGE_WEIGHT_FORMAT
            edge_weight_format = instance_info["EDGE_WEIGHT_FORMAT"]
            if edge_weight_format:
                summary["edge_weight_formats"][edge_weight_format] = summary["edge_weight_formats"].get(edge_weight_format, 0) + 1
    
    return summary

# Funzione 3: Raggruppare i file per tipo di distanza
def list_files_by_distance_type(directory):
    """Crea una lista di file raggruppati per EDGE_WEIGHT_TYPE."""
    files_by_type = {}
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".tsp"):
            instance_info = parse_tsplib_instance(file_path)
            edge_weight_type = instance_info["EDGE_WEIGHT_TYPE"]
            
            if edge_weight_type:
                if edge_weight_type not in files_by_type:
                    files_by_type[edge_weight_type] = []
                files_by_type[edge_weight_type].append(instance_info["NAME"])
    
    return files_by_type

# Funzione 4: Filtrare i file TSPLIB per tipo di distanza
def filter_tsplib_files(source_dir, dest_dir, valid_types={"EUC_2D"}, max_nodes=10000):
    """
    Filtra i file TSPLIB mantenendo solo quelli con EDGE_WEIGHT_TYPE specificati
    e meno di max_nodes nodi.
    
    Args:
        source_dir (str): Directory sorgente con i file TSPLIB.
        dest_dir (str): Directory di destinazione per i file filtrati.
        valid_types (set): Tipi validi di EDGE_WEIGHT_TYPE.
        max_nodes (int): Numero massimo di nodi da mantenere.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path) and filename.endswith(".tsp"):
            with open(file_path, 'r') as file:
                edge_weight_type = None
                dimension = None
                for line in file:
                    line = line.strip()
                    if line.startswith("EDGE_WEIGHT_TYPE"):
                        edge_weight_type = line.split(":")[1].strip()
                    elif line.startswith("DIMENSION"):
                        dimension = int(line.split(":")[1].strip())
                    # Termina la lettura se entrambi i valori sono trovati
                    if edge_weight_type and dimension:
                        break
                
                # Filtra per tipo di distanza e dimensione
                if edge_weight_type in valid_types and dimension < max_nodes:
                    shutil.copy(file_path, os.path.join(dest_dir, filename))

def filter_solutions(solution_file, filtered_directory, output_file):
    """Filtra il file delle soluzioni mantenendo solo quelle per le istanze filtrate."""
    # Ottieni i nomi delle istanze nella directory filtrata
    valid_instances = set(
        os.path.splitext(filename)[0]
        for filename in os.listdir(filtered_directory)
        if filename.endswith(".tsp")
    )
    
    with open(solution_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Ottieni il nome dell'istanza (prima di `:`)
            instance_name = line.split(":")[0].strip()
            
            # Scrivi la soluzione solo se è presente nella directory filtrata
            if instance_name in valid_instances:
                outfile.write(line)

# Esempio di utilizzo

# Script principale
# if __name__ == "__main__":
#     # Percorsi delle directory
#     source_directory = "new_instances"  # Cambia con il percorso reale della tua directory
#     destination_directory = "new_instances_filtered"
    
#     # Filtro dei file TSPLIB
#     print("Filtraggio dei file in corso...")
#     filter_tsplib_files(source_directory, destination_directory)
#     print(f"File filtrati salvati in: {destination_directory}")
    
#     # Analisi della directory filtrata
#     print("\nAnalisi della directory filtrata...")
#     filtered_summary = analyze_tsplib_directory(destination_directory)
#     print("Totale istanze:", filtered_summary["total_instances"])
#     print("Tipologie di problemi:", filtered_summary["types"])
#     print("Tipi di distanza (EDGE_WEIGHT_TYPE):", filtered_summary["edge_weight_types"])
#     print("Formati dei pesi (EDGE_WEIGHT_FORMAT):", filtered_summary["edge_weight_formats"])
#     print("Istanze senza EDGE_WEIGHT_FORMAT:", filtered_summary["missing_edge_weight_format"])
    
#     # Lista dei file per tipo di distanza
#     print("\nElenco dei file raggruppati per tipo di distanza:")
#     files_by_type = list_files_by_distance_type(destination_directory)
#     for edge_weight_type, files in files_by_type.items():
#         print(f"EDGE_WEIGHT_TYPE: {edge_weight_type}")
#         print("File:", ", ".join(files))
#         print()
    
#     solution_file = "new_instances/solutions"  # Cambia con il percorso del file originale
#     filtered_directory = "new_instances_filtered"  # Directory con i file filtrati
#     output_file = "new_instances_filtered/filtered_solutions"  # Nuovo file per le soluzioni filtrate

#     filter_solutions(solution_file, filtered_directory, output_file)
#     print(f"Soluzioni filtrate salvate in: {output_file}")


if __name__ == "__main__":
    directory_path = "new_instances_filtered"  # Cambia con la directory contenente i file filtrati
    
    # Controlla che la directory esista
    if not os.path.exists(directory_path):
        print(f"Errore: La directory '{directory_path}' non esiste.")
        exit(1)
    
    # Itera sui file nella directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Verifica che sia un file TSPLIB
        if os.path.isfile(file_path) and filename.endswith(".tsp"):
            print(f"\nAnalizzando il file: {filename}")
            
            # Leggi il file usando readTSPLIB
            try:
                n, points, dist = readTSPLIB(file_path)
                print(f"Numero di nodi (DIMENSION): {n}")
                print("Punti (coordinate):")
                for i, point in enumerate(points, start=1):
                    print(f"  Nodo {i}: {point}")
                print("Esempio distanze (prime 5):")
                for k, (edge, weight) in enumerate(dist.items()):
                    if k >= 5:  # Stampa solo le prime 5 distanze per esempio
                        break
                    print(f"  {edge}: {weight}")
            except Exception as e:
                print(f"Errore durante la lettura di '{filename}': {e}")
        # input("Premi INVIO per continuare...")