import numpy as np
import pandas as pd

class Pipeline:
    '''
    Implement the general form of a Pipeline.
    '''
    def __init__(self,*featGenList):
        self.generators = featGenList
        self.generator_names = []
        for g in self.generators:
            if g.get_name()[-4:] == "hits":
                self.generator_names.append(g.get_name() + "_hubs")
                self.generator_names.append(g.get_name() + "_authorities")
            else:
                self.generator_names.append(g.get_name())
        self.nfeat = sum([g.nfeat for g in self.generators])

    def get_generator_names(self):
        return self.generator_names

    def apply(self,Graph,verbose = False):
        n = Graph.number_of_nodes()
        node_names = [Graph.nodes[i]['name'] for i in range(n)]
        features = pd.DataFrame(data=np.zeros((n, self.nfeat)), index=node_names, columns=self.generator_names)
        current = 0
        for g in self.generators:
            g_res = g.apply(Graph)
            if verbose:
                print(g.get_name())
            features.iloc[:,current:(current+g.nfeat)] = np.reshape(g_res, (n, g.nfeat))
            current += g.nfeat
        features = filter_genes(features)
        node_names = list(features.index)
        
        return features, node_names

    
def filter_genes(features, mapping_file="validation_datasets/entrez_to_ENSP_to_symbols.csv"):    
    
    mapping = pd.read_csv(mapping_file)
    string_to_symbol = {}
    for i in range(len(mapping)):
        string_to_symbol[str(mapping.iloc[i,2])] = str(mapping.iloc[i,3])
    indices = [gene for gene in features.index.values if gene in list(string_to_symbol.keys())]
    features = features.loc[indices,:]
    features = features.rename(index=string_to_symbol)
    
    return features



    
    