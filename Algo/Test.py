import networkx as nx
from Algo.BipartiteMatchingAugmentation import augmentGraph




G = nx.Graph()
G.add_edges_from({(0,1), (2,3)})


A = set()
A.update({1,2,3})
augmentGraph(G, {0, 2})
