import numpy as np
import pandas as pd
import gseapy as gp
import math
from scipy.stats import hypergeom


def get_query_and_rank(features, node_names, index=0, mapping_file="validation_datasets/entrez_to_ENSP_to_symbols.csv"):
    """
    Converts the features to a gene list with their ranks
    
    Args:
        -features: Array of features.
        -node_names: List of node names.
        -index: Index of the feature column.
        -mapping_file: Location of the mapping file.

    """
    scores = features[:,index]
    gene_query_Id = np.array(node_names.keys())[scores.argsort()[::-1]].tolist()
    gene_query = np.array(node_names.values())[scores.argsort()[::-1]].tolist()
    gene_rank = scores.copy()
    gene_rank.sort()
    gene_rank = gene_rank[::-1].tolist()
    
    mapping = pd.read_csv(mapping_file)
    string_to_symbol = {}
    for i in range(len(mapping)):
        string_to_symbol[str(mapping.iloc[i,2])] = str(mapping.iloc[i,3])
    gene_rank = [gene for i,gene in enumerate(gene_rank) if gene_query[i] in string_to_symbol.keys()]
    gene_query = [string_to_symbol[gene] for gene in gene_query if gene in string_to_symbol.keys()]
    
    return gene_query, gene_rank


def compare_gene_lists(gene_query, gene_rank, gene_ref):
    
    N = len(gene_query)
    n = 100
    M = len(list(set(gene_query) & set(gene_ref)))
    m = len(list(set(gene_query[0:n]) & set(gene_ref)))
    print N,n,M,m
    
    pass
    #hypergeometric test?
    #Proportion of indispensable vs neutral vs dispensables in the ref_gene_list
    
    
    