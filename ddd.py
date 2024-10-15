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
#     - geometric
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
import json, csv
import tsp_utils 

def generate_benchmark(num_vertices_list, max_coords_list, num_instances, output_dir):
    """
    Generates random Euclidean graphs and saves them in structured folders.

    Args:
        num_vertices_list (list): List of vertex counts for each graph. Es.: [10, 50, 100, 500, 1000]
        max_coords_list (list): List of maximum coordinate values. Es.: [10, 100, 1000]
        num_instances (int): Number of instances for each combination. Es.: 20
        output_dir (str): Main directory where the graphs will be saved. Es.: 'data/euclidean'
    """
    
    for num_vertices in num_vertices_list: # For each number of vertices
        for max_coord in max_coords_list:  # For each maximum coordinate value     --> this create all the possible combinations
            
            # Create the directory for the number of vertices and max_coord
            dir_path = os.path.join(output_dir, f"NumVertices_{num_vertices}", f"MaxValCoord_{max_coord}")
            os.makedirs(dir_path, exist_ok=True) # Create the directory if it does not exist
            
            for instance_num in range(1, num_instances + 1): # For each instance
                # Generate a random Euclidean graph
                points, dist = tsp_utils.randomEuclGraph(num_vertices, max_coord)
                
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
                print(f"Saved graph instance {instance_num} in {file_path}")


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
