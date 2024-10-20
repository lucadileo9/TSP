from my_utils import *
from algorithm_metrics import *
from tsp_utils import *
from dataset_generator import *


import matplotlib.pyplot as plt

# Lista delle coordinate (x, y) dei punti del grafo
coordinates, distances = load_graph_data("./data/euclidean/NumVertices_100/MaxVal_50/instance_1.csv")
#coordinates, distances = randomGraph2D(10, 0.5)


# Funzione per disegnare il grafo e mostrare le distanze tra i punti
def plot_graph_with_distances(coordinates, distances):
    coordinates = [coordinates for coordinates, _ in coordinates]

    # Estrazione delle coordinate x e y
    x_vals, y_vals = zip(*coordinates)  # Separiamo x e y per disegnare i punti
    plt.scatter(x_vals, y_vals, color='blue')  # Disegna i punti sul grafico
    
    # Annotazione dei punti sul grafico
    for i, (x, y) in enumerate(coordinates):
        plt.text(x, y, f'{i}', fontsize=12, ha='right')  # Mostra l'indice di ogni punto vicino al punto stesso

    # Aggiunta delle linee e delle etichette delle distanze tra i punti connessi
    for (i, j), dist in distances.items():
        x1, y1 = coordinates[i]  # Coordinate del primo punto
        x2, y2 = coordinates[j]  # Coordinate del secondo punto

        # Disegna una linea grigia tratteggiata tra i due punti connessi
        plt.plot([x1, x2], [y1, y2], color='gray', linestyle='--', linewidth=1)

        # Calcola il punto medio tra i due punti per posizionare l'etichetta della distanza
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2

        # Mostra la distanza tra i punti come etichetta in rosso e riduce la dimensione del testo a 8
        plt.text(mid_x, mid_y, f'{dist}', fontsize=8, color='red', ha='center')

    # Etichette degli assi e titolo del grafico
    plt.xlabel('X Coordinate')  # Etichetta asse X
    plt.ylabel('Y Coordinate')  # Etichetta asse Y
    plt.title('Graph with Distances')  # Titolo del grafico

    # Mostra una griglia di sfondo per facilitare la lettura del grafico
    plt.grid(True)

    # Visualizza il grafico finale
    plt.show()

# Esegui la funzione per visualizzare il grafo e le distanze
# run_tests = True
# points, dist = coordinates, distances
# path = nearest_neighbor_first(points, dist, debug=False)
# print_in_square("Path", path)

# if run_tests:
#     if check_path(points, path):
#         print("Brute force is correct")
#     else:
#         print("Brute force is not correct")

#     path_length(dist, path, print_length=True)
#     reset_points(points)
#     research_path_time(points, dist, nearest_neighbor_first, print_time=True)
    #average_research_path_time(points, dist, nearest_neighbor_first, num_runs=1000)

plot_graph_with_distances(coordinates, distances)

# n= 10
# maxcoord = 100
# use_existing = False
# run_tests = True
# data_debug = False

# points, dist = get_or_create_graph_data(n, maxcoord, function=randomGraphGeo, use_existing=use_existing, debug=data_debug)

# path = nearest_neighbor_first(points, dist)
# print_in_square("Brute force", path)

# if run_tests:
#     if check_path(points, path):
#         print("Brute force is correct")
#     else:
#         print("Brute force is not correct")

#     path_length(dist, path, print_length=True)
#     reset_points(points)
#     research_path_time(points, dist, nearest_neighbor_first, print_time=True)
#     average_research_path_time(points, dist, nearest_neighbor_first, num_runs=1000)
