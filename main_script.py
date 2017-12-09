# This script contains everything the whole sequence of things to do
# to get our results.

import networkx as nx

from read_graph import read_graph
from common.pipeline import Pipeline
from common.feature_generators import ExpectedDegree
from common.feature_generators import ClusteringCoefficient
from common.feature_generators import Degree
from common.feature_generators import ClosenessCentrality
from common.feature_generators import BetweennessCentrality
from common.feature_generators import HITS
from common.feature_generators import PageRank
from common.feature_generators import Log10Wrapper
from common.feature_generators import NormalizeWrapper
from common.feature_generators import NeighbouringConductance
from common.feature_generators import FeatureSelector
from common.feature_generators import ExternalFeature
from validation import compute_correlations
from prediction import get_labels, train_model, get_metrics


# Loading PPI graph
print("\n######### Loading Graph #########")
Graph = read_graph(directed=False)
print("Loaded graph:\n\t{} nodes\n\t{} edges".format(
    Graph.number_of_nodes(),
    Graph.number_of_edges()
))

#########################
# Computing node features
#########################

print("\n######### Computing/retrieving node features #########")

# The pipeline object takes as an argument the sequence of feature generator objects we want
pipeline = Pipeline(Log10Wrapper(Degree(default_dump=True, default_recomputing=False))(),
                    Log10Wrapper(ExpectedDegree(default_dump=True, default_recomputing=False))(),
                    ClusteringCoefficient(),
                    ClosenessCentrality(),
                    BetweennessCentrality(),
                    FeatureSelector(HITS())(columns=1),
                    PageRank(),
                    NeighbouringConductance(range=2),
                    NeighbouringConductance(range=3),
                    ExternalFeature(source_file="ppi_32dimq05.emb", name="PPINode2vec"))

features, node_names = pipeline.apply(Graph, verbose=True)

#########################
# Class prediction
#########################

print("\n######### Class Prediction #########")

sources = ["mendelian", "cancer", "drugbank"]

for source in sources:
    labels = get_labels(node_names)
    y_test, y_pred, y_score = train_model(features, labels, source)
    get_metrics(y_test, y_pred, y_score, source)

#########################
# Features Correlation
#########################

print("\n######### Features Correlation #########")

pvalues = compute_correlations(features, sources)

# Perform gene set enrichment analysis (GSEA) on a variety of gene sets directories
gene_sets_directories = [
    u'Cancer_Cell_Line_Encyclopedia',
    u'ChEA_2016',
    u'DrugMatrix',
    u'GeneSigDB',
    u'KEGG_2016',
    u'LINCS_L1000_Chem_Pert_down',
    u'LINCS_L1000_Chem_Pert_up',
    u'MSigDB_Computational',
    u'MSigDB_Oncogenic_Signatures',
    u'OMIM_Disease',
    u'OMIM_Expanded',
    u'PPI_Hub_Proteins',
    u'Panther_2016',
    u'Reactome_2016'
]
# enrichr = enrichr_validation(gene_query, gene_rank=None, outdir="validation_results", gene_sets='KEGG_2016')
# prerank = prerank_validation(gene_query, gene_rank, outdir="validation_results", gene_sets='KEGG_2016')

