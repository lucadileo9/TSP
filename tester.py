# In this file there will be a function that takes as input the points of a graph and the path connecting them, and checks if the path is correct.
# Specifically, it checks that:
#  - no node is visited twice,
#  - the path is closed,
#  - all nodes are present,
#  - the nodes are part of the graph.
def check_path(points, path):
    """
    Validates a given path in a graph.

    This function performs several checks to ensure that the provided path is valid:
    1. The path must be closed (i.e., the first and last nodes must be the same).
    2. The path must contain all the nodes in the graph.
    3. The path must only contain nodes that are present in the graph.
    4. Each node in the path (except for the first and last) must appear only once.

    Parameters:
        points (list): A list of nodes in the graph.
        path (list): A list representing the path to be checked.

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    # check if the path is closed
    if path[0] != path[-1]:
        print("The path is not closed")
        return False
    # check if the path contains all the nodes
    for i in range(len(points)):
        if i not in path:
            print("The path doesn't contain all the nodes")
            return False
    # check if the path contains only the nodes in the graph
    for i in path:
        if i >= len(points):
            print("The path contains nodes not in the graph")
            return False
    # check if the path contains the nodes only once, except for the first and the last 
    for i in range(1, len(path) - 1):
        if path.count(path[i]) != 1:
            print("The path contains nodes more than once")
            return False
    return True
