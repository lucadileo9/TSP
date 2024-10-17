
import os
from tqdm import tqdm
from my_utils import *
from algorithm_metrics import *
from tsp_utils import *
from dataset_generator import *

# Allora adesso ho salvato tutti i grafi in file csv che faranno parte del mio benchmarks. Adesso ho bisogno di chiamare il mio algoritmo nearest_neighbor_first su ogni istanza. E in seguito ottenere i dati statistici dell'algoritmo.
num_vertices_list= [10, 50, 100, 500, 1000]
max_coords_list = [50, 100, 1000]
num_instances = 20
input_dir = "./data/euclidean"

total_files = len(num_vertices_list) * len(max_coords_list) * num_instances


with tqdm(total=total_files, desc="Something") as pbar:
        for num_vertices in num_vertices_list: # For each number of vertices
                for max_coord in max_coords_list:  # For each maximum coordinate value     --> this create all the possible combinations
                    
                    # Create the directory for the number of vertices and max_coord
                    instance_path = os.path.join(input_dir, f"NumVertices_{num_vertices}", f"MaxVal_{max_coord}")

                    with tqdm(total=num_instances, desc=f"Generating instances for {num_vertices} vertices and {max_coord} max coord", leave=False) as instance_bar:
                        results = {}

                        for instance_num in (range(1, num_instances + 1)):

                            # Generate a random graph
                            points, dist = load_graph_data(instance_path)
                            path= nearest_neighbor_first(points, dist) # oppure la funzione passata come parametro 
                            path_distance = path_length(dist, path)
                            execution_time = research_path_time(points, dist, nearest_neighbor_first)
                            average_execution_time = average_research_path_time(points, dist, nearest_neighbor_first, num_runs=1000)
                            
                # La struttura dati per memorizzare queste info sarà fatta così:
                # dizionario chaive = coppia (num_vertices, max_coord) e valore = lista di tuple (path_distance, execution_time, average_execution_time)
                # Ci sarà un dizionario per ogni algoritmo
                # Visivamente:
                # results = {
                #             (num_vertices, max_coord): [
                #                 (path_distance_1, execution_time_1, average_execution_time_1),
                #                 (path_distance_2, execution_time_2, average_execution_time_2),
                #                 ...
                #             ],
                #             ...
                #         }
                # results = {
                #             (10, 10): [
                #                 (123.4, 0.0012, 0.0011),  # Prima istanza per 10 vertici, max coord 10
                #                 (134.6, 0.0014, 0.0012)   # Seconda istanza per 10 vertici, max coord 10
                #             ],
                #             (10, 100): [
                #                 (543.7, 0.0023, 0.0020),  # Prima istanza per 10 vertici, max coord 100
                #                 (567.1, 0.0025, 0.0021)   # Seconda istanza per 10 vertici, max coord 100
                #             ],
                #             (50, 10): [
                #                 (1523.6, 0.0121, 0.0117), # Prima istanza per 50 vertici, max coord 10
                #                 (1601.3, 0.0128, 0.0119)  # Seconda istanza per 50 vertici, max coord 10
                #             ],
                #             (50, 1000): [
                #                 (6543.2, 0.0456, 0.0440), # Prima istanza per 50 vertici, max coord 1000
                #                 (6600.1, 0.0462, 0.0445)  # Seconda istanza per 50 vertici, max coord 1000
                #             ]
                #         }