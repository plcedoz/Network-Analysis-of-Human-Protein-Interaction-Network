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
        self.nfeat=None

    def get_name(self):
        pass

    def get_feature_names(self):
        return [self.get_name()+str(i) for i in range(self.nfeat)]

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
        print("Computing Pagerank")
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


class HITS(FeatureGenerator):
    '''
    HITS score of every node in the graph (can be quite heavy to compute)
    '''

    def __init__(self, default_recomputing=False, default_dump=True, prefix=''):
        super(HITS, self).__init__(default_recomputing=default_recomputing, default_dump=default_dump,
                                       prefix=prefix)
        self.nfeat = 2

    def get_name(self):
        return "hits"

    def get_feature_names(self):
        return ["hits_hubs","hits_authorities"]

    def compute(self, Graph):
        n = Graph.number_of_nodes()
        result = np.zeros((n, self.nfeat))
        print("Computing HITS...")
        hubs,authorities = nx.algorithms.hits(Graph)
        for i in hubs.keys():
            result[i,0] = hubs[i]
            result[i,1] = authorities[i]
        return result


class NeighbouringConductance(FeatureGenerator):
    def __init__(self, range = 1,default_recomputing=False, default_dump=True, prefix=''):
        super(NeighbouringConductance, self).__init__(default_recomputing=default_recomputing, default_dump=default_dump,
                                       prefix=prefix)
        self.nfeat = 1
        self.range = range

    def get_name(self):
        return "Nconductance{}".format(self.range)

    def compute(self,Graph):
        n = Graph.number_of_nodes()
        result = np.zeros((n, self.nfeat))
        for node in tqdm(Graph.nodes(),desc=self.get_name()):
            neighs = set()
            new_neighs = set()
            new_neighs.add(node)
            for _ in range(self.range):
                neighs = neighs.union(new_neighs)
                next_neighs = set()
                for neigh in new_neighs:
                    next_neighs = next_neighs.union(set(Graph[neigh].keys()))
                new_neighs =  next_neighs.difference(neighs)
            if Graph.degree(node) == 0:
                result[node] = np.nan
            else:
                result[node] = nx.algorithms.cuts.conductance(Graph,neighs)
        return result


def Log10Wrapper(FeatureObject):
    class Log10(FeatureGenerator):
        """
        Log10 of a feature
        """

        def __init__(self, default_recomputing=False, default_dump=True, prefix=''):
            super(Log10,self).__init__(default_recomputing=default_recomputing, default_dump=default_dump,
                                           prefix=prefix)
            self.nfeat = FeatureObject.nfeat

        def get_name(self):
            return "log10-"+FeatureObject.get_name()

        def get_feature_names(self):
            return ["log10-"+ x for x in FeatureObject.get_feature_names()]

        def compute(self,Graph):
            result_local  = FeatureObject.apply(Graph)
            return np.log10(result_local)
    return Log10


def NormalizeWrapper(FeatureObject):
    class Normalized(FeatureGenerator):
        """
        Log10 of a feature
        """

        def __init__(self, default_recomputing=False, default_dump=True, prefix=''):
            super(Normalized,self).__init__(default_recomputing=default_recomputing, default_dump=default_dump,
                                           prefix=prefix)
            self.nfeat = FeatureObject.nfeat
            self.mean=None
            self.sd=None

        def get_name(self):
            return "normalized-"+FeatureObject.get_name()

        def get_feature_names(self):
            return ["normalized-" + x for x in FeatureObject.get_feature_names()]

        def compute(self,Graph):
            result_local  = FeatureObject.apply(Graph)
            self.mean = np.mean(result_local,axis=0)
            result_local = result_local - self.mean
            self.sd = np.std(result_local,axis = 0)
            result_local = result_local/self.sd
            return result_local
    return Normalized

def FeatureSelector(FeatureObject):
    class Selected(FeatureGenerator):
        """
        Select a list of columns
        """

        def __init__(self, columns = None,default_recomputing=False, default_dump=True, prefix=''):
            super(Selected,self).__init__(default_recomputing=default_recomputing, default_dump=default_dump,
                                           prefix=prefix)
            if columns is None:
                self.columns = list(range(FeatureObject.nfeat))
            else:
                if isinstance(columns,int):
                    self.columns = [columns]
                else:
                    self.columns = columns
            self.nfeat = len(self.columns)

        def get_name(self):
            return "selected{}-".format("-".join(list(map(str,self.columns))))+FeatureObject.get_name()

        def get_feature_names(self):
            original_feature_names = FeatureObject.get_feature_names()
            return [original_feature_names[col] for col in self.columns]

        def compute(self,Graph):
            result_origin  = FeatureObject.apply(Graph)
            result_local = np.zeros((result_origin.shape[0],self.nfeat))
            for i,col in enumerate(self.columns):
                result_local[:,i]=  result_origin[:,col]
            return result_local
    return Selected
