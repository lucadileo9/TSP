from my_utils import *
from tester import *
from tsp_utils import *
from benchmark import *

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
                        for instance_num in (range(1, num_instances + 1)):

                            # Generate a random graph
                            points, dist = load_graph_data(instance_path)
                            