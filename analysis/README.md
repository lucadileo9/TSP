# README - Directory `analysis`

## **Introduzione**
La directory `analysis` si occupa di analizzare le prestazioni degli algoritmi implementati nel progetto, con particolare attenzione ai risultati su istanze del TSPLIB. Questa directory consente di generare dataset, eseguire test su vari algoritmi e confrontare le loro performance in termini di qualità della soluzione e tempi di esecuzione.

Ogni file è autonomo ed eseguibile, facilitando la comprensione del loro funzionamento e l’integrazione con altre parti del progetto.

---

## **Struttura dei File**

| File                              | Descrizione                                                                                      |
|-----------------------------------|--------------------------------------------------------------------------------------------------|
| `dataset_generator.py`             | Genera un dataset per testare vari algoritmi greedy su istanze generate casualmente.            |
| `benchmark_runner.py`              | Valuta algoritmi greedy sul dataset generato, misurando lunghezza del percorso e tempi di esecuzione. |
| `analyze_performances.py`              | Esegue il multistart su istanze della TSPLIB, combinando algoritmi di vicinato e greedy.         |
| `metaheuristics_comparison.py`       | Confronta diverse metaeuristiche sulle istanze della TSPLIB.                                     |

---

## **Descrizione dei File**

### **`dataset_generator.py`**
Questo script permette di creare un dataset personalizzato per testare algoritmi greedy. Ogni istanza è generata con parametri configurabili per dimensioni e caratteristiche dei nodi.

### **`benchmark_runner.py`**
Testa gli algoritmi greedy sul dataset creato, producendo risultati dettagliati che includono:
- Lunghezza totale del percorso.
- Tempo per trovare la soluzione.
- Tempo medio di esecuzione per ogni algoritmo.

### **`analyze_performances.py`**
Esegue una combinazione di algoritmi greedy e di vicinato in un framework multistart. Questo approccio permette di valutare l’efficacia delle diverse combinazioni nel migliorare le soluzioni su istanze della TSPLIB.

### **`metaheuristics_comparison.py`**
Confronta le prestazioni delle metaeuristiche implementate (inclusa la metaeuristica ibrida ILS + SA). I risultati includono metriche di qualità della soluzione per ciascuna istanza della TSPLIB.

---

## **Guida all'Esecuzione**

Gli script possono essere eseguiti direttamente tramite il comando:
```bash
python -m TSP.analysis.[fileName]
```
Ad esempio, per generare un dataset:
```bash
python -m TSP.analysis.generate_dataset
```

---

## **Output**
Gli script producono file di output salvati nella directory `outputs`, come:
- **JSON**: Dati relativi alle performance (es. tempi, lunghezze dei percorsi).

---

## **Ulteriori Informazioni**
Per una descrizione approfondita di ogni script e delle relative funzioni, consultare la documentazione interna nei file di codice.

