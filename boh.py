# Traveling Salesman Problem (TSP): Dato un grafo G = (V, E) pesato sui lati, trovare il circuito hamiltoniano di peso minimo.
# Quel che devo fare è: (trovate le istanze)
# 1) Inizializzazione: Partire da un nodo casuale nel grafo.
# 2) Costruire il percorso: Ad ogni iterazione, scegli il prossimo nodo da visitare (tra i 𝑘 nodi più vicini, ordinati secondo una regola greedy come la distanza minima).
# 3) Randomizzazione: Tra questi 𝑘 selezioniare casualmente il prossimo nodo da visitare, così da introdurre indecisione.
# Non eseguire questo passo poterebbere ad un algoritmo deterministico
# 4) Continuazione: Ripetere il processo fino a coprire tutti i nodi. 
# 5) Chiudre il circuito ritornando al nodo di partenza.

def next_node(node, dist):
    # Prendo tutti i nodi connessi al nodo corrente, con relative distanze
    filtered_distances = {key: value for key, value in dist.items() if node in key}
    # stampa del dizionario
    # for key, value in filtered_distances.items():
    #     print(f"Chiave: {key}, Valore: {value}")
    # print("\n")

    sorted_distances = sorted(filtered_distances.items(), key=lambda x: x[1])
    # stampa della lista ordinata
    # for item in sorted_distances:
    #     print(f"Chiave: {item[0]}, Valore: {item[1]}")
    return sorted_distances[0]
        
def elaborete_dist(dist):
    '''
    Funzione che elabora il dizionario contenente le distanze tra i nodi
        - Elimina le distanze tra un nodo e se stesso
        - Elimina le distanze duplicate
        - Inserisce un flag per indicare se il nodo è stato visitato o meno
    '''
    for key in list(dist):
        # Elimina le distanze tra un nodo e se stesso
        if key[0] == key[1]:
            del dist[key]
        # Elimina le distanze duplicate
        if (key[1], key[0]) in dist:
            del dist[key]
    # Inserisce un flag per indicare se il nodo è stato visitato o meno
    for key in dist.keys():
        dist[key] = (dist[key], False)
            
import random
import tsp_utils 

# Parametri per il grafo
n = 10  # Numero di nodi
maxcoord = 100  # Massima coordinata

# Genera un grafo casuale
points, dist = tsp_utils.randomEuclGraph(n, maxcoord)

# print("\nDistanze tra i nodi:")
# for (i, j), distance in dist.items():
#     print(f"Distanza tra Nodo {i} e Nodo {j}: {distance:.2f}")

elaborete_dist(dist)

# print("\nDistanze tra i nodi POST-ELABORAZIONE:")
# for (i, j), distance in dist.items():
#     print(f"Distanza tra Nodo {i} e Nodo {j}: {distance[0]:.2f} - Flag: {distance[1]}")

# print("Punti (nodi del grafo):")
# for index, point in enumerate(points):
#     print(f"Nodo {index}: {point}")

# print("\nDistanze tra i nodi:")
# for (i, j), distance in dist.items():
#     print(f"Distanza tra Nodo {i} e Nodo {j}: {distance:.2f}")
# input("Premi un tasto per continuare...")

# Estrazione di un nodo a caso
# random_node_index = random.randint(0, n - 1)
random_node_index = 2
random_node = points[random_node_index]

print(f"\nNodo scelto a caso: Nodo {random_node_index} con coordinate {random_node}")

next_node = next_node(random_node_index, dist)
print(f"Il prossimo nodo da visitare è: {next_node[0][0]} con distanza {next_node[1][0]:.2f}")

# Adesso devo scegliere il prossimo nodo da visitare, per farlo devo prima ordinare i nodi in base alla distanza dal nodo corrente
# Ordino i nodi in base alla distanza dal nodo corrente
# for i in range(n):
#     next_node(i, dist)
#     input("Premi un tasto per continuare...")

