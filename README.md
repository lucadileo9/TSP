# TSP Solver Project

Questo progetto è stato sviluppato come parte del corso "Algoritmi di Ottimizzazione" e affronta il problema del Travelling Salesman Problem (TSP). L'obiettivo è stato quello di partire da algoritmi greedy basilari, sviluppare una local search e, infine, creare e testare una metaeuristica ibrida basata su ILS (Iterated Local Search) e SA (Simulated Annealing).

Il risultato finale del progetto è un'analisi approfondita delle performance della metaeuristica ibrida e delle altre tecniche utilizzate, testate su istanze del TSPLIB e confrontate tramite grafici e metriche.

## Project Structure

Il progetto è organizzato nelle seguenti directory:

- **algorithms**: Contiene le implementazioni di metaeuristiche, local search, generatori di vicinati, e funzioni per perturbare soluzioni (ILS).
- **analysis**: Include file per generare dataset e analizzare le performance di vari algoritmi su istanze del TSPLIB.
- **plotting**: Contiene script per visualizzare i risultati dei test effettuati.
- **utils**: Racchiude funzioni utili riutilizzabili, come algoritmi greedy, decoratori logger, e strumenti per analizzare le istanze del TSPLIB.
- **data**: Contiene dataset generati e istanze del TSPLIB organizzate.
- **outputs**: Salva risultati di test (JSON), log del logger e grafici generati dagli script di plotting.

Ogni directory include un README specifico con maggiori dettagli sui file e le loro funzionalità.

---

## How to Use

1. Clone the repository:

   ```bash
   git clone https://github.com/lucadileo9/TSP.git
   cd tsp-solver
   ```

2. Run the scripts:

   ```bash
    python -m TSP.[directory].[fileName]
   ```

## Installation

To run this project, you need:

- Python 3.x

There shouldn't be any other dependencies needed, but I'm not sure.

## Contributing

Feel free to submit pull requests or report issues. Contributions to improve the algorithms or add new features are welcome.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
