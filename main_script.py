# This script contains everything the whole sequence of things to do
# to get our results.

import networkx as nx

from read_graph import read_graph
from common.pipeline import Pipeline
from common.feature_generators import *
from validation import *
from validation_datasets import *
from GSEA_validation import *

# Loading PPI graph
Graph, node_names = read_graph(directed=False)
print("Loaded graph:\n\t{} nodes\n\t{} edges".format(
    Graph.number_of_nodes(),
    Graph.number_of_edges()
    ))

#########################
# Computing node features
#########################

# The pipeline object takes as an argument the sequence of features we want
pipeline = Pipeline(Degree(default_dump=True,default_recomputing=False), ExpectedDegree())
features = pipeline.apply(Graph, verbose=True)


#########################
# Learning
#########################

gene_query, gene_rank = get_query_and_rank(features, node_names, index=0)

#########################
# Validation
#########################

#Perform gene set enrichment analysis (GSEA) on a variety of gene sets directories
gene_sets_directories = [u'Cancer_Cell_Line_Encyclopedia', u'ChEA_2016', u'DrugMatrix', u'GeneSigDB', u'KEGG_2016', u'LINCS_L1000_Chem_Pert_down', u'LINCS_L1000_Chem_Pert_up', u'MSigDB_Computational', u'MSigDB_Oncogenic_Signatures', u'OMIM_Disease', u'OMIM_Expanded', u'PPI_Hub_Proteins', u'Panther_2016', u'Reactome_2016']
enrichr = enrichr_validation(gene_query, gene_rank=None, outdir="validation_results", gene_sets='KEGG_2016')
prerank = prerank_validation(gene_query, gene_rank, outdir="validation_results", gene_sets='KEGG_2016')

#Extract relevant gene lists

gene_ref = get_gene_ref(source="cancer")

compare_gene_lists(gene_query, gene_rank, gene_ref)

