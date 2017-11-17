import numpy as np

class Pipeline:
    '''
    Implement the general form of a Pipeline.
    '''
    def __init__(self,*featGenList):
        self.generators = featGenList
        self.generator_names = [g.get_name() for g in self.generators]
        self.nfeat = sum([g.nfeat for g in self.generators])

    def get_generator_names():
        return self.generator_names

    def apply(self,Graph,verbose = False):
        n = Graph.number_of_nodes()
        result = np.zeros((n, self.nfeat))
        current = 0
        for g in self.generators:
            g_res = g.apply(Graph)
            if verbose:
                print(g.get_name())
            result[:,current:(current+g.nfeat)] = np.reshape(g_res, (n, g.nfeat))
            current += g.nfeat
        return result
