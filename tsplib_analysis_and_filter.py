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
def filter_tsplib_files(source_dir, dest_dir, valid_types={"EUC_2D"}, max_nodes=500):
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

def filter_and_organize_tsplib_files(source_dir, dest_dir, valid_types={"EUC_2D"}):
    """
    Filtra i file TSPLIB per EDGE_WEIGHT_TYPE e li organizza in sottocartelle 
    basate sul numero di nodi (DIMENSION).
    
    Args:
        source_dir (str): Directory sorgente con i file TSPLIB.
        dest_dir (str): Directory principale di destinazione.
        valid_types (set): Tipi validi di EDGE_WEIGHT_TYPE.
    """
    # Definizione dei range per le sottocartelle
    ranges = [
        (0, 50, "50_nodes"),
        (51, 100, "100_nodes"),
        (101, 200, "200_nodes"),
        (201, 500, "500_nodes"),
        (501, 1000, "1000_nodes"),
        (1001, 2000, "2000_nodes"),
        (2001, float("inf"), "2000_plus_nodes"),
    ]
    
    # Crea la directory principale di destinazione se non esiste
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
                
                # Verifica se il file soddisfa i criteri
                if edge_weight_type in valid_types and dimension is not None:
                    # Determina il range appropriato
                    for min_nodes, max_nodes, folder_name in ranges:
                        if min_nodes <= dimension <= max_nodes:
                            # Crea la sottocartella se non esiste
                            subfolder = os.path.join(dest_dir, folder_name)
                            if not os.path.exists(subfolder):
                                os.makedirs(subfolder)
                            # Copia il file nella sottocartella appropriata
                            shutil.copy(file_path, os.path.join(subfolder, filename))
                            break


def organize_solutions(solution_file, organized_instances_dir, output_dir):
    """
    Organizza il file delle soluzioni in base alle sottocartelle delle istanze TSPLIB.
    
    Args:
        solution_file (str): Percorso del file originale delle soluzioni.
        organized_instances_dir (str): Directory organizzata con le sottocartelle delle istanze TSPLIB.
        output_dir (str): Directory in cui salvare i file delle soluzioni organizzati.
    """
    # Carica tutte le soluzioni dal file originale in un dizionario
    solutions = {}
    with open(solution_file, 'r') as infile:
        for line in infile:
            parts = line.split(":")
            if len(parts) == 2:
                instance_name = parts[0].strip()
                solution_value = parts[1].strip()
                solutions[instance_name] = solution_value

    # Itera sulle sottocartelle delle istanze organizzate
    for subfolder in os.listdir(organized_instances_dir):
        subfolder_path = os.path.join(organized_instances_dir, subfolder)
        if os.path.isdir(subfolder_path):
            # Trova tutte le istanze nella sottocartella
            instance_files = os.listdir(subfolder_path)
            instance_names = {os.path.splitext(filename)[0] for filename in instance_files if filename.endswith(".tsp")}
            
            # Crea un file delle soluzioni per questa sottocartella
            solutions_file_path = os.path.join(subfolder_path, "solutions.txt")
            with open(solutions_file_path, 'w') as outfile:
                for instance_name in instance_names:
                    if instance_name in solutions:
                        outfile.write(f"{instance_name} : {solutions[instance_name]}\n")
            
            print(f"File delle soluzioni salvato in: {solutions_file_path}")


# Script principale
if __name__ == "__main__":
       #___________________ FILTRAGGIO DEI FILE TSPLIB E DELLE SOLUZIONI ___________________ 
    # # Percorsi delle directory
    source_directory = "new_instances"  # Cambia con il percorso reale della tua directory
    destination_directory = "new_instances_filtered"
    
    # Filtro dei file TSPLIB
    print("Filtraggio dei file in corso...")
    filter_tsplib_files(source_directory, destination_directory, valid_types={"EUC_2D"}, max_nodes=500)
    print(f"File filtrati salvati in: {destination_directory}")
    
    solution_file = "new_instances/solutions"  # Cambia con il percorso del file originale
    filtered_directory = "new_instances_filtered"  # Directory con i file filtrati
    output_file = "new_instances_filtered/solutions"  # Nuovo file per le soluzioni filtrate

    filter_solutions(solution_file, filtered_directory, output_file)
    print(f"Soluzioni filtrate salvate in: {output_file}")

    # ___________________ FILTRAGGIO E ORGANIZZAZIONE DEI FILE TSPLIB ___________________
    source_directory = "new_instances_filtered"  # Cambia con il percorso della directory sorgente
    destination_directory = "organized_instances"  # Directory principale di destinazione
    
    print("Filtraggio e organizzazione dei file per EDGE_WEIGHT_TYPE e DIMENSION...")
    filter_and_organize_tsplib_files(source_directory, destination_directory, valid_types={"EUC_2D"})
    print(f"File organizzati salvati in: {destination_directory}")
    # PER CARICARE LE SOLUZIONI
    solution_file_path = "new_instances/solutions"  # File originale delle soluzioni
    organized_instances_path = "organized_instances"  # Directory con le istanze organizzate
    output_solutions_path = "organized_solutions"  # Directory per i file delle soluzioni organizzati
    
    print("Organizzazione delle soluzioni in corso...")
    organize_solutions(solution_file_path, organized_instances_path, output_solutions_path)
    print(f"Soluzioni organizzate salvate in: {output_solutions_path}")



    # #___________________ ANALISI DEI FILE TSPLIB ___________________
    # # Analisi della directory filtrata
    # print(f"\nAnalisi della directory {destination_directory}...")
    # filtered_summary = analyze_tsplib_directory(source_directory)
    # print("Totale istanze:", filtered_summary["total_instances"])
    # print("Tipologie di problemi:", filtered_summary["types"])
    # print("Tipi di distanza (EDGE_WEIGHT_TYPE):", filtered_summary["edge_weight_types"])
    # print("Formati dei pesi (EDGE_WEIGHT_FORMAT):", filtered_summary["edge_weight_formats"])
    # print("Istanze senza EDGE_WEIGHT_FORMAT:", filtered_summary["missing_edge_weight_format"])
    
    # #___________________ RAGGRUPPAMENTO DEI FILE PER TIPO DI DISTANZA ___________________
    # # Lista dei file per tipo di distanza
    # print("\nElenco dei file raggruppati per tipo di distanza:")
    # files_by_type = list_files_by_distance_type(source_directory)
    # for edge_weight_type, files in files_by_type.items():
    #     print(f"EDGE_WEIGHT_TYPE: {edge_weight_type}")
    #     print("File:", ", ".join(files))
    #     print()