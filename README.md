# TSP Solver Project

This repository contains a solution to the **Traveling Salesman Problem (TSP)** using a greedy nearest neighbor approach. The project is divided into multiple files to ensure modularity and clarity, including a main execution file, a testing suite, and utility functions for TSP algorithms.

## Project Structure

- **main.py**: Contains the main logic to run the TSP solver with different configurations. This file is the entry point of the project.
  
- **tester.py**: Includes various tests to validate the correctness of the TSP solutions. It ensures that the algorithms work under different conditions and setups.

- **my_utils.py**: Contains custom utility functions for the TSP solver. This includes different algorithms, such as the greedy nearest neighbor approach with random selection between the closest points.

- **tsp_utils.py**: A collection of utility functions taken from an external source to handle TSP-specific calculations and helpers (e.g., distance calculation, graph representation).

## Algorithms Implemented

1. **Nearest Neighbor Algorithm**: A greedy algorithm that starts from a random point and at each step selects the nearest unvisited neighbor.
   
2. **Nearest Neighbor Algorithm with random choice**: A greedy algorithm that starts from a random point and at each step selects casually between the nearest unvisited neighbor and the second unvisited neighbor.

3. **Brute Force**: This algorithm finds the shortest path by calculating the distance for every possible permutation of points. It guarantees the optimal solution but is computationally expensive for large graphs.

## How to Use

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/tsp-solver.git
   cd tsp-solver
   ```

2. Run the main script:

   ```bash
   python main.py
   ```

You can run the project from the command line using the `main.py` script. Several command-line arguments are available to customize the execution.

### Command-line Arguments

- `-u_e`, `--use_existing`: Use existing graph data instead of generating new data.
- `-n`: Number of points in the graph (default: 10).
- `-m`, `--maxcoord`: Maximum coordinate value for points (default: 100).
- `-t`, `--test`: Run tests to validate the algorithms.
- `-dd`, `--data_debug`: Print debug information during data creation/loading.

### Example Commands

Generate a graph with 10 points, and 100 as maximum value for the coordinates, run all the algorithms without running tests:
```bash
python main.py -n 10 -m 100
```
Use existing graph data, run and all the algorithms:
```bash
python main.py --use_existing -t
```
Enable debug mode to print additional information during data creation:
```bash
python main.py -dd
```
## Installation

To run this project, you need:

- Python 3.x

There shouldn't be any other dependencies needed, but I'm not sure.

## Customization

- You can add your own algorithms inside `my_utils.py` and test them using `tester.py`.
- Modify the graph generator in `my_utils.py` to create different types of graphs (e.g., non-Euclidean).

## Test
The project includes a testing framework to ensure the correctness of the algorithms. The following functions are used to validate the output:
- check_path(): Verifies whether the calculated path is valid and visits all points.
- path_length(): Computes the total length of a given path.
- research_path_time(): Measures the execution time of the algorithms.
- average_research_path_time(): Averages the research time over multiple runs.

## Future Improvements

- Implement other heuristic algorithms like Simulated Annealing or Genetic Algorithms to compare their performance with the nearest neighbor approach.
- Add a graphical user interface (GUI) to visualize the TSP paths.

## Contributing

Feel free to submit pull requests or report issues. Contributions to improve the algorithms or add new features are welcome.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
