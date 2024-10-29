# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:00:58 2022

@author: Mauro
"""
import math
import random
from csv import reader
import matplotlib.pyplot as plt
import tsplib95 



def plot_selectedEdges2D(points, edges, selectededges=[], title="", figsize=(12, 12), save_fig=None):
    """
    Plot a graph in 2D emphasizing a set of selected edges .

    :param points: list of points.
    : param edges: all the edges of the graph
    :param selectededges: list of selected edges
    :param title: title of the figure.
    :param figsize: width and height of the figure
    :param save_fig: if provided, path to file in which the figure will be save.
    :return: None
    """

    plt.figure(figsize=figsize)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(title, fontsize=15)
    plt.grid()
    x = [pnt[0] for pnt in points]
    y = [pnt[1] for pnt in points]
    plt.scatter(x, y, s=60)

    maxx = max(x)
    maxy=max(y)
    # Add label to points
    for i, label in enumerate(points):
        plt.annotate('{}'.format(i), (x[i]+0.001/maxx, y[i]+0.001/maxy), size=25)

   # Add the edges
    for (i,j) in edges:
        if i < j:
            plt.plot([points[i][0], points[j][0]], [points[i][1], points[j][1]], 'b', alpha=.5)
    # plots the selected edges (sub)tours
    for (i, j) in selectededges:
       plt.plot([points[i][0], points[j][0]], [points[i][1], points[j][1]], 'r', alpha=1.,linewidth=3)
       
    if save_fig:
        plt.savefig(save_fig)
    else:
        plt.show()
        
def read_csv_points(file_path, sep=',', has_headers=True, dtype=float):
    """
    Read a csv file containing 2D points.

    :param file_path: path to the csv file containing the points
    :param sep: csv separator (default ',')
    :param has_headers: whether the file has headers (default True)
    :param dtype: data type of values in the input file (default float)
    :return: list of points
    """
    with open(file_path, 'r') as f:
        csv_r = reader(f, delimiter=sep)

        if has_headers:
            headers = next(csv_r)
            print('Headers:', headers)

        points = [tuple(map(dtype, line)) for line in csv_r]
        print(points)

    return points

def EuclDist(points):
    """
    generates a dictionary of Euclidean distances between pairs of points    

    Parameters
    ----------
    points : list of pair of coordinates

    """
    # Dictionary of Euclidean distance between each pair of points
    dist = {(i, j):
            math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
            for i in range(len(points)) for j in range(len(points))}
            #for i in range(len(points)) for j in range(i)}
    return dist        

def randomEuclGraph (n, maxcoord):
    """
    generates an instance of an Euclidean graph
    Parameters
    ----------
    n number of vertices
    maxcoord maximum value of a coordinate of a vertex
    """
    points = [(random.randint(0, maxcoord), random.randint(0, maxcoord)) for i in range(n)]    
    dist = EuclDist(points)
        
    # Adesso aggiungo che ogni punto ha un flag che indica se è stato visitato o meno
    for i in range(n):
        points[i] = (points[i], False)
    
    # Modifico le distanze in modo che abbiano al più due cifre decimali
    for key in dist.keys():
        dist[key] = round(dist[key], 2)
    
    
    return points, dist

def randomGraphGeo (n, d):
    """
    generates an instance of a Geometric graph U_{n,d}, 
    generated drawing from an uniform distribution n points in a unit square, 
    associating a vertex with each point and adding edge [u, v] to the graph 
    iff the euclidean distance between u and v is less or equal to d.
    Parameters
    ----------
    n number of vertices
    d max distance between two connected vertices 
    """
    points = [(round(random.random(),2), round(random.random(),2)) for i in range(n)]            

    dist = {}
    for i in range(len(points)-1):
        for j in range(i+1,len(points)): 
            
            dij = math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
            if dij < d:
                dist.update({(i,j) : dij})
                dist.update({(j,i) : dij})
    
    
    # Modifico le distanze in modo che abbiano al più due cifre decimali
    for key in dist.keys():
        dist[key] = round(dist[key], 4)
    
    # Adesso aggiungo che ogni punto ha un flag che indica se è stato visitato o meno
    for i in range(n):
        points[i] = (points[i], False)
    
    return points, dist

def randomGraph2D (n, p):
    """
    generates an instance of a Random graph in 2D G_{n,p}, 
    generated drawing from an uniform distribution n points in a unit square, 
    associating a vertex with each point and adding edge [u, v] with probability p 
    Parameters
    ----------
    n number of vertices
    d max distance between two connected vertices 
    """
    points = [(round(random.random(),2), round(random.random(),2)) for i in range(n)]
    dist = {}
    for i in range(len(points)-1):
        for j in range(i+1,len(points)): 
            prob = random.random()
            dij = math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
            if prob < p:
                dist.update({(i,j) : dij})
                dist.update({(j,i) : dij})
    
    # Modifico le distanze in modo che abbiano al più due cifre decimali
    for key in dist.keys():
        dist[key] = round(dist[key], 4)
    
    # Adesso aggiungo che ogni punto ha un flag che indica se è stato visitato o meno
    for i in range(n):
        points[i] = (points[i], False)
        
    return points, dist    

def readTSPLIB(file_path):
    """
    Reads a TSPLIB file and extracts the problem's dimension, node coordinates, and edge weights.
    Args:
        file_path (str): The path to the TSPLIB file.
    Returns:
        tuple: A tuple containing:
            - n (int): The number of nodes in the TSP problem.
            - points (tuple): A tuple of coordinates for each node.
            - dist (dict): A dictionary where keys are tuples representing edges (i, j) and values are the weights of those edges.
    """
    problem = tsplib95.load(file_path)
    n = problem.dimension # number of nodes
    
    nodes = list(problem.get_nodes()) # get nodes
    nodes = [x-1 for x in nodes] # shift nodes to start from 0

    points = tuple(problem.node_coords.values()) # get coordinates of nodes
    if len(points) == 0:
        points = tuple(problem.display_data.values()) 
    
    edges = list(problem.get_edges()) # get edges
    edges = [(i-1,j-1) for (i,j) in edges] # shift edges to start from 0
    
    dist = {(i,j) : 0 for  (i,j) in edges} # initialize dictionary of distances
    for (i,j) in edges:
        dist[i,j] = problem.get_weight(i+1, j+1) # get weight of edge (i,j)
    
    return n, points, dist
