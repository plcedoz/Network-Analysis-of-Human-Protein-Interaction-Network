import numpy as np
import pandas as pd
import gseapy as gp


def enrichr_validation(gene_list, gene_rank=None, outdir="validation_results", gene_sets='KEGG_2016'):
    """
    Perform the enrichr tool (http://amp.pharm.mssm.edu/Enrichr/)
    Enrichment of a gene list
    
    Args:
        -gene_list (list): Gene list to analyze
        -gene_rank (list): Ranking of the genes (according to a scoring function)
        -outdir (str): Location to save the files
        -gene_sets (str): Gene set to use for the enrichment
    
    """
    if gene_rank == None:
        enr = gp.enrichr(gene_list=gene_list, description='pathway', gene_sets='KEGG_2016', outdir='test',
                         cutoff=0.05, format='png')
    else:
        assert type(gene_rank)==list, "please provide gene_rank as a list"
        rnk = pd.DataFrame(np.array([gene_list, gene_rank]).T, columns = ['gene', 'score'])
        enr = gp.enrichr(gene_list=rnk, description='pathway', gene_sets='KEGG_2016', outdir=outdir, cutoff=0.05, format='png')
    #result = enr.res2d[enr.res2d["Adjusted P-value"]<pvalue]
    
    return result


def prerank_validation(gene_list, gene_rank, outdir="validation_results", gene_sets='KEGG_2016'):
    """
    Perform the prerank tool (http://software.broadinstitute.org/cancer/software/genepattern/modules/docs/GSEAPreranked/1)
    Enrichment of a gene list
    
    Args:
        -gene_list (list): Gene list to analyze
        -gene_rank (list): Ranking of the genes (according to a scoring function)
        -outdir (str): Location to save the files
        -gene_sets (str): Gene set to use for the enrichment
    
    """
    rnk = pd.DataFrame(np.array([gene_list, gene_rank]).T, columns = ['gene', 'score'])
    prerank = gp.prerank(rnk=rnk, gene_sets=gene_sets, outdir=outdir,format='png')        
        
    return prerank.res2d
