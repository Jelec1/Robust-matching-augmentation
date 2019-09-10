import networkx as nx
from Algo.BipartiteMatchingAugmentation import bipartite_matching_augmentation
import random


B = nx.Graph()
B.add_edge(0, 1)
B.add_edge(2, 3)
#B.add_edge(0, 3)
#B.add_edge(2, 1)
B.add_edge(4, 5)
#B.add_edge(0, 5)

print(bipartite_matching_augmentation(B, {0, 2, 4}))

