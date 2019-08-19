import networkx as nx
from Algo.BipartiteMatchingAugmentation import augmentGraph



a = {1,2,0}

a.remove(0)





G = nx.Graph()


U = [i for i in range(6)]
W = [i for i in range(5, 11)]

G.add_nodes_from(U + W)

#matching = [(i, i+5) for i in range(5)]
matching = [(0,2), (1,3)]

G.add_edges_from(matching)

match = {}
for e in matching:
    match[e[0]] = e[1]

augmentGraph(G, matching)
