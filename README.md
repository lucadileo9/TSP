# TSP Solver Project

This repository contains a solution to the **Traveling Salesman Problem (TSP)** using a greedy nearest neighbor approach. The project is divided into multiple files to ensure modularity and clarity, including a main execution file, a testing suite, and utility functions for TSP algorithms.

## Project Structure

- **main.py**: Contains the main logic to run the TSP solver with different configurations. This file is the entry point of the project.
  
- **tester.py**: Includes various tests to validate the correctness of the TSP solutions. It ensures that the algorithms work under different conditions and setups.

- **my_utils.py**: Contains custom utility functions for the TSP solver. This includes different algorithms, such as the greedy nearest neighbor approach with random selection between the closest points.

- **tsp_utils.py**: A collection of utility functions taken from an external source to handle TSP-specific calculations and helpers (e.g., distance calculation, graph representation).

## Algorithms Implemented

1. **Nearest Neighbor Algorithm**: A greedy algorithm that starts from a random point and at each step selects the nearest unvisited neighbor. In some cases, it selects randomly between the first and second closest points.
   
2. **Random Euclidean Graph Generator**: Generates a random instance of a TSP graph with Euclidean distances between points, useful for testing various algorithms on randomly generated data.

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

   You can modify parameters inside `main.py` to run the TSP solver with different settings (e.g., number of points, maximum coordinate values).

## Installation

To run this project, you need:

- Python 3.x

There shouldn't be any other dependencies needed, but I'm not sure.

## Customization

- You can add your own algorithms inside `my_utils.py` and test them using `tester.py`.
- Modify the graph generator in `my_utils.py` to create different types of graphs (e.g., non-Euclidean).

## Future Improvements

- Implement other heuristic algorithms like Simulated Annealing or Genetic Algorithms to compare their performance with the nearest neighbor approach.
- Add a graphical user interface (GUI) to visualize the TSP paths.

## Contributing

Feel free to submit pull requests or report issues. Contributions to improve the algorithms or add new features are welcome.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
