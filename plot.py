import matplotlib.pyplot as plt
from benchmark_runner import *  
import numpy as np
from enum import Enum

class DataType(Enum):
    """
    DataType(Enum):
        An enumeration to represent different types of data metrics for TSP (Traveling Salesman Problem) instances.
        Attributes:
            DISTANCE (tuple): Represents the distance metric with a unique identifier, a name, and a title.
            TIME (tuple): Represents the execution time metric with a unique identifier, a name, and a title.
            AVG_TIME (tuple): Represents the average execution time metric with a unique identifier, a name, and a title.
        Methods:
            get_number():
                Returns the unique identifier of the data type.
            get_name():
                Returns the name of the data type.
            get_title():
                Returns the title of the data type.
    """
    DISTANCE = (0,'Distance', 'Path Distance per Instance')
    TIME = (1, "Execution Time", 'Execution Time per Instance')
    AVG_TIME = (2, "Average Execution Time", 'Average Execution Time per Instance')

    def get_number(self):
        return self.value[0]
    def get_name(self):
        return self.value[1]
    def get_title(self):
        return self.value[2]

def plot_chart(ax, results, datum, cmap):
        """
        Plots a bar chart based on the provided results.
        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to plot the chart.
        results (dict): A dictionary where keys are tuples of (num_vertices, max_coord) and values are lists of dictionaries containing data.
        datum (str): The key in the dictionaries within `results` to extract the data to be plotted. (e.g., 'distance', 'time', 'avg_time')
        cmap (matplotlib.colors.Colormap): The colormap to use for coloring the bars.
        The function will create a bar chart where each bar represents a distance value from the `results` dictionary.
        The bars are colored based on the (num_vertices, max_coord) configuration using the provided colormap.
        A legend is added to the plot to indicate which color corresponds to which (num_vertices, max_coord) configuration.
        """
        labels = []
        path_distances = []
        colors = []
        color_map = {}
        color_index = 0
        
        for (num_vertices, max_coord), infos in results.items():
            distances = [info[datum] for info in infos]
            if (num_vertices, max_coord) not in color_map:
                color_map[(num_vertices, max_coord)] = cmap(color_index % cmap.N)
                color_index += 1

            for i, distance in enumerate(distances):
                labels.append(f"{len(labels) + 1}")
                path_distances.append(distance)
                colors.append(color_map[(num_vertices, max_coord)])

        x_pos = np.arange(len(path_distances))
        ax.bar(x_pos, path_distances, color=colors)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels, rotation=90, ha='right')

        handles = [plt.Rectangle((0, 0), 1, 1, color=color_map[key]) for key in color_map]
        labels_legend = [f'Vertices: {k[0]}, Max Coord: {k[1]}' for k in color_map]
        ax.legend(handles, labels_legend, title="Graph Configurations", bbox_to_anchor=(1.05, 1), loc='upper left')

def plot_two_bar_charts(file_name_1, file_name_2, data_type: DataType):
    """
    Plots two bar charts side by side for comparison.
    Parameters:
    file_name_1 (str): The name of the first file containing the results to plot.
    file_name_2 (str): The name of the second file containing the results to plot.
    data_type (DataType): An instance of DataType that provides methods to get the data to plot.
    The function loads results from the given files, extracts the necessary data using the provided
    DataType instance, and plots two bar charts side by side for visual comparison. Each chart is 
    labeled with the file name and the data type title.
    """

    results_1 = load_results(file_name_1)
    results_2 = load_results(file_name_2)

    # Creiamo i grafici con una griglia 1x2
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))  # Due grafici affiancati
    cmap = plt.colormaps['tab20']  # Mappa di colori    
    
    # Dato da plottare
    datum = data_type.get_number()

    # Plot primo grafico
    plot_chart(axes[0], results_1, datum, cmap)
    axes[0].set_title(f'{file_name_1} - {data_type.get_title()}')
    axes[0].set_xlabel('Instance Number')
    axes[0].set_ylabel(data_type.get_name())

    # Plot secondo grafico
    plot_chart(axes[1], results_2, datum, cmap)
    axes[1].set_title(f'{file_name_2} - {data_type.get_title()}')
    axes[1].set_xlabel('Instance Number')

    # Mostra i grafici affiancati
    plt.tight_layout()
    plt.show()



def plot_bar_chart(file_name, data_type: DataType):
        
    results= load_results(file_name)
    # Creiamo il grafico
    fig, ax = plt.subplots(figsize=(15, 6))
    # Liste per le etichette e per i valori delle distanze
    labels = []
    path_distances = []
    colors = []  # Una lista per assegnare un colore diverso per ciascuna combinazione
    color_map = {}  # Un dizionario per assegnare un colore unico a ciascuna combinazione

    # Uso una mappa di colori più ampia come 'tab20' per più variazioni di colore
    cmap = plt.colormaps['tab20']

    # Iniziamo con un indice per assegnare i colori
    color_index = 0

    datum = data_type.get_number()
    # Iteriamo su ciascuna combinazione di numero di vertici e massimo numero di coordinate
    for (num_vertices, max_coord), infos in results.items():
        # Estraggo le distanze dei percorsi
        distances = [info[datum] for info in infos]
        
        # Se la combinazione non ha ancora un colore assegnato, ne assegniamo uno nuovo dalla mappa
        if (num_vertices, max_coord) not in color_map:
            color_map[(num_vertices, max_coord)] = cmap(color_index % cmap.N)
            color_index += 1

        # Aggiungiamo i dati al grafico
        for i, distance in enumerate(distances):
            labels.append(f"{len(labels) + 1}")  # Etichetta con il numero progressivo dell'istanza
            path_distances.append(distance)
            colors.append(color_map[(num_vertices, max_coord)])  # Usa il colore corrispondente

    # Posizioni delle barre
    x_pos = np.arange(len(path_distances))

    # Creiamo il grafico a barre con colori distinti per ogni combinazione
    ax.bar(x_pos, path_distances, color=colors)

    # Etichette e titolo
    ax.set_xlabel('Instance Number')
    ax.set_ylabel(data_type.get_name())
    ax.set_title(data_type.get_title())
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=90, ha='right')


    # Aggiungiamo una legenda che mostra le combinazioni di numero di vertici e massime coordinate
    handles = [plt.Rectangle((0,0),1,1, color=color_map[key]) for key in color_map]
    labels_legend = [f'Vertices: {k[0]}, Max Coord: {k[1]}' for k in color_map]
    ax.legend(handles, labels_legend, title="Graph Configurations", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Mostra il grafico
    plt.tight_layout()
    plt.show()



def plot_graph_with_distances(coordinates, distances):
    """
    Plots a graph with given coordinates and distances between points.
    Args:
        coordinates (list of tuples): A list of tuples where each tuple contains the x and y coordinates of a point.
        distances (dict): A dictionary where keys are tuples of point indices (i, j) and values are the distances between those points.
    The function performs the following steps:
        1. Extracts x and y coordinates from the input list.
        2. Plots the points on a scatter plot.
        3. Annotates each point with its index.
        4. Draws dashed lines between connected points and labels the lines with the distances.
        5. Adds axis labels and a title to the plot.
        6. Displays a grid for better readability.
        7. Shows the final plot.
    Note:
        The function uses matplotlib for plotting and assumes it is already imported as plt.
    """
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


# def plot_boxplot_tempi(results, num_vertices_list, max_coords_list):
#     fig, axes = plt.subplots(len(num_vertices_list), len(max_coords_list), figsize=(15, 10), sharey=True)

#     for i, num_vertices in enumerate(num_vertices_list):
#         for j, max_coords in enumerate(max_coords_list):
#             istanze = results[(num_vertices, max_coords)]
#             tempi_A = [x[1] for x in istanze]  # Tempo di esecuzione Algoritmo A
#             tempi_B = [x[1] for x in istanze]  # Tempo di esecuzione Algoritmo B
            
#             ax = axes[i, j]
            
#             ax.boxplot([tempi_A, tempi_B], labels=['Algoritmo A', 'Algoritmo B'])
#             ax.set_title(f'Vertici: {num_vertices}, Max Coord: {max_coords}')
#             ax.set_ylabel('Tempo (s)')
#             ax.set_yscale('log')  # Scala logaritmica sull'asse Y


#     plt.tight_layout()
#     plt.show()

# def get_all_execution_time(results):
#     all_execution_time = []
    
#     # Itera attraverso tutte le chiavi e i valori del dizionario
#     for key, values in results.items():
#         # Estrai la distanza dal primo elemento di ogni tupla nella lista associata alla chiave
#         for path_distance, execution_time, avg_execution_time in values:
#             all_execution_time.append(execution_time)
    
#     return all_execution_time

# def get_all_distances(results):
#     all_distances = []
    
#     # Itera attraverso tutte le chiavi e i valori del dizionario
#     for key, values in results.items():
#         # Estrai la distanza dal primo elemento di ogni tupla nella lista associata alla chiave
#         for path_distance, execution_time, avg_execution_time in values:
#             all_distances.append(path_distance)
    
#     return all_distances

# def get_all_avg_execution_time(results):
#     all_avg_execution_time = []
    
#     # Itera attraverso tutte le chiavi e i valori del dizionario
#     for key, values in results.items():
#         # Estrai la distanza dal primo elemento di ogni tupla nella lista associata alla chiave
#         for path_distance, execution_time, avg_execution_time in values:
#             all_avg_execution_time.append(avg_execution_time)
    
#     return all_avg_execution_time

# results_A = load_results("nearest_neighbor_random_euclidean_results.json")
# results_B = load_results("nearest_neighbor_second_euclidean_results.json")


# #plot_boxplot_tempi(results_A, [10, 50, 100, 500, 1000],  [50, 100, 1000])
# input()
# tempi_algoritmo_A = get_all_execution_time(results_A)
# tempi_algoritmo_B = get_all_execution_time(results_B)

# tempi_medi_A = get_all_avg_execution_time(results_A)  
# tempi_medi_B = get_all_avg_execution_time(results_B)

# distanze_algoritmo_A = get_all_distances(results_A)
# distanze_algoritmo_B = get_all_distances(results_B)

# plt.plot(range(1, 301), tempi_algoritmo_A, label='Algoritmo A')
# plt.plot(range(1, 301), tempi_algoritmo_B, label='Algoritmo B')
# plt.xlabel('Istanza')
# plt.ylabel('Tempo (s)')
# plt.yscale('log')
# plt.legend()
# plt.show()


# import numpy as np

# # Definisci la larghezza delle barre
# width = 0.35

# # Definisci la posizione delle barre (una per ogni istanza)
# x = np.arange(1, 301)

# # Grafico a barre
# plt.bar(x - width/2, tempi_algoritmo_A, width=width, label='Algoritmo A', color='blue')
# plt.bar(x + width/2, tempi_algoritmo_B, width=width, label='Algoritmo B', color='green')

# # Etichette e scala logaritmica
# plt.xlabel('Istanza')
# plt.ylabel('Tempo (s)')
# plt.yscale('log')  # Scala logaritmica per visualizzare bene i tempi piccoli e grandi

# # Aggiungi la legenda
# plt.legend()

# # Mostra il grafico
# plt.show()

# # plt.boxplot([tempi_algoritmo_A, tempi_algoritmo_B], labels=['Algoritmo A', 'Algoritmo B'])
# # plt.ylabel('Tempo (s)')
# # plt.show()

# #__________________________
# plt.scatter(range(1, 301), tempi_algoritmo_A, label='Algoritmo A')
# plt.scatter(range(1, 301), tempi_medi_B, label='Algoritmo B')
# plt.xlabel('Istanza')
# plt.ylabel('Tempo Medio (s)')
# plt.yscale('log')
# plt.show()


# #__________________________
# import numpy as np
# ind = np.arange(300)  # 300 istanze
# width = 0.35  # Larghezza delle barre

# plt.bar(ind, distanze_algoritmo_A, width, label='Algoritmo A')
# plt.bar(ind + width, distanze_algoritmo_B, width, label='Algoritmo B')
# plt.xlabel('Istanza')
# plt.ylabel('Distanza')
# plt.legend()
# plt.show()

# plt.boxplot([distanze_algoritmo_A, distanze_algoritmo_B], labels=['Algoritmo A', 'Algoritmo B'])
# plt.ylabel('Distanza')
# plt.show()


if __name__ == "__main__":
    plot_two_bar_charts("random_euclidean_results.json", "first_euclidean_results.json", DataType.DISTANCE)
    plot_two_bar_charts("random_euclidean_results.json", "first_euclidean_results.json", DataType.TIME)
    plot_two_bar_charts("random_euclidean_results.json", "first_euclidean_results.json", DataType.AVG_TIME)