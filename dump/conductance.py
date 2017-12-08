import networkx as nx

from read_graph import read_graph
from common.pipeline import Pipeline
from common.feature_generators import *

# Loading PPI graph
Graph = read_graph(directed=False, threshold = 600)

pipeline = Pipeline(NeighbouringConductance(range=3))
_ = pipeline.apply(Graph)
