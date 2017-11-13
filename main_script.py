# This script contains everything the whole sequence of things to do
# to get our results.

import networkx as nx
from read_graph import read_graph

# Loading PPI graph
Graph, node_names = read_graph(directed=False)
print("Loaded graph:\n\t{} nodes\n\t{} edges".format(
    Graph.number_of_nodes(),
    Graph.number_of_edges()
    ))

# Computing node features
