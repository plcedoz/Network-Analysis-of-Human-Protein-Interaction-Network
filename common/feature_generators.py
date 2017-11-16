import numpy as np
import networkx as nx
import pickle
from tqdm import tqdm
import os

class FeatureGenerator(object):
    def __init__(self, default_recomputing=False, default_dump=True, prefix=''):
        self.cache_filename = None
        self.default_recomputing = default_recomputing
        self.prefix = prefix
        self.default_dump = default_dump

    def get_name(self):
        pass

    def compute(self):
        pass

    def init_filename(self):
        if not os.path.exists('data/cache/'):
            os.mkdir('data/cache/')
        self.cache_filename = 'data/cache/{}_featurecache_{}.pkl'.format(self.prefix, self.get_name())

    def load_from_cache(self):
        if self.cache_filename is None:
            self.init_filename()
        result = pickle.load(open(self.cache_filename, 'rb'))
        return result

    def dump_to_cache(self, result):
        if self.cache_filename is None:
            self.init_filename()
        pickle.dump(result, open(self.cache_filename, 'wb'))

    def apply(self, Graph, recompute=None, dump=None):
        if recompute is None:
            recompute = self.default_recomputing
        if dump is None:
            dump = self.default_dump
        if not recompute:
            try:
                return self.load_from_cache()
            except:
                return self.apply(Graph, recompute=True)
        else:
            result = self.compute(Graph)
            if dump:
                self.dump_to_cache(result)
            return result


class Degree(FeatureGenerator):
    '''
    Degree of every node (in/out if directed)
    '''

    def __init__(self, directed=False, default_recomputing=True, default_dump=False, prefix=''):
        super(Degree, self).__init__(default_recomputing=default_recomputing, default_dump=default_dump, prefix=prefix)
        self.directed = directed
        self.nfeat = 1 + self.directed

    def get_name(self):
        return "degree_{}directed".format("" if self.directed else "un")

    def compute(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros((n, self.nfeat))
        if not self.directed:
            for i in range(n):
                result[i] = Graph.degree(i)
        else:
            for i in range(n):
                result[i, 0] = Graph.out_degree(i)
                result[i, 1] = Graph.in_degree(i)
        return result


class ExpectedDegree(FeatureGenerator):
    '''
    Expected degree of every node, considering every edge is weighted with the
    probability of its existence (in/out if directed)
    '''

    def __init__(self, directed=False, default_recomputing=True, default_dump=False, prefix=''):
        super(ExpectedDegree, self).__init__(default_recomputing=default_recomputing, default_dump=default_dump,
                                             prefix=prefix)
        self.directed = directed
        self.nfeat = 1 + self.directed

    def get_name(self):
        return "expecteddegree_{}directed".format("" if self.directed else "un")

    def compute(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros((n, self.nfeat))
        if not self.directed:
            for i in range(n):
                for j in Graph.neighbors(i):
                    result[i] += Graph[i][j]['weight'] / 1000.0
        else:
            for i in range(n):
                for j in Graph.successors(i):
                    result[i, 0] += Graph[i][j]['weight'] / 1000.0
                for j in Graph.predecessors(i):
                    result[i, 1] += Graph[j][i]['weight'] / 1000.0
        return result


class PageRank(FeatureGenerator):
    '''
    PageRank score of every node in the graph (can be quite heavy to compute)
    '''

    def __init__(self, default_recomputing=False, default_dump=True, prefix=''):
        super(PageRank, self).__init__(default_recomputing=default_recomputing, default_dump=default_dump,
                                       prefix=prefix)
        self.nfeat = 1

    def get_name(self):
        return "pagerank"

    def compute(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros((n, self.nfeat))
        pr = nx.algorithms.pagerank(Graph)
        for i, p in pr.items():
            result[i] = p
        return result


class BetweennessCentrality(FeatureGenerator):
    '''
    Betweenness centrality of every node in the graph (can be quite heavy to compute)
    '''
    def __init__(self,default_recomputing = False, default_dump=True,prefix=''):
        super(BetweennessCentrality,self).__init__(default_recomputing = default_recomputing, default_dump=default_dump,prefix=prefix)
        self.nfeat = 1

    def get_name(self):
        return "betweenness"

    def compute(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros((n, self.nfeat))
        bc = nx.betweenness_centrality(Graph)
        for i,c in bc.items():
            result[i] = c
        return result


class ClusteringCoefficient(FeatureGenerator):
    """
    Clustering Coefficient
    """
    def __init__(self, default_recomputing=False, default_dump=True, prefix=''):
        super(ClusteringCoefficient, self).__init__(default_recomputing=default_recomputing, default_dump=default_dump,
                                       prefix=prefix)
        self.nfeat = 1

    def get_name(self):
        return "clusteringcoefficient"

    def compute(self,Graph):
        list_nodes = Graph.nodes()
        n = len(list_nodes)
        result = np.zeros((n, self.nfeat))
        for node in tqdm(list_nodes,desc="Clustering Coefficient"):
            result[node]=nx.algorithms.clustering(Graph, node)
        return result

    
class ClosenessCentrality(FeatureGenerator):
    '''
    Closeness centrality of every node in the graph (can be quite heavy to compute)
    '''
    def __init__(self,default_recomputing = False, default_dump=True,prefix=''):
        super(ClosenessCentrality,self).__init__(default_recomputing = default_recomputing, default_dump=default_dump,prefix=prefix)
        self.nfeat = 1

    def get_name(self):
        return "closeness"

    def compute(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros((n, self.nfeat))
        cc = nx.closeness_centrality(Graph)
        for i,c in cc.items():
            result[i] = c
        return result
