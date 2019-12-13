"""
Author: Tomas Jelinek
Last change: 30.11.2019

Description: tests for the bipartite_matching_augmentation(G, M) function
"""

import networkx as nx
from src.algo.BipartiteMatchingAugmentation import bipartite_matching_augmentation
from src.utils.AuxiliaryFunctions import bipartite_to_D, get_sources_sinks_isolated, D_to_bipartite
from src.exceptions.Exceptions import bipartite_ghraph_not_augmentable_exception
from nose.tools import assert_true, assert_raises, assert_set_equal, assert_equal
from typing import Set


def is_correctly_augmented(G: nx.Graph, A: Set, L: Set = None) -> bool:
    """ Returns a perfect matching of a bipartite graph G that corresponds to D

    Parameters
    ----------
    G : NetworkX Graph
       A bipartite graph.
    A : Set
        A bipartition of G.
    L : Set
        To-be proved augmenting set of G. Optional, computed otherwise.

    Returns
    -------
    bool
        True if G is correctly augmented, i.e. in underlying digraph D,
        each strong component is non-trivial.

    Notes
    -----
    Makes use of the observation that if each vertex in G lies on M-augmenting cycle,
    then G is robust against edge-failure. However, this function does not check optimality of L.
    """

    if L is None:
        L = bipartite_matching_augmentation(G, A)
    G.add_edges_from(L)

    D = bipartite_to_D(G, A)
    C_D = nx.algorithms.condensation(D)
    result: bool = True

    for v in C_D.nodes:
        result &= len(C_D.nodes[v]['members']) > 1

    G.remove_edges_from(L)

    return result


class TestBipartiteMatchingAugmentation:

    def test_unaugmentable(self):
        # Testing on the only two cases when the bipartite graph cannot be augmented.
        # This happens when it consists only of two vertices, connected or disconnected
        G: nx.Graph = nx.Graph()
        G.add_nodes_from({0, 1})
        assert_raises(bipartite_ghraph_not_augmentable_exception, bipartite_matching_augmentation, G, {0})

        G.add_edge(0, 1)
        assert_raises(bipartite_ghraph_not_augmentable_exception, bipartite_matching_augmentation, G, {0})

    def test_simple_already_robust(self):
        # Test a simple graph that is already robust
        G: nx.Graph = nx.Graph()
        G.add_edges_from({(0, 1), (0, 3), (2, 1), (2, 3)})
        assert_set_equal(bipartite_matching_augmentation(G, {0, 2}), set())

    def test_simple_needs_to_be_augmented(self):
        # tests a simple graph that admits a perfect matching and needs to be augmented
        G: nx.Graph = nx.Graph()
        G.add_edges_from({(0, 1), (2, 3)})
        assert_set_equal(bipartite_matching_augmentation(G, {0, 2}), {(0, 3), (2, 1)})

        G.add_edge(0, 3)
        assert_set_equal(bipartite_matching_augmentation(G, {0, 2}), {(2, 1)})

    def test_more_strong_components(self):
        # tests more strong connected component, no augmentation is required
        D: nx.DiGraph = nx.DiGraph()
        nx.add_cycle(D, {1, 2})
        nx.add_cycle(D, {3, 4})
        G, A, M = D_to_bipartite(D)
        assert_true(is_correctly_augmented(G, A))
        assert_set_equal(bipartite_matching_augmentation(G, A), set())
        nx.add_cycle(D, {5, 6, 7})
        G, A, M = D_to_bipartite(D)
        L: Set = bipartite_matching_augmentation(G, A)
        assert_true(is_correctly_augmented(G, A, L))
        assert_set_equal(L, set())

    def test_strong_components_and_critical_vert(self):
        # Testing corner case when there are more strongly
        # connected components and a single critical vertex.
        # Expected the algorithm strongly connects the critical
        # vertex to one of the strongly connected components.
        D: nx.DiGraph = nx.DiGraph()
        nx.add_cycle(D, {1, 2, 3})
        D.add_node(4)
        G, A, M = D_to_bipartite(D)
        L = bipartite_matching_augmentation(G, A)
        assert_equal(len(L), 2)
        assert_true(is_correctly_augmented(G, A))

        nx.add_cycle(D, {5, 6})
        L = bipartite_matching_augmentation(G, A)
        assert_equal(len(L), 2)
        assert_true(is_correctly_augmented(G, A))

    def test_strong_components_and_critical_vertices(self):
        # Special instance of a graph where there are strong components
        # and several critical vertices connected to them. Correct solution
        # manually checked.
        D: nx.DiGraph = nx.DiGraph()
        nx.add_cycle(D, {1, 2, 3})
        nx.add_cycle(D, {4, 5})
        D.add_edge(1, 4)
        D.add_nodes_from({i for i in range(6, 10)})
        D.add_edge(5, 8)
        D.add_edge(9, 4)
        G, A, M = D_to_bipartite(D)

        L = bipartite_matching_augmentation(G, A)
        assert_equal(len(L), 3)
        assert_true(is_correctly_augmented(G, A, L))

    def test_only_critical(self):
        # tests only critical vertices in form of trees, paths and stars,
        # expected the algorithm correctly augments G and the augmenting set
        # cardinality correspond the simple bound on Eswaran-Tarjan.
        D: nx.DiGraph = nx.DiGraph()

        nx.add_star(D, {i for i in range(1, 5)})
        nx.add_path(D, {i for i in range(5, 10)})
        D.add_nodes_from({i for i in range(10, 20)})

        G, A, M = D_to_bipartite(D)
        assert_true(is_correctly_augmented(G, A))
        sources, sinks, isolated = get_sources_sinks_isolated(D)
        s, t, q = len(sources), len(sinks), len(isolated)
        L = bipartite_matching_augmentation(G, A)
        assert_equal(len(L), max(s, t) + q)

        D.clear()
        D = nx.balanced_tree(2, 13, nx.DiGraph())
        D.remove_node(0)
        G, A, M = D_to_bipartite(D)
        sources, sinks, isolated = get_sources_sinks_isolated(D)
        s, t, q = len(sources), len(sinks), len(isolated)
        for i in range(1):
            L = bipartite_matching_augmentation(G, A)
        assert_true(is_correctly_augmented(G, A, L))
        assert_equal(len(L), max(s, t) + q)

    def test_bounded_approximation(self):
        # Test for unbounded approximation factor as discussed
        # in section 2.1 the thesis. The optimal solution is 1. The variable
        # num_of_gadgets allows to set the number of vertices s_2, ... with its children
        # to be added to the graph.
        # Expected source cover is of length 1 if it works correctly.

        A: Set = set()
        num_of_gadgets = 5000

        G: nx.Graph = nx.Graph()
        for i in range(1, num_of_gadgets + 2):
            u1 = 's_' + str(2*i)
            v1 = 's\'_' + str(2*i)
            u2 = 's_' + str(2*i-1)
            v2 = 's\'_' + str(2*i-1)
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
            us = ['t_' + str(4*i + j) for j in range(-2, 2)]
            vs = ['t\'_' + str(4 * i + j) for j in range(-2, 2)]

            G.add_edges_from([(us[j], vs[j]) for j in range(len(us))])
            G.add_edges_from([(us[2*j], vs[2*j+1]) for j in range(len(us) // 2)])
            G.add_edges_from([(us[2 * j + 1], vs[2 * j]) for j in range(len(us) // 2)])
            G.add_edge('t_' + str(4*i - 1), 's\'_' + str(2*i+1))
            G.add_edge('t_' + str(4 * i + 1), 's\'_' + str(2 * i + 2))
            A = A | set(us)

        L = bipartite_matching_augmentation(G, A)

        assert_true(is_correctly_augmented(G, A, L))
        assert_true(len(L) == 1)

    def test_random_graph(self):
        # tests 10 random graphs, which must be very sparse due to time complexity
        # Also test the approximation factor log(n)

        for i in range(10):
            D: nx.DiGraph = nx.generators.random_graphs.erdos_renyi_graph(10000, 0.001, directed=True)
            D.remove_node(0)
            D.remove_edges_from([(u, v) for (u, v) in D.edges() if u < v])
            G, A, M = D_to_bipartite(D)
            L = bipartite_matching_augmentation(G, A)
            assert_true(is_correctly_augmented(G, A, L))



