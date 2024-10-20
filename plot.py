import matplotlib.pyplot as plt
from benchmark_runner import *  


import matplotlib.pyplot as plt
import numpy as np


import matplotlib.pyplot as plt
import numpy as np

# Dati di esempio (results)
results = {
    (10, 50): [(12, "info1", "info2"), (14, "info3", "info4")],
    (50, 100): [(50, "info1", "info2"), (53, "info3", "info4")],
    (100, 50): [(120, "info1", "info2"), (140, "info3", "info4")],
    (500, 1000): [(600, "info1", "info2"), (640, "info3", "info4")]
}
results = load_results("nearest_neighbor_random_euclidean_results.json")
# Imposto il numero di grafici da disporre in una griglia (es. 2x2)
n_graphs = len(results)
cols = 5  # Numero di colonne
rows = (n_graphs // cols) + (n_graphs % cols > 0)  # Numero di righe

fig, axs = plt.subplots(rows, cols, figsize=(12, 8))

# Flatten degli assi per poterli usare in un ciclo
axs = axs.ravel()

# Iteriamo su ciascuna combinazione di numero di vertici e massimo numero di coordinate
for i, ((num_vertices, max_coord), distances_info) in enumerate(results.items()):
    distances = [info[0] for info in distances_info]
    instances = [f'Instance {i+1}' for i in range(len(distances))]
    
    # Creiamo un'etichetta per ogni coppia (num_vertices, max_coord)
    label = f'Vertices: {num_vertices}, Max Coord: {max_coord}'
    
    # Creiamo il grafico a barre per la specifica combinazione
    axs[i].bar(np.arange(len(distances)), distances, color=plt.cm.tab10(i))
    axs[i].set_xticks(np.arange(len(distances)))
    axs[i].set_xticklabels(instances)
    axs[i].set_title(label)
    axs[i].set_ylabel('Path Distance')
    axs[i].set_xlabel('Instances')

# Rimozione dei subplot vuoti, se il numero di grafici è dispari
if n_graphs % cols != 0:
    for j in range(n_graphs, rows * cols):
        fig.delaxes(axs[j])

# Aggiustiamo il layout per una migliore visualizzazione
plt.tight_layout()
plt.show()

#______________________
# Dati di esempio (results)
results = {
    (10, 50): [(12, "info1", "info2"), (14, "info3", "info4")],
    (50, 100): [(50, "info1", "info2"), (53, "info3", "info4")],
    (100, 50): [(120, "info1", "info2"), (140, "info3", "info4")],
    (500, 1000): [(600, "info1", "info2"), (640, "info3", "info4")]
}
results = load_results("nearest_neighbor_random_euclidean_results.json")
# Creiamo il grafico
fig, ax = plt.subplots(figsize=(10, 6))

# Creiamo una lista per le etichette e per i valori delle distanze
labels = []
path_distances = []
colors = []  # Aggiungo colori per distinguere visivamente le diverse combinazioni

# Iteriamo su ciascuna combinazione di numero di vertici e massimo numero di coordinate
for (num_vertices, max_coord), distances_info in results.items():
    # Estraggo le distanze dei percorsi
    distances = [info[0] for info in distances_info]
    
    # Creiamo un'etichetta per ogni coppia (num_vertices, max_coord)
    label = f'Vertices: {num_vertices}, Max Coord: {max_coord}'
    
    # Aggiungiamo i dati al nostro grafico
    for i, distance in enumerate(distances):
       # labels.append(f"{label} - Instance {i+1}")
        path_distances.append(distance)
        # Aggiungiamo un colore unico per ogni coppia (num_vertices, max_coord)
        colors.append((num_vertices + max_coord) % 10)  # Giusto per diversificare i colori

# Posizioni delle barre
x_pos = np.arange(len(path_distances))

# Creiamo il grafico a barre
ax.bar(x_pos, path_distances, color=plt.cm.tab10(colors))

# Etichette e titolo
ax.set_xlabel('Graph Instances')
ax.set_ylabel('Path Distance')
ax.set_title('Path Distance per Instance for Different Graph Configurations')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation=90, ha='right')

# Mostra il grafico
plt.tight_layout()
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