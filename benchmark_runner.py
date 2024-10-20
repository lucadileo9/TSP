import os, json
from tqdm import tqdm
from my_utils import nearest_neighbor_second as nearest_neighbor
from my_utils import nearest_neighbor_random
from algorithm_metrics import *
from tsp_utils import *
from dataset_generator import *

def save_results(results, output_file):
    """
    Salva il dizionario dei risultati in un file JSON.
    
    Parametri:
    - results (dict): Dizionario con i risultati da salvare.
    - output_file (str): Percorso del file JSON dove salvare i risultati.
    """
    # Converti il dizionario in un formato serializzabile
    serializable_results = {str(key): value for key, value in results.items()}
    
    with open(output_file, 'w') as f:
        json.dump(serializable_results, f, indent=4)



def print_results(results):
    """
    Stampa in maniera chiara e leggibile i risultati contenuti nel dizionario.
    Il dizionario ha chiavi come tuple (num_vertices, max_coord) e valori come liste di tuple
    (path_distance, execution_time, average_execution_time).
    
    Parametri:
    results (dict): Dizionario che contiene i risultati delle istanze TSP.
    """
    for key, values in results.items():
        num_vertices, max_coord = key
        print(f"Numero Vertici: {num_vertices}, Max Coordinata: {max_coord}")
        print("--------------------------------------------------------")
        print(f"{'Path Distance':<20} {'Execution Time (s)':<20} {'Avg Execution Time (s)':<25}")
        print("-" * 65)
        
        for path_distance, execution_time, avg_execution_time in values:
            print(f"{path_distance:<20.5f} {execution_time:} {avg_execution_time:}")
        
        print("\n")  # Stampa una riga vuota tra le diverse combinazioni

def insert_result(results, num_vertices, max_coord, path_distance, execution_time, average_execution_time):
    """
    Inserts the results of a TSP benchmark into the results dictionary.
    Parameters:
    results (dict): The dictionary to store the results. The keys are tuples of (num_vertices, max_coord),
                    and the values are lists of tuples containing (path_distance, execution_time, average_execution_time).
    num_vertices (int): The number of vertices in the TSP instance.     -->  These are the
    max_coord (int): The maximum coordinate value for the vertices.     -->  keys of the dictionary
    path_distance (float): The total distance of the path found.
    execution_time (float): The time taken to find the path.
    average_execution_time (float): The average time taken over multiple runs to find the path.
    Returns:
    None
    """
    key = (num_vertices, max_coord)
    
    # Crea una nuova lista se la chiave non esiste
    if key not in results:
        results[key] = []
    
    # Aggiungi i nuovi risultati alla lista
    results[key].append((path_distance, execution_time, average_execution_time))

def generate_statistics(num_vertices_list, max_coords_list, num_instances, input_dir, function):
    """
    Generates statistics for the Traveling Salesman Problem (TSP) benchmark.
    This function iterates over combinations of vertex counts and maximum coordinate values,
    runs a specified TSP algorithm on generated instances, and collects performance metrics.
    Args:
        num_vertices_list (list of int): List of different numbers of vertices to test.
        max_coords_list (list of int): List of different maximum coordinate values to test.
        num_instances (int): Number of instances to generate for each combination of vertices and coordinates.
        input_dir (str): Directory where the input instances are stored.
        function (callable): The TSP algorithm function to be tested. It should take points and distance matrix as input and return a path.
    Returns:
        dict: A dictionary containing the results of the benchmarks, including path distances, execution times, and average execution times.
        results = {
                                (num_vertices, max_coord): [
                                    (path_distance_1, execution_time_1, average_execution_time_1),
                                    (path_distance_2, execution_time_2, average_execution_time_2),
                                    ...
                                ],
                                ...
                    }
        """
    
    total_files = len(num_vertices_list) * len(max_coords_list) * num_instances
    results = {}
    with tqdm(total=total_files, desc=f"Esecuzione benchmark of {function.__name__} on {input_dir.split("/")[1]}") as pbar:
            for num_vertices in num_vertices_list: # For each number of vertices
                    for max_coord in max_coords_list:  # For each maximum coordinate value     --> this create all the possible combinations
                        
                        with tqdm(total=num_instances, desc=f"Vertici: {num_vertices}, Max Coord: {max_coord}", leave=False) as instance_bar:
                            for instance_num in (range(1, num_instances + 1)):
                                # Create the path of the file
                                instance_path = os.path.join(input_dir, f"NumVertices_{num_vertices}", f"MaxVal_{max_coord}", f"instance_{instance_num}.csv")
                                # Load the graph graph
                                points, dist = load_graph_data(instance_path) # Try catch ?????????????
                                # Run the algorithm
                                path= function(points, dist) # oppure la funzione passata come parametro 
                                # Compute the metrics
                                path_distance = path_length(dist, path)
                                reset_points(points)
                                execution_time = research_path_time(points, dist, function)
                                reset_points(points)
                                if num_vertices < 500:
                                    average_execution_time = average_research_path_time(points, dist, function, num_runs=100)
                                else:
                                    average_execution_time = average_research_path_time_parallel(points, dist, function, num_runs=100)
                                insert_result(results, num_vertices, max_coord, path_distance, execution_time, average_execution_time)
                                
                                instance_bar.update(1)
                                pbar.update(1)  
            save_results(results, f"{function.__name__}_{input_dir.split("/")[1]}_results.json")   
            return results
            
def generate_all_statistics():
    """
    Generates and prints statistics for various TSP instances using different algorithms.
    This function iterates over a list of TSP solving functions and input directories,
    generating statistics for each combination of number of vertices, maximum coordinates,
    and number of instances. The results are then printed.
    Parameters:
    None
    Returns:
    None
    Non c'è bisogno di salvare nulla, perché i dizionario di ogni algoritmo vengono salvati automaticamente in memoria
    """
    
    num_vertices_list= [10, 50, 100, 500, 1000]
    max_coords_list = [50, 100, 1000]
    num_instances = 20
    input_dir = ["data/euclidean"]
    functions = [nearest_neighbor, nearest_neighbor_random]
    for function in functions:
        for dir in input_dir:
            generate_statistics(num_vertices_list, max_coords_list, num_instances, dir, function)
    

def load_results(file_path):
    """
    Carica i risultati del benchmark da un file JSON.
    
    Parametri:
    - file_path (str): Percorso del file JSON da cui caricare i risultati.
    
    Returns:
    - dict: Dizionario con i risultati del benchmark.
    """
    with open(file_path, 'r') as f:
        serializable_results = json.load(f)
    
    # Converti le chiavi in tuple di interi
    results = {eval(key): value for key, value in serializable_results.items()}
    
    return results



if __name__ == "__main__":
    generate_all_statistics()
    # print("Dizionario dell'algoritmo nearest_neighbor")
    # print_results(results[0])
    # print("Dizionario dell'algoritmo nearest_neighbor_random")
    # print_results(results[1])


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
                