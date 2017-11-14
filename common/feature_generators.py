import numpy as np
import networkx as nx


class Degree:
    '''
    Degree of every node (in/out if directed)
    '''
    def __init__(self, directed=False):
        self.directed = directed
        self.nfeat = 1 + self.directed

    def get_name(self):
        return "degree_{}directed".format("" if self.directed else "un")

    def apply(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros((n,self.nfeat))
        if not self.directed:
            for i in range(n):
                result[i] = Graph.degree(i)
        else:
            for i in range(n):
                result[i,0] = Graph.out_degree(i)
                result[i,1] = Graph.in_degree(i)
        return result


class ExpectedDegree:
    '''
    Expected degree of every node, considering every edge is weighted with the
    probability of its existence (in/out if directed)
    '''
    def __init__(self, directed=False):
        self.directed = directed
        self.nfeat = 1 + self.directed

    def get_name(self):
        return "expecteddegree_{}directed".format("" if self.directed else "un")

    def apply(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros((n,self.nfeat))
        if not self.directed:
            for i in range(n):
                for j in Graph.neighbors(i):
                    result[i] += Graph[i][j]['weight'] / 1000.0
        else:
            for i in range(n):
                for j in Graph.successors(i):
                    result[i,0] += Graph[i][j]['weight'] / 1000.0
                for j in Graph.predecessors(i):
                    result[i,1] += Graph[j][i]['weight'] / 1000.0
        return result


class PageRank:
    '''
    PageRank score of every node in the graph (can be quite heavy to compute)
    '''
    def __init__(self):
        self.nfeat = 1

    def get_name(self):
        return "pagerank"

    def apply(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros(n)
        pr = nx.algorithms.pagerank(Graph)
        for i,p in pr.items():
            result[i] = p
        return result
