"""
Author: Tomas Jelinek
Last change: 14.9.2019

Description: Tests for the bipartite_matching_augmentation(G, M) function
"""
import networkx as nx
from Algo.BipartiteMatchingAugmentation import bipartite_matching_augmentation
from Utils.AuxiliaryAlgorithms import get_sources_sinks_isolated
from nose.tools import assert_true, assert_equal
from typing import Set, Dict


def D_to_bipartite(D: nx.DiGraph) -> (nx.Graph, Set):
    M = default_matching_from_D(D)
    G = nx.Graph()
    G.add_edges_from(set(map(lambda e: (e[1], M[e[0]]), D.edges)))
    G.add_edges_from(set(map(lambda k: (k, M[k]), M)))
    return G, set(D.nodes)


def bipartite_to_D(G: nx.Graph, A: Set) -> nx.DiGraph:
    D: nx.DiGraph = nx.DiGraph()
    M: Dict = nx.algorithms.bipartite.eppstein_matching(G, A)

    for u in M:  # Construction of D, iterate over all keys in M
        if u in A:  # Add all edges from A to D
            w = M[u]
            D.add_node(u)

            for uPrime in G.neighbors(w):  # Construct edges of D
                if uPrime != u:
                    D.add_edge(u, uPrime)
    return D


def is_correctly_augmented(G: nx.Graph, A: Set, L=None) -> bool:
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


def default_matching_from_D(D: nx.DiGraph):
    """ Returns a perfect matching of a bipartite graph G that corresponds to D

    Parameters
    ----------
    D : NetworkX DiGraph
       An arbitrary directed graph. Assumes that the vertices are positive integers between 1 to n

    Returns
    -------
    Dict
        A dictionary of a perfect matching on G, where vertices from the upper bipartition are
        inversions of the original integers with regard to addition (negative integers).

    Notes
    -----
    Makes use of the observation that there is an isomorphism between each D that
    is constructed with regard to a different perfect matching.
    """
    edges = {}
    for v in D.nodes:
        edges[v] = (-1) * v
        edges[(-1) * v] = v

    return edges


class TestEswaranTarjan:
    """
    def test_unaugmentable(self):
        # Testing on the only two cases when the bipartite graph cannot be augmented.
        # This happens when it consists only of two vertices, connected or disconnected
        G: nx.Graph = nx.Graph()
        G.add_nodes_from({0,1})
        assert_raises(BipartiteGraphNotAugmentableException, bipartite_matching_augmentation, G, {0})

        G.add_edge(0,1)
        assert_raises(BipartiteGraphNotAugmentableException, bipartite_matching_augmentation, G, {0})

    def test_simple_already_robust(self):
        # Test a simple graph that is already robust
        G: nx.Graph = nx.Graph()
        G.add_edges_from({(0,1), (0,3), (2,1), (2,3)})
        assert_set_equal(bipartite_matching_augmentation(G, {0,2}), set())

    def test_simple_needs_to_be_augmented(self):
        # Tests a simple graph that admits a perfect matching and needs to be augmented
        G: nx.Graph = nx.Graph()
        G.add_edges_from({(0, 1), (2, 3)})
        assert_set_equal(bipartite_matching_augmentation(G, {0, 2}), {(0, 3), (2, 1)})

        G.add_edge(0, 3)
        assert_set_equal(bipartite_matching_augmentation(G, {0, 2}), {(2, 1)})

    def test_more_strong_components(self):
        D: nx.DiGraph = nx.DiGraph()
        nx.add_cycle(D, {1, 2})
        nx.add_cycle(D, {3, 4})
        G, A = D_to_bipartite(D)
        assert_true(is_correctly_augmented(G, A))
        assert_set_equal(bipartite_matching_augmentation(G, A), set())
        nx.add_cycle(D, {5, 6, 7})
        G, A = D_to_bipartite(D)
        assert_true(is_correctly_augmented(G, A))
        assert_set_equal(bipartite_matching_augmentation(G, A), set())

    def test_strong_components_and_critical_vert(self):
        D: nx.DiGraph = nx.DiGraph()
        nx.add_cycle(D, {1, 2, 3})
        D.add_node(4)
        G, A = D_to_bipartite(D)
        L = bipartite_matching_augmentation(G, A)
        assert_equal(len(L), 2)
        assert_true(is_correctly_augmented(G, A))

        nx.add_cycle(D, {5, 6})
        L = bipartite_matching_augmentation(G, A)
        assert_equal(len(L), 2)
        assert_true(is_correctly_augmented(G, A))

    def test_strong_components_and_critical_verts(self):
        D: nx.DiGraph = nx.DiGraph()
        nx.add_cycle(D, {1, 2, 3})
        nx.add_cycle(D, {4, 5})
        D.add_edge(1, 4)
        D.add_nodes_from({i for i in range(6, 10)})
        D.add_edge(5, 8)
        D.add_edge(9, 4)
        G, A = D_to_bipartite(D)

        L = bipartite_matching_augmentation(G, A)
        assert_equal(len(L), 4)
        assert_true(is_correctly_augmented(G, A))
    """

    def test_only_critical(self):
        D: nx.DiGraph = nx.DiGraph()
        nx.add_star(D, {i for i in range(1, 5)})
        nx.add_path(D, {i for i in range(5, 10)})
        D.add_nodes_from({i for i in range(10, 20)})
        """
        G, A = D_to_bipartite(D)
        assert_true(is_correctly_augmented(G, A))
        sources, sinks, isolated = get_sources_sinks_isolated(D)
        s, t, q = len(sources), len(sinks), len(isolated)
        L = bipartite_matching_augmentation(G, A)
        assert_equal(len(L), max(s, t) + q)
        """
        D.clear()
        D = nx.balanced_tree(2, 13, nx.DiGraph())
        D.remove_node(0)
        G, A = D_to_bipartite(D)
        sources, sinks, isolated = get_sources_sinks_isolated(D)
        s, t, q = len(sources), len(sinks), len(isolated)
        L = bipartite_matching_augmentation(G, A)
        assert_true(is_correctly_augmented(G, A, L))
        assert_equal(len(L), max(s, t) + q)

    def test_set_coverage(self):
        pass
