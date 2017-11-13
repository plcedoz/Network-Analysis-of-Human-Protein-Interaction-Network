import networkx as nx
import sys


def usage():
    print("{} [graph_file]".format(sys.argv[0]))


if __name__=='__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    file_name = sys.argv[1]
    print("loading graph...")
    Graph = nx.read_pajek(file_name)
    print("graph loaded\n\t{} nodes\n\t{} edges".format(
        Graph.number_of_nodes(),
        Graph.number_of_edges()
        ))
