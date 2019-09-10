import networkx as nx
from Algo.BipartiteMatchingAugmentation import sourceCover
import random
import time

for i in range(1):
    start = time.time()
    G: nx.DiGraph = nx.generators.classic.balanced_tree(2, 16, create_using=nx.DiGraph)
    print(time.time() - start)
    # G = nx.algorithms.traversal.dfs_tree(G, 0)
    sources = set()
    a = len(G)

    print("DFS------")
    start = time.time()
    nx.algorithms.traversal.dfs_tree(G, 0)
    print(time.time() - start)
    print("DFS------")

    for i in range(len(G) + 1, len(G) + 1 + 100):
        j = random.randint(1, a - 1)
        G.add_edge(i, j)
        sources.add(i)
    start = time.time()
    torem = set()
    for n in G:
        r = random.randint(0, 100)
        if r <= 1:
            torem.add(n)
    G.remove_nodes_from(torem)
    for u in range(1, 100):
        p = r = random.randint(0, len(G) - 10)
        s = r = random.randint(p + 1, len(G) - 1)
        G.add_edge(p, s)
    print(len(G))
    res = sourceCover(G, {n for n in G if G.in_degree(n) == 0}, {n for n in G if G.out_degree(n) == 0})
    print(time.time() - start)

    print(res)
    print("---------------------")
