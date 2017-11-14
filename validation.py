import numpy as np
%matplotlib inline
import pandas as pd
import gseapy as gp
import matplotlib.pyplot as plt
import math
from scipy.stats import hypergeom


def enrichr_validation(gene_list, gene_rank=None, outdir="validation_results", gene_sets='KEGG_2016'):
    
    if gene_rank == None:
        enr = gp.enrichr(gene_list=gene_list, description='pathway', gene_sets='KEGG_2016', outdir='test',
                         cutoff=0.05, format='png')
    else:
        assert type(gene_rank)==list, "please provide gene_rank as a list"
        rnk = pd.DataFrame(np.array([gene_list, gene_rank]).T, columns = ['gene', 'score'])
        enr = gp.enrichr(gene_list=rnk, description='pathway', gene_sets='KEGG_2016', outdir=outdir, cutoff=0.05, format='png')

    return enr.res2d


def prerank_validation(gene_list, gene_rank, outdir="validation_results", gene_sets='KEGG_2016'):
    
    rnk = pd.DataFrame(np.array([gene_list, gene_rank]).T, columns = ['gene', 'score'])
    prerank = gp.prerank(rnk=rnk, gene_sets=gene_sets, outdir=outdir,format='png')        
        
    return prerank.res2d


def get_cancer_genes(filename="validation_datasets/cancer_gene_census.csv"):

    cancer_gene_census = pd.read_csv(filename)
    gene_symbols = cancer_gene_census.loc[:,"Gene Symbol"]
    gene_names = cancer_gene_census.loc[:,"Name"]
    gene_string = []
    list_of_synonyms = cancer_gene_census.loc[:,"Synonyms"]
    for synonyms in list_of_synonyms:
        if str(synonyms) != 'nan':        
            for synonym in synonyms.split(','):
                if synonym[:3] == "ENS":
                    gene_string.append(synonym)
    
    return gene_symbols, gene_names, gene_string


def get_mendelian_genes(filename="validation_datasets/mim2gene.txt"):
    
    gene_entrez = []
    gene_symbols = []
    gene_string = []
    with open(filename) as f:
        for line in f:
            if len(line.split('\t'))>1:
                if line.split('\t')[1] == "gene":
                    if len(line.split('\t'))>2:
                        gene_entrez.append(line.split('\t')[2])
                        gene_symbols.append(line.split('\t')[3])
                        gene_string.append(line.split('\t')[4])

    return gene_symbols, gene_entrez, gene_string


def compare_gene_lists(query_gene_list, ref_gene_list):
    pass
    #hypergeometric test?
    #Proportion of indispensable vs neutral vs dispensables in the ref_gene_list
    
    
    