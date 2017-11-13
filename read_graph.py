from tqdm import tqdm
import networkx as nx


def read_graph(file_name = "data/9606.protein.links.v10.5.paj",directed = True):
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    nodes_names=dict()

    with open(file_name,'r') as f:
        header1 = f.readline().strip().lstrip("*Vertices ")
        print("Reading Nodes list")
        n_nodes = int(header1)
        for _ in tqdm(range(n_nodes)):
            line = f.readline()
            node_id,node_name = line.strip().split()
            node_id =int(node_id)
            G.add_node(node_id, name=node_name)
            nodes_names[node_id]=node_name

        header2 = f.readline()
        print("Reading Edges list")
        for line in f:
            start_node, end_node,wght = line.strip().split()
            G.add_edge(int(start_node),int(end_node),weight = float(wght))
        f.close()  # with open(...) does it already

    return G,nodes_names
