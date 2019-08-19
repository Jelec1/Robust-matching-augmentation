import networkx as nx
from Algo.BipartiteMatchingAugmentation import augmentGraph


B = nx.Graph()
B.add_edge(0, 1)

print(augmentGraph(B, {(0, 1)}))