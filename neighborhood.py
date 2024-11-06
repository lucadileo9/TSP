from my_utils import print_in_square

def swap_neighborhood(path):
    """
    Generate all possible neighbors of a path by swapping two nodes.
    
    Args:
        path (list): The current path (a list of node indices).
    
    Returns:
        list: A list of paths, each created by swapping two nodes in the original path.
    """
    neighbors = []
    n = len(path)
    
    # For each pair of nodes (i, j), perform a swap
    for i in range(1, n - 1):        # Avoid swapping the start and end nodes (0 and last)
        for j in range(i + 1, n - 1):
            # Create a copy of the path to avoid modifying the original
            new_path = path[:]
            # Perform the swap
            new_path[i], new_path[j] = new_path[j], new_path[i]
            # Add the new path to the neighborhood
            neighbors.append(new_path)
    
    return neighbors


# Pseudocode:
# procedure 2optSwap(route, v1, v2) {
#     1. take route[start] to route[v1] and add them in order to new_route
#     2. take route[v1+1] to route[v2] and add them in reverse order to new_route
#     3. take route[v2+1] to route[start] and add them in order to new_route
#     return new_route;
# }
def two_opt_neighborhood(path, print_neighbors=False):
    """
    Generates the 2-opt neighborhood for a given path in the Traveling Salesman Problem (TSP).
    The 2-opt neighborhood is created by reversing the order of nodes between two indices in the path.
    This function generates all possible 2-opt neighbors by considering all pairs of indices (i, j) 
    where 1 <= i < j - 1 < len(path) - 1.
    Args:
        path (list): A list representing the current path of nodes in the TSP.
    Returns:
        list: A list of paths, each representing a neighbor obtained by a 2-opt move.
    """
    neighbors = []
    n = len(path)
    # Generate all possible 2-opt neighbors
    for i in range(1, n - 2): # i starts from 1 to avoid the start node and ends at n - 2 to avoid the second-to-last node, as the last node (typically the starting node again) cannot be swapped with any other node
        for j in range(i + 3, n - 1):  # if j started from i it would swap a node with itself, if it started from i+1 it would swap two consecutive nodes, if it started from i+2 it would swap two nodes with only one node in between, not creating a true path inversion but rather a swap
            # and ends at n - 1 to avoid the end node
            new_path = path[:i] + path[i:j+1][::-1] + path[j+1:] # From start to i {path[:i]}, then from i+1 to j in reverse order {path[i:j+1][::-1]}, and finally from j+1 to the end {path[j+1:]}
            neighbors.append(new_path)
            
    if print_neighbors:
        print_in_square("Path", path)
        print("2-opt Neighborhood:")
        for neighbor in neighbors:
            print(neighbor)
    return neighbors

if __name__ == "__main__":
    path = [0, 1, 2, 3, 4, 5, 6, 7]
    two_opt_neighborhood(path, print_neighbors=True)
    swap_neighborhood(path)
    print_in_square("Path", path)
    print("Swap Neighborhood:")
    for neighbor in swap_neighborhood(path):
        print(neighbor)