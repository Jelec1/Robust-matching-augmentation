import networkx as nx
from Algo.BipartiteMatchingAugmentation import bipartite_matching_augmentation
import random


B = nx.Graph()
for i in range(5):
    B.add_edge(2*i, 2*i + 1)

print(bipartite_matching_augmentation(B, {2 * i for i in range(5)}))

