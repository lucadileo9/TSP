import matplotlib.pyplot as plt
from benchmark_runner import *  

def get_all_execution_time(results):
    all_execution_time = []
    
    # Itera attraverso tutte le chiavi e i valori del dizionario
    for key, values in results.items():
        # Estrai la distanza dal primo elemento di ogni tupla nella lista associata alla chiave
        for path_distance, execution_time, avg_execution_time in values:
            all_execution_time.append(execution_time)
    
    return all_execution_time

def get_all_distances(results):
    all_distances = []
    
    # Itera attraverso tutte le chiavi e i valori del dizionario
    for key, values in results.items():
        # Estrai la distanza dal primo elemento di ogni tupla nella lista associata alla chiave
        for path_distance, execution_time, avg_execution_time in values:
            all_distances.append(path_distance)
    
    return all_distances

def get_all_avg_execution_time(results):
    all_avg_execution_time = []
    
    # Itera attraverso tutte le chiavi e i valori del dizionario
    for key, values in results.items():
        # Estrai la distanza dal primo elemento di ogni tupla nella lista associata alla chiave
        for path_distance, execution_time, avg_execution_time in values:
            all_avg_execution_time.append(avg_execution_time)
    
    return all_avg_execution_time

results_A = load_results("nearest_neighbor_random_euclidean_results.json")
results_B = load_results("nearest_neighbor_second_euclidean_results.json")

tempi_algoritmo_A = get_all_execution_time(results_A)
tempi_algoritmo_B = get_all_execution_time(results_B)

tempi_medi_A = get_all_avg_execution_time(results_A)  
tempi_medi_B = get_all_avg_execution_time(results_B)

distanze_algoritmo_A = get_all_distances(results_A)
distanze_algoritmo_B = get_all_distances(results_B)

plt.plot(range(1, 301), tempi_algoritmo_A, label='Algoritmo A')
plt.plot(range(1, 301), tempi_algoritmo_B, label='Algoritmo B')
plt.xlabel('Istanza')
plt.ylabel('Tempo (s)')
plt.legend()
plt.show()

input()


plt.boxplot([tempi_algoritmo_A, tempi_algoritmo_B], labels=['Algoritmo A', 'Algoritmo B'])
plt.ylabel('Tempo (s)')
plt.show()

#__________________________
plt.scatter(range(1, 301), tempi_medi_A, label='Algoritmo A')
plt.scatter(range(1, 301), tempi_medi_B, label='Algoritmo B')
plt.xlabel('Istanza')
plt.ylabel('Tempo Medio (s)')
plt.show()


#__________________________
import numpy as np
ind = np.arange(300)  # 300 istanze
width = 0.35  # Larghezza delle barre

plt.bar(ind, distanze_algoritmo_A, width, label='Algoritmo A')
plt.bar(ind + width, distanze_algoritmo_B, width, label='Algoritmo B')
plt.xlabel('Istanza')
plt.ylabel('Distanza')
plt.legend()
plt.show()

plt.boxplot([distanze_algoritmo_A, distanze_algoritmo_B], labels=['Algoritmo A', 'Algoritmo B'])
plt.ylabel('Distanza')
plt.show()