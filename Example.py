"""
Author: Tomas Jelinek
Last change: 13.12.2019

Description: An example of the usage of the algorithm.
"""
import networkx as nx
from src.algo.BipartiteMatchingAugmentation import bipartite_matching_augmentation
from src.utils.AuxiliaryFunctions import D_to_bipartite
from typing import Set


# Graph from Figue 2.1
def example1():
    A: Set = set()
    num_of_gadgets = 2

    G: nx.Graph = nx.Graph()
    for i in range(1, num_of_gadgets + 2):
        u1 = 's_' + str(2 * i)
        v1 = 's\'_' + str(2 * i)
        u2 = 's_' + str(2 * i - 1)
        v2 = 's\'_' + str(2 * i - 1)
        G.add_edge(u1, v1)
        G.add_edge(u2, v2)
        G.add_edge(u1, v2)
        G.add_edge(u2, v1)
        G.add_edge(v2, 't_1')
        A.add(u1)
        A.add(u2)

    G.add_edge('t_1', 't\'_1')
    A.add('t_1')

    for i in range(1, num_of_gadgets + 1):
        us = ['t_' + str(4 * i + j) for j in range(-2, 2)]
        vs = ['t\'_' + str(4 * i + j) for j in range(-2, 2)]

        G.add_edges_from([(us[j], vs[j]) for j in range(len(us))])
        G.add_edges_from([(us[2 * j], vs[2 * j + 1]) for j in range(len(us) // 2)])
        G.add_edges_from([(us[2 * j + 1], vs[2 * j]) for j in range(len(us) // 2)])
        G.add_edge('t_' + str(4 * i - 1), 's\'_' + str(2 * i + 1))
        G.add_edge('t_' + str(4 * i + 1), 's\'_' + str(2 * i + 2))
        A = A | set(us)

    L = bipartite_matching_augmentation(G, A)
    print(L)


# Random graph
def example2():
    D: nx.DiGraph = nx.generators.random_graphs.erdos_renyi_graph(10, 0.5, directed=True)
    D.remove_node(0)
    D.remove_edges_from([(u, v) for (u, v) in D.edges() if u < v])
    G, A, M = D_to_bipartite(D)
    L = bipartite_matching_augmentation(G, A)
    print(L)


print("Ahoj")
example1()

example2()