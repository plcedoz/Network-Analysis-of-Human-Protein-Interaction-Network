import numpy as np
import pandas as pd
import gseapy as gp
import math
import matplotlib.pyplot as plt

import scipy.stats as ss

from scipy.stats import hypergeom

def get_genes_scores(features, feature_name, ref_genes):
    
    feature = features.loc[:,feature_name].copy()
    indices = np.argsort(feature.values)[::-1]
    sample_genes = list(feature[indices].index)
    sample_scores = list(feature[indices].values)   
    ref_scores = feature[ref_genes].values
    ref_scores = list(ref_scores[np.isnan(ref_scores) == False])
    return sample_genes, sample_scores, ref_scores
    
def compare_feature_distribution_mannwhitney(features, feature_name, ref_genes, output_file, title="Feature distribution"):

    sample_genes, sample_scores, ref_scores = get_genes_scores(features, feature_name, ref_genes)
    
    bins = np.linspace(np.min(sample_scores), np.max(sample_scores), 100)
    plt.hist(sample_scores, bins, alpha=0.5, label='all', normed=True)
    plt.hist(ref_scores, bins, alpha=0.5, label='ref', normed=True)
    plt.title(title)
    plt.legend()
    plt.savefig(output_file)
    plt.close()

    return ss.mannwhitneyu(sample_scores, ref_scores)

def compare_feature_distribution_hypergeom(features, feature_name, ref_genes, N=100):
    """
        k: Intersection with gene_ref within the cluster
        M: Size of the gene query
        n: Intersection with gene_ref in total
        N: Size of the cluster
    """
    sample_genes, sample_scores, ref_scores = get_genes_scores(features, feature_name, ref_genes)
    
    k = len(list(set(sample_genes[0:N]) & set(ref_genes)))
    M = len(sample_genes)
    n = len(list(set(sample_genes) & set(ref_genes)))
    p_value = hypergeom.sf(k, M, n, N, loc=0)
    return p_value
