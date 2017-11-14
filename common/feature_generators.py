import numpy as np
import networkx as nx


class Degree:
    '''
    Degree of every node (in/out if directed set to True)
    '''
    def __init__(self, directed=False):
        self.directed = directed
        self.nfeat = 1 + self.directed

    def get_name(self):
        return "degree_{}directed".format("" if self.directed else "un")

    def apply(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros(n)
        for i in range(n):
            result[i] = Graph.degree(i)
        return result
