# This script contains everything the whole sequence of things to do
# to get our results.

import networkx as nx

from read_graph import read_graph
from common.pipeline import Pipeline
from common.feature_generators import *

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

gene_query, gene_rank = [], []

#If we pick the score to be the degree:
scores = features[:,0]
gene_query_Id = np.array(node_names.keys())[scores.argsort()[::-1]].tolist()
gene_query = np.array(node_names.values())[scores.argsort()[::-1]].tolist()
gene_rank = scores.copy()
gene_rank.sort()
gene_rank = gene_rank[::-1].tolist()


#########################
# Validation
#########################

#Perform gene set enrichment analysis (GSEA) on a variety of gene sets directories
gene_sets_directories = [u'Cancer_Cell_Line_Encyclopedia', u'ChEA_2016', u'DrugMatrix', u'GeneSigDB', u'KEGG_2016', u'LINCS_L1000_Chem_Pert_down', u'LINCS_L1000_Chem_Pert_up', u'MSigDB_Computational', u'MSigDB_Oncogenic_Signatures', u'OMIM_Disease', u'OMIM_Expanded', u'PPI_Hub_Proteins', u'Panther_2016', u'Reactome_2016']
enrichr = enrichr_validation(gene_query, gene_rank=None, outdir="validation_results", gene_sets='KEGG_2016')
prerank = prerank_validation(gene_query, gene_rank, outdir="validation_results", gene_sets='KEGG_2016')

#Extract relevant gene lists
cancer = get_cancer()
mendelian = get_mendelian()
drugbank_target_all = get_drugbank(molecule_type="target", subset="all")
drugbank_target_approved = get_drugbank(molecule_type="target", subset="approved")
drugbank_enzyme_all = get_drugbank(molecule_type="enzyme", subset="all")
drugbank_enzyme_approved = get_drugbank(molecule_type="enzyme", subset="approved")
drugbank_carrier_all = get_drugbank(molecule_type="carrier", subset="all")
drugbank_carrier_approved = get_drugbank(molecule_type="carrier", subset="approved")
drugbank_transporter_all = get_drugbank(molecule_type="transporter", subset="all")
drugbank_transporter_approved = get_drugbank(molecule_type="transporter", subset="approved")

gene_ref_formatted = [gene[4:] for gene in cancer['gene_string']]
gene_query_formatted = [gene[9:] for gene in gene_query]

compare_gene_lists(gene_query_formatted, gene_ref_formatted)


