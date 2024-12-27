# README - Directory `utils`

## **Introduzione**
La directory `utils` contiene funzioni e moduli di supporto utilizzati in tutto il progetto. Questi strumenti migliorano la leggibilità, l'organizzazione e la riutilizzabilità del codice, semplificando operazioni comuni e fornendo funzionalità aggiuntive per la gestione delle istanze e dei dati.

---

## **Struttura dei File**

| File                          | Descrizione                                                                                          |
|-------------------------------|------------------------------------------------------------------------------------------------------|
| `algorithm_metrics.py`          | Contiene funzioni per il calcolo della lunghezza di un percorso e verifiche sulla sua validità e calcolo del tempo di esecuzione.     |
| `logger.py`         | Fornisce un decoratore per registrare quante volte e per quanto tempo vengono eseguite le funzioni. |
| `path_utils.py`        | Implementa vari algoritmi greedy per il TSP.                                                        |
| `tsplib_analysis_and_filter.py`             | Funzioni per analizzare e filtrare istanze della TSPLIB, oltre a organizzarle per test specifici.    |
| `tsp_utils.py`             | Funzioni di supporto per la manipolazione di istanze del TSP.                                        |
---

## **Descrizione dei File**

### **`algorithm_metrics.py`**
Contiene funzioni che permettono di:
- Calcolare la lunghezza di un percorso dato un grafo e una sequenza di nodi.
- Verificare la validità di un percorso (es. che tutti i nodi siano visitati una sola volta).
- Calcolare il tempo di esecuzione di una funzione.
- Calcolare il tempo medio di esecuzione di una funzione su più esecuzioni
oni, utili per valutare le prestazioni degli algoritmi implementati.

### **`logger.py`**
Questo modulo fornisce un decoratore che:
- Registra quante volte viene chiamata una funzione.
- Misura e registra il tempo totale di esecuzione per ogni funzione decorata.
I log vengono salvati nella directory `output/logs` e possono essere utilizzati per analizzare le prestazioni degli algoritmi e delle funzioni.

### **`path_utils.py`**
Implementa vari algoritmi greedy per il TSP, tra cui:
- Algoritmo del nearest neighbour.
- Algoritmo del nearest neighbour con scelta casuale.
- Algoritmo di brute force.
Ogni algoritmo è modulare e può essere combinato con altre tecniche nel progetto.

### **`tsplib_analysis_and_filter.py`**
Questo modulo fornisce strumenti per:
- Analizzare le istanze della TSPLIB (es. tipologia, dimensioni).
- Filtrare le istanze per criteri specifici (es. dimensioni, tipo di grafo).
- Organizzare le istanze per test specifici.

---

## **Ulteriori Informazioni**
Per una documentazione dettagliata su ogni funzione e il suo utilizzo, consultare i docstring all’interno dei file di codice.

