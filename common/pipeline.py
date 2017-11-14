import numpy as np

class Pipeline:
    '''
    Implement the general form of a Pipeline.
    '''
    def __init__(self,*featGenList):
        self.generators = featGenList
        self.nfeat = sum([g.nfeat for g in self.generators])

    def apply(self,Graph,verbose = False):
        n = Graph.number_of_nodes()
        result = np.zeros((n, self.nfeat))
        current = 0
        for g in self.generators:
            g_res = g.apply(Graph)
            if verbose:
                print(g.get_name())
            result[n,current:(current+g.nfeat)] = g_res
            current += g.nfeat
        return result
