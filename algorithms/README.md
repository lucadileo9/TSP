# README - Directory `algorithms`

## **Introduzione**
La directory `algorithms` contiene il cuore algoritmico del progetto sul TSP. Qui si trovano gli script che implementano le metaeuristiche, le tecniche di local search, la generazione di vicinati e le strategie di perturbazione, elementi fondamentali per affrontare il problema del TSP in modo efficace e innovativo.

Questa directory è progettata per essere modulare e riutilizzabile: ogni file ha uno scopo specifico e tutte le funzioni sono documentate internamente per facilitarne l'uso.

---

## **Struttura dei File**

| File                     | Descrizione                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `metaheuristic_algorithms.py`                  | Implementazione della metaeuristica Simulated Annealing (SA) e Iterated Local Search (ILS).            |
| `hybrid_metaheuristic.py`       | Implementazione della metaeuristica ibrida che combina ILS e SA.          |
| `local_search_algorithms.py`        | Algoritmi per la ricerca locale su soluzioni del TSP.                     |
| `neighborhood_generatos.py`        | Funzioni per la generazione di vicinati (es. swap, inversion, ecc.).       |
| `perturbation.py`        | Funzioni per perturbare soluzioni, parte integrante di ILS.               |

---

## **Metaeuristiche**

### **Iterated Local Search (ILS)**
La metaeuristica ILS si basa sull'idea di migliorare iterativamente una soluzione tramite cicli di perturbazione e local search.

### **Simulated Annealing (SA)**
La metaeuristica SA è ispirata al processo fisico di ricottura, dove si cerca di sfuggire a minimi locali accettando soluzioni peggiori con una probabilità decrescente nel tempo.

### **Metaeuristica Ibrida (ILS + SA)**
L'algoritmo ibrido combina i punti di forza di ILS e SA: utilizza il framework iterativo di ILS, ma integra SA nella ricerca locale per migliorare l'esplorazione del vicinato.

---

## **Local Search e Vicinati**

### **Local Search**
Sono implementati diversi algoritmi di ricerca locale, ognuno mirato a migliorare una soluzione nel contesto di specifici vicinati.

### **Vicinati**
La directory include metodi per generare diversi tipi di vicinati, tra cui:
- **Swap**: Scambia due nodi del percorso.
- **Inversion**: Inverte una sottosequenza di nodi.

---

## **Perturbazioni**

Le funzioni di perturbazione svolgono un ruolo chiave nel framework di ILS, introducendo variazioni casuali controllate alle soluzioni per evitare minimi locali e migliorare la diversità delle soluzioni esplorate.

---

## **Guida all'Esecuzione**

Gli script di questa directory possono essere eseguiti direttamente tramite il comando:
```bash
python -m TSP.algorithms.[fileName]
```
Ad esempio, per eseguire la metaeuristica ILS:
```bash
python -m TSP.algorithms.ils
```

---

## **Ulteriori Informazioni**
Per dettagli tecnici su ogni funzione o algoritmo, consultare la documentazione presente nei file di codice. Ogni script include spiegazioni approfondite sulle implementazioni e i parametri utilizzati.

