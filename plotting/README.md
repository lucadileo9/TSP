# README - Directory `plotting`

## **Introduzione**
La directory `plotting` contiene script utilizzati per la visualizzazione grafica dei risultati delle analisi effettuate nel progetto. Questi strumenti aiutano a confrontare le prestazioni degli algoritmi e delle metaeuristiche sviluppati.

---

## **Struttura dei File**

| File                          | Descrizione                                                                                              |
|-------------------------------|----------------------------------------------------------------------------------------------------------|
| `comparison_plot.py`| Genera grafici per confrontare i risultati delle metaeuristiche in termini di qualità delle soluzioni.   |
| `greedy_plot.py`   | Visualizza le prestazioni degli algoritmi greedy in termini di lunghezza del percorso, tempi d'esecuzione e tempi medi d'esecuzione.      |
| `performances_plot.py`  | Confronta le prestazioni di diverse combinazioni di algoritmi di local search.                           |

---

## **Descrizione dei File**

### **`metaheuristics_comparison.py`**
Questo script:
- Genera grafici comparativi per valutare le prestazioni delle diverse metaeuristiche.
- Mostra metriche come la lunghezza del percorso e il tempo di esecuzione per ogni metaeuristica.

### **`greedy_algorithms_plot.py`**
Questo script:
- Crea grafici che confrontano gli algoritmi greedy.
- Evidenzia la lunghezza del percorso trovato e il tempo necessario per completare l'algoritmo.

### **`local_search_comparison.py`**
Questo script:
- Confronta combinazioni di algoritmi di local search, inclusi vicinati e algoritmi greedy.
- Mostra come cambiano le prestazioni con diverse configurazioni.

---

## **Guida all'Esecuzione**

Gli script in questa directory sono progettati per essere eseguiti direttamente. Assicurarsi che i dati necessari siano presenti nella directory `outputs`.

Esempio di esecuzione:
```bash
python -m TSP.plotting.metaheuristics_comparison
```
Conviene leggere il main di ogni script per capire come funziona e quali parametri accetta.

---

## **Output**
Talvolta i grafici generati vengono salvati nella directory `outputs/plots` in formato PNG.

---

## **Ulteriori Informazioni**
Per ulteriori dettagli sul funzionamento di ogni script, consultare i commenti e i docstring all'interno del codice.

