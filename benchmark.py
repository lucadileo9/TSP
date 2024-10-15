# Adesso devo fare in modo di creare dei file che contengano varie isanze di grafi. 
# Queste varie istanze devono essere differenziate nei seguenti modi:
# - tipo di grafo: euclideo o geometrico
# - numero di vertici: 10, 50, 100, 500, 1000
# - massimo valore delle coordinate: 10, 100, 1000
# Il numero di istanze per ogni tipologia di grafo deve essere 20.
# Per adesso mi concentro solo sul grafo euclideo.
# La struttura della directory è la seguente:
# - data
#     - euclidean
#         - NumVertici 10
#             - MaxValCoord 10
#               - 20 istanze 
#             - MaxValCoord 100
#               - 20 istanze 
#             - MaxValCoord 1000
#               - 20 istanze
#         - NumVertici 50
#             - MaxValCoord 10
#               - 20 istanze
#             - MaxValCoord 100
#               - 20 istanze
#             - MaxValCoord 1000
#               - 20 istanze
#         - NumVertici 100
#             - MaxValCoord 10
#               - 20 istanze
#             - MaxValCoord 100
#               - 20 istanze
#             - MaxValCoord 1000
#               - 20 istanze
#         - NumVertici 500
#             - MaxValCoord 10
#               - 20 istanze
#             - MaxValCoord 100
#               - 20 istanze
#             - MaxValCoord 1000
#               - 20 istanze
#         - NumVertici 1000
#             - MaxValCoord 10
#               - 20 istanze
#             - MaxValCoord 100
#               - 20 istanze
#             - MaxValCoord 1000
#               - 20 istanze
#     - GraphGeo
#         - NumVertici 10
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000
#         - NumVertici 50
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000
#         - NumVertici 100
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000
#         - NumVertici 500
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000
#         - NumVertici 1000
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000
#     - Graph2D
#         - NumVertici 10
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000
#         - NumVertici 50
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000
#         - NumVertici 100
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000
#         - NumVertici 500
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000
#         - NumVertici 1000
#             - MaxValCoord 10
#             - MaxValCoord 100
#             - MaxValCoord 1000

import os
import csv
import tsp_utils
import shutil
from tqdm import tqdm

def generate_all_benchmark():
    """
    Generates benchmark datasets for different types of graphs and saves them to specified directories.

    This function calls `generate_benchmark` with various parameters to create datasets for:
    - Euclidean graphs
    - Geographical graphs
    - 2D graphs

    The datasets are generated with different sizes and saved in the respective directories.

    Parameters:
    None

    Returns:
    None
    """
    generate_benchmark([10, 50, 100, 500, 1000], [50, 100, 1000], tsp_utils.randomEuclGraph, 20, "./data/euclidean")
    generate_benchmark([10, 50, 100, 500, 1000], [10, 100, 1000], tsp_utils.randomGraphGeo, 20, "./data/graphGeo")
    generate_benchmark([10, 50, 100, 500, 1000], [10, 100, 1000], tsp_utils.randomGraph2D, 20, "./data/graph2D")    
    
def generate_benchmark(num_vertices_list, max_coords_list, function,  num_instances, output_dir):
    """
    Generates random Euclidean graphs and saves them in structured folders.

    Args:
        num_vertices_list (list): List of vertex counts for each graph. Es.: [10, 50, 100, 500, 1000]
        max_coords_list (list): List of maximum coordinate values. Es.: [10, 100, 1000]
        function (function): Function to generate the graph. Es.: tsp_utils.randomEuclGraph
        num_instances (int): Number of instances for each combination. Es.: 20
        output_dir (str): Main directory where the graphs will be saved. Es.: 'data/euclidean'
    """
    # Numero totale di file da generare (300 in questo caso)
    total_files = len(num_vertices_list) * len(max_coords_list) * num_instances

    # Inizializza la barra di caricamento
    with tqdm(total=total_files, desc="Generating benchmark datasets") as pbar:
        for num_vertices in num_vertices_list: # For each number of vertices
                for max_coord in max_coords_list:  # For each maximum coordinate value     --> this create all the possible combinations
                    
                    # Create the directory for the number of vertices and max_coord
                    dir_path = os.path.join(output_dir, f"NumVertices_{num_vertices}", f"MaxVal_{max_coord}")
                    os.makedirs(dir_path, exist_ok=True) # Create the directory if it does not exist
                    

                    with tqdm(total=num_instances, desc=f"Generating instances for {num_vertices} vertices and {max_coord} max coord", leave=False) as instance_bar:
                        for instance_num in (range(1, num_instances + 1)):

                            # Generate a random graph
                            points, dist = function(num_vertices, max_coord)
                            
                            file_path = os.path.join(dir_path, f"instance_{instance_num}.csv")
                            
                            with open(file_path, mode='w', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(["x", "y"])  # intestazioni per le colonne delle coordinate
                                for point in points:                       
                                    writer.writerow(point[0])
                                
                                writer.writerow([])  # riga vuota per separare le sezioni
                                writer.writerow(["Distanze"])  # intestazione per la sezione delle distanze
                                
                                # Scrivi le distanze nel formato desiderato
                                for (i, j), distance in dist.items():
                                    writer.writerow([f"{i},{j} : {distance}"]) 
                            # print(f"Saved graph instance {instance_num} in {file_path}")
                            instance_bar.update(1)
                            pbar.update(1)


def load_graph_data(file_path):
    """
    Carica i dati del grafo da un file CSV e restituisce le coordinate dei punti e le distanze.

    Args:
        file_path (str): Il percorso del file CSV da cui caricare i dati.

    Returns:
        points (list): Lista delle coordinate dei punti.
        dist (dict): Dizionario delle distanze tra i punti.
    """
    points = []
    dist = {}

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        reading_distances = False  # Flag per sapere quando iniziare a leggere le distanze
        
        for row in reader:
            if len(row) == 0:
                continue  # Salta le righe vuote

            # Controlla se siamo nella sezione delle coordinate
            if row[0] == "x":
                continue  # Salta l'intestazione delle coordinate
            
            # Seleziona i punti
            if not reading_distances:
                # Controlla se abbiamo raggiunto la sezione delle distanze
                if row[0] == "Distanze":
                    reading_distances = True
                    continue
                
                # Aggiungi il punto alla lista delle coordinate
                points.append(((float(row[0]), float(row[1])), False))  # Aggiungi la tupla (x, y)
            else:
                # Leggi le distanze
                # La riga avrà la forma "i,j : distanza"
                key_value = row[0].split(" : ")
                if len(key_value) == 2:
                    key = tuple(map(int, key_value[0].split(",")))  # Converti la chiave in tupla (i, j)
                    value = float(key_value[1])  # Distanza come float
                    dist[key] = value

    return points, dist

def clean_directory(dir_path):
    """
    Empties the specified directory.

    Parameters:
    dir_path (str): The path of the directory to empty.

    Returns:
    None
    """
    # Controlla se la directory esiste
    if os.path.exists(dir_path):
        # Itera attraverso tutti i file e le sottodirectory nella directory
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                # Se è un file, lo rimuove
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                # Se è una directory, la rimuove ricorsivamente
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Error removing {file_path}: {e}')
    else:
        print(f"The directory {dir_path} does not exist.")
if __name__ == "__main__":
    clean_directory('./data')
    generate_all_benchmark()