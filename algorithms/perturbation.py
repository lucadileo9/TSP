'''
This module provides various perturbation functions for the Traveling Salesman Problem (TSP). 
Each function applies a different type of perturbation to a given TSP solution to explore the solution space.
Functions:
    perturbation(solution, phase, points, n, DEBUG=False):
        Applies a perturbation to the current path based on the current phase.
    two_opt_randomized(solution, n, points, DEBUG=False):
        Performs a randomized 2-opt perturbation by selecting a random segment and reversing its order.
    multi_swap(solution, k, points, DEBUG=False):
        Executes k random swaps between pairs of nodes with validity checks.
    shuffle_partial(solution, n, points, DEBUG=False):
        Randomly selects a subsequence of nodes in the path and shuffles them.
    three_opt_randomized(solution, points, DEBUG=False):
        Applies a randomized 3-opt perturbation by dividing the path into three random segments and reconnecting them.
    double_bridge_move(solution, points, DEBUG=False):
        Cuts the path into four distinct segments and recombines them by swapping the positions of two central segments.
    perturbation_swap_segments(solution, points, DEBUG=False):
        Selects two random segments in the path, ensuring they do not overlap, and swaps their positions.
Usage:
    The perturbation functions can be used to explore the solution space of the TSP by applying different types of perturbations to a given solution.
    Example:
        python perturbation.py
    This will test the perturbation functions by applying each perturbation type to a sample TSP solution.
'''
import numpy as np
import random

from ..utils.algorithm_metrics import check_path

def perturbation(solution, phase, points,n, DEBUG=False):
    """
    Applica una perturbazione al percorso attuale in base alla fase corrente.
    La perturbazione può essere di diverso tipo a seconda della fase:
    - "aggressive": double bridge move
    - "medium": multi-swap
    - "soft": 2-opt randomizzata
    The number of multi-swap operations is set to n//50, and the number of nodes to shuffle is set to n//10, 
    so that the perturbation is proportional to the size of the problem.
    Args:
        solution (list): Il percorso attuale.
        phase (str): La fase corrente ("aggressive", "medium", "soft").
        points (list): Lista di punti (coordinate o dati relativi al problema TSP).
        n (int): Numero di nodi del problema TSP.
        DEBUG (bool): Se True, stampa informazioni aggiuntive.
    Returns:
        list: Il percorso perturbato valido.
    """
    
    if phase == "aggressive":
        return double_bridge_move(solution, points, DEBUG=DEBUG)
    elif phase == "medium":
        return multi_swap(solution, k=n//50 , points=points, DEBUG=DEBUG)
    elif phase == "soft":
        return shuffle_partial(solution, n=n//10, points=points, DEBUG=DEBUG)
    else:
        raise ValueError("Fase non valida.")
    
    
def two_opt_randomized(solution, n, points, DEBUG=False):
    """
    Effettua una perturbazione sul percorso attuale selezionando un segmento casuale e invertendone l'ordine.
    È una variante del classico algoritmo 2-opt, ma il segmento da invertire viene scelto in modo casuale
    Viene effettuato anche un controllo di validità.
    Args:
        solution (list): Il percorso attuale.
        n (int): Lunghezza del segmento da invertire.
        points (list): Lista di punti (coordinate o dati relativi al problema TSP).
        DEBUG (bool): Se True, stampa informazioni aggiuntive.
    Returns:
        list: Il percorso perturbato valido.
    """
    size = len(solution) - 1  # Escludi l'ultimo nodo
    while True:
        i = random.randint(1, size - n - 1)  # Evita il primo e l'ultimo nodo
        j = i + n
        new_solution = solution[:i] + solution[i:j][::-1] + solution[j:]
        if check_path(points, new_solution):
            if DEBUG:
                print(f"2-opt valido trovato: i={i}, j={j}")
            return new_solution
        elif DEBUG:
            print(f"2-opt non valido: i={i}, j={j}. Rigenero...")

def multi_swap(solution, k, points, DEBUG=False):
    """
    Esegue k scambi casuali tra coppie di nodi con controllo di validità.
    Args:
        solution (list): Il percorso attuale.
        k (int): Numero di scambi casuali da effettuare.
        points (list): Lista di punti (coordinate o dati relativi al problema TSP).
        DEBUG (bool): Se True, stampa informazioni aggiuntive.
    Returns:
        list: Il percorso perturbato valido.
    """
    size = len(solution) - 1  # Escludi l'ultimo nodo
    while True:
        new_solution = solution[:]
        for _ in range(k):
            i, j = random.sample(range(1, size), 2)  # Evita il primo e l'ultimo nodo
            new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        if check_path(points, new_solution, DEBUG):
            if DEBUG:
                print(f"Multi-swap valido con {k} scambi.")
            return new_solution
        elif DEBUG:
            print(f"Multi-swap non valido. Rigenero...")

def shuffle_partial(solution, n, points, DEBUG=False):
    """
    Seleziona casualmente una sottosequenza di nodi nel percorso e la mescola in modo casuale.
    Viene effettuato anche un controllo di validità.
    Args:
        solution (list): Il percorso attuale.
        n (int): Lunghezza della sottosequenza da mescolare.
        points (list): Lista di punti (coordinate o dati relativi al problema TSP).
        DEBUG (bool): Se True, stampa informazioni aggiuntive.
    Returns:
        list: Il percorso perturbato valido.
    """
    size = len(solution) - 1  # Escludi l'ultimo nodo
    while True:
        i = random.randint(1, size - n - 1)  # Evita il primo e l'ultimo nodo
        j = i + n
        segment = solution[i:j]
        random.shuffle(segment)
        new_solution = solution[:i] + segment + solution[j:]
        if check_path(points, new_solution, DEBUG):
            if DEBUG:
                print(f"Shuffle valido: segmento [{i}:{j}] mescolato.")
            return new_solution
        elif DEBUG:
            print(f"Shuffle non valido: segmento [{i}:{j}]. Rigenero...")

def three_opt_randomized(solution, points, DEBUG=False):
    """
    Applica una perturbazione 3-opt randomizzata con controllo di validità.
    Introduce una perturbazione più complessa dividendo il percorso in tre segmenti casuali
    e riconnettendoli in uno dei diversi modi possibili (incluso il loro ordine originale o inversioni).
    Args:
        solution (list): Il percorso attuale.
        points (list): Lista di punti (coordinate o dati relativi al problema TSP).
        DEBUG (bool): Se True, stampa informazioni aggiuntive.
    Returns:
        list: Il percorso perturbato valido.
    """
    size = len(solution) - 1  # Escludi l'ultimo nodo
    while True:
        a, b, c = sorted(random.sample(range(1, size), 3))  # Evita il primo e l'ultimo nodo
        configurations = [
            solution[:a] + solution[a:b] + solution[b:c] + solution[c:],  # Originale
            solution[:a] + solution[b:c] + solution[a:b] + solution[c:],  # Swap 1
            solution[:a] + solution[a:b][::-1] + solution[b:c] + solution[c:],  # Reverse 1
            solution[:a] + solution[b:c] + solution[a:b][::-1] + solution[c:],  # Reverse 2
            solution[:a] + solution[a:b][::-1] + solution[b:c][::-1] + solution[c:],  # Reverse 3
            solution[:a] + solution[c:b:-1] + solution[a:b] + solution[c:],  # Complex swap 1
            solution[:a] + solution[b:c] + solution[c:a:-1] + solution[:c]  # Complex swap 2
        ]
        new_solution = random.choice(configurations)
        if check_path(points, new_solution):
            if DEBUG:
                print(f"3-opt valido trovato: a={a}, b={b}, c={c}.")
            return new_solution
        elif DEBUG:
            print(f"3-opt non valido: a={a}, b={b}, c={c}. Rigenero...")

def double_bridge_move(solution, points, DEBUG=False):
    """
    Taglia il percorso in quattro segmenti distinti e li ricombina scambiando la posizione di due segmenti centrali
    Viene effettuato anche un controllo di validità.
    Args:
        solution (list): Il percorso attuale.
        points (list): Lista di punti (coordinate o dati relativi al problema TSP).
        DEBUG (bool): Se True, stampa informazioni aggiuntive.
    Returns:
        list: Il percorso perturbato valido.
    """
    size = len(solution) - 1  # Escludi l'ultimo nodo
    if size < 8:
        raise ValueError("La soluzione deve contenere almeno 8 nodi per il Double Bridge Move.")
    while True:
        a, b, c, d = sorted(random.sample(range(1, size), 4))  # Evita il primo e l'ultimo nodo
        new_solution = (
            solution[:a] +
            solution[c:d] +
            solution[b:c] +
            solution[a:b] +
            solution[d:]
        )
        if check_path(points, new_solution, DEBUG):
            if DEBUG:
                print(f"Double Bridge Move valido trovato: a={a}, b={b}, c={c}, d={d}.")
            return new_solution
        elif DEBUG:
            print(f"Double Bridge Move non valido: a={a}, b={b}, c={c}, d={d}. Rigenero...")


def perturbation_swap_segments(solution, points, DEBUG=False):
    """
    Seleziona due segmenti casuali nel percorso, assicurandosi che non si sovrappongano,
    e li scambia di posizione
    Viene effettuato anche un controllo di validità.
    Args:
        solution: Lista rappresentante il percorso attuale.
        points: Lista di punti (coordinate o dati relativi al problema TSP).
        DEBUG: Se True, stampa informazioni aggiuntive.

    Returns:
        Lista rappresentante il percorso perturbato valido.
    """
    size = len(solution) - 1  # Escludi l'ultimo nodo
    while True:
        # Genera due segmenti casuali
        i1, j1 = sorted(random.sample(range(1, size), 2))  # Evita il primo e l'ultimo nodo
        i2, j2 = sorted(random.sample(range(1, size), 2))  # Evita il primo e l'ultimo nodo

        # Assicura che i segmenti non si sovrappongano
        while i1 <= j2 and i2 <= j1:
            i1, j1 = sorted(random.sample(range(1, size), 2))
            i2, j2 = sorted(random.sample(range(1, size), 2))

        if DEBUG:
            print(f"Swap segments: scelti segmenti [i1={i1}, j1={j1}] e [i2={i2}, j2={j2}]")

        # Scambia i segmenti
        new_solution = solution.copy()
        segment1 = new_solution[i1:j1+1]
        segment2 = new_solution[i2:j2+1]
        new_solution[i1:j1+1] = segment2
        new_solution[i2:j2+1] = segment1

        # Verifica la validità della soluzione
        if check_path(points, new_solution):
            if DEBUG:
                print("Soluzione valida trovata.")
            return new_solution
        elif DEBUG:
            print("Soluzione non valida, rigenero...")

if __name__ == "__main__":
    current_solution = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,0]
    points= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("Soluzione iniziale:", current_solution)

    # Perturbazioni
    perturbed_solution = perturbation_swap_segments(current_solution, points, DEBUG=True)
    print("Perturbazione Swap Segments:", perturbed_solution) 

    # 2-opt randomizzato
    perturbed_solution = two_opt_randomized(current_solution, n=3, points=points, DEBUG=True)
    print("Perturbazione 2-opt randomizzata:", perturbed_solution)

    # Multi-swap
    perturbed_solution = multi_swap(current_solution, k=2, points=points, DEBUG=True)
    print("Perturbazione Multi-swap:", perturbed_solution)

    # Shuffle parziale
    perturbed_solution = shuffle_partial(current_solution, n=4, points=points, DEBUG=True)
    print("Perturbazione Shuffle Parziale:", perturbed_solution)

    # 3-opt randomizzato
    perturbed_solution = three_opt_randomized(current_solution, points=points, DEBUG=True)
    print("Perturbazione 3-opt randomizzata:", perturbed_solution)

    # Double Bridge Move
    perturbed_solution = double_bridge_move(current_solution, points=points, DEBUG=True)
    print("Perturbazione Double Bridge Move:", perturbed_solution)