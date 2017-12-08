import numpy as np
import pandas as pd
import gseapy as gp
import math
import matplotlib.pyplot as plt
import scipy.stats as ss

from scipy.stats import hypergeom
from validation_import import get_ref_genes


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
    pvalue = ss.mannwhitneyu(sample_scores, ref_scores).pvalue
    return pvalue

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
    pvalue = hypergeom.sf(k, M, n, N, loc=0)
    return pvalue


def compute_correlations(features, sources):

    print ("Computing correlations/pvalues for all features for different sources\n")
    feature_names = list(features.columns)
    pvalues = pd.DataFrame(data=np.zeros((6,len(feature_names))), index=["cancer_Mann–Whitney", "drugbank_Mann–Whitney",
                                                                         "mendelian_Mann–Whitney", "cancer_hypergeom",
                                                                         "drugbank_hypergeom", "mendelian_hypergeom"],
                           columns = feature_names)
    for source in sources:
        print("Source = %s"%source)
        ref_genes = get_ref_genes(source=source)
        for feature_name in feature_names:
            pvalue_MW = compare_feature_distribution_mannwhitney(features, feature_name, ref_genes, 'output/' + feature_name +
                                                                 '_distribution_comparison_{}.png'.format(source),
                                                                 title="{},{}".format(feature_name, source))
            pvalue_hypergeom = compare_feature_distribution_hypergeom(features, feature_name, ref_genes)
            pvalues.loc["%s_Mann–Whitney"%source:,feature_name] = pvalue_MW
            pvalues.loc["%s_hypergeom"%source:,feature_name] = pvalue_hypergeom
            print ("pvalue Mann-Whitney = %.2g \t pvalue hypergeometric = %.2g \t(%s)"%(pvalue_MW, pvalue_hypergeom,
                                                                                        feature_name))
        print("############\n")
    print ("Saving pvalues to output/pvalues")
    pvalues.to_pickle("output/pvalues")
    
    return pvalues


