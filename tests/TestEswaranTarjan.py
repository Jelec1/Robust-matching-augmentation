"""
Author: Tomas Jelinek
Last change: 8.9.2019

Description: tests for the eswaran_tarjan(G) function
"""

from nose.tools import assert_set_equal, assert_raises, assert_false, assert_true
import networkx as nx
from src.algo import EswaranTarjan
from src.utils.AuxiliaryFunctions import get_sources_sinks_isolated
from typing import Set


def arcs_for_augmentation(G: nx.DiGraph) -> int:
    """ Bounds the number of arcs needed to make G strongly connected

    Parameters
    ----------
    G : NetworkX DiGraph
       A directed graph.

    Returns
    -------
    ints
        A lower and an upper bound on the number of arcs needed to add to G
        to make G strongly connected
    Notes
    -----
    For upper and lower bound on augmenting arcs see
    Theorem 2 in Eswaran and Tarjan's algorithm https://epubs.siam.org/doi/abs/10.1137/0205044
    """
    G = nx.algorithms.condensation(G)

    sources, sinks, isolated = get_sources_sinks_isolated(G)
    s: int = len(sources)
    t: int = len(sinks)
    q: int = len(isolated)

    if s + t + q > 1:
        return max(s, t) + q
    else:  # obviously s > 0 iff t > 0, thus s == t == 0
        return 0


def is_correctly_augmented(G: nx.DiGraph()) -> bool:
    """Returns if eswaran_tarjan augments G and the augmenting set is minimal

    Parameters
    ----------
    G : NetworkX DiGraph
       A directed graph.

    Returns
    -------
    correct : bool
       True if eswaran_tarjan augments eswaran_tarjan and is a minimal such set
       according to the lower bound by Eswaran and Tarjan

    Notes
    -----
    For upper and lower bound see
    Theorem 2 in Eswaran and Tarjan's algorithm https://epubs.siam.org/doi/abs/10.1137/0205044
    """

    G = G.copy()
    A = EswaranTarjan.eswaran_tarjan(G)
    n = arcs_for_augmentation(G)
    G.add_edges_from(A)
    return nx.algorithms.is_strongly_connected(G) and (len(A) == n)


class TestEswaranTarjan:

    def test_directed(self):
        # Testing on directed graph, no exception expected
        exception = False
        try:
            EswaranTarjan.eswaran_tarjan(nx.DiGraph())
        except:
            exception = True
        assert_false(exception, "eswaran_tarjan should be implemented for networkx.DiGraph")

    def test_wrong_graph_type(self):
        # Testing on unsupported graph types, exception networkx.NetworkXNotImplemented expected
        assert_raises(nx.NetworkXNotImplemented, EswaranTarjan.eswaran_tarjan, nx.Graph())
        assert_raises(nx.NetworkXNotImplemented, EswaranTarjan.eswaran_tarjan, nx.MultiGraph())
        assert_raises(nx.NetworkXNotImplemented, EswaranTarjan.eswaran_tarjan, nx.MultiDiGraph())

    def test_output_format(self):
        # tests the type of the output on an elementary case. Expected a set of tuples of
        # length 2. We only test the most trivial case in so as not to depend
        # on the correctness of the implementation.

        G = nx.DiGraph()
        assert_true(isinstance(EswaranTarjan.eswaran_tarjan(G), Set))
        G.add_edge(0, 1)
        result = EswaranTarjan.eswaran_tarjan(G)
        assert_true(isinstance(EswaranTarjan.eswaran_tarjan(G), Set))
        element = result.pop()
        assert_true(isinstance(element, tuple))
        assert_true(len(element) == 2)

    def test_empty(self):
        # Testing on empty digraph, empty set expected.
        assert_set_equal(EswaranTarjan.eswaran_tarjan(nx.DiGraph()), set(), "Expected empty set")

    def test_trivial(self):
        # Testing digraph with one vertex, empty set expected.
        assert_set_equal(EswaranTarjan.eswaran_tarjan(nx.complete_graph(1, nx.DiGraph())), set(), "Expected empty set")

    def test_directed_path_joins_ends(self):
        # Testing if called on directed path,
        # expected
        for i in range(2, 11):
            assert_set_equal(EswaranTarjan.eswaran_tarjan(nx.path_graph(i, nx.DiGraph())), {(i - 1, 0)})

    """
    --------------------
    The following tests test the correct behaviour on corner cases
    in regard to s, t, p, q as defined in eswaran_tarjan
    --------------------
    """

    def test_A_critical_q_null_p_eq_st(self):
        # tests correct behaviour if q = 0 and p = s = t
        G = nx.DiGraph()
        for i in range(0, 5):
            G.add_edge(2 * i, 2 * i + 1)
        assert_true(is_correctly_augmented(G))

    def test_A_critical_q_null_p_lower_s_eq_t(self):
        # tests correct behaviour if q = 0 and p < s = t
        # To test this, we test in on a "crossroad" graph G
        # E(G) = {(a, m), (m, b), (c, m), (d, m)}
        # We test both if p + 1 = s = t and if the difference if bigger
        # and also if the underlying undirected graph is not connected
        G = nx.DiGraph()
        G.add_edges_from({('a', 'm'), ('m', 'b'), ('c', 'm'), ('m', 'd')})
        assert_true(is_correctly_augmented(G))

        H = nx.DiGraph()
        H.add_edges_from({('a', 'm'), ('m', 'b'), ('c', 'm'), ('m', 'd'),
                          ('e', 'm'), ('m', 'f')})
        assert_true(is_correctly_augmented(H))

        G = nx.disjoint_union(G, H)
        assert_true(is_correctly_augmented(G))

    def test_A_critical_q_null_p_lower_s_lower_t(self):
        # tests correct behaviour if q = 0 and p < s < t.
        # We extend our crossroad graph by extending the central cross
        # one vertex to each side. As previously, we test
        # if s + 1 = t and if the difference is bigger.
        # We also test correct behaviour on reversed graph.
        G = nx.DiGraph()
        G.add_edges_from({('a', 'p'), ('p', 'm'), ('m', 'n'),
                          ('n', 'b'), ('n', 'c'), ('d', 'q'),
                          ('q', 'm'), ('m', 'o'), ('o', 'e')})
        assert_true(is_correctly_augmented(G))
        G.add_edges_from({('o', 'f')})
        assert_true(is_correctly_augmented(G))
        G = G.reverse()
        assert_true(is_correctly_augmented(G))

    def test_A_critical_q_notnull_stp_null(self):
        # tests correct behaviour if q != 0 and 0 = p = s = t.
        # This will be done using generating number of graphs where
        # no two vertices are connected. G will have both, even and odd number
        # of vertices.
        n = 1
        for i in range(5):
            G: nx.DiGraph = nx.DiGraph()
            G.add_nodes_from({j for j in range(2 ** i + n)})
            n = n + 1
            assert_true(is_correctly_augmented(G))

    def test_A_critical_q_notnull_p_eq_st_not_null(self):
        # tests correct behaviour if q != 0, 0 < p = s = t
        # To test this, we will test cases when p, s, t = {1, 2}
        # and q = {0, 1}
        G = nx.DiGraph()
        G.add_node(0)
        H = nx.path_graph(2, nx.DiGraph())
        G = nx.disjoint_union(G, H)
        assert_true(is_correctly_augmented(G))

        H = nx.path_graph(3, nx.DiGraph())
        G = nx.disjoint_union(G, H)
        assert_true(is_correctly_augmented(G))

        H = nx.DiGraph()
        H.add_node(0)
        G = nx.disjoint_union(G, H)
        assert_true(is_correctly_augmented(G))

    def test_A_critical_q_notnull_p_lower_s_eq_t(self):
        # tests correct behaviour if q != 0 and p < s = t
        # To test this, we test in on a "crossroad" graph G
        # E(G) = {(a, m), (m, b), (c, m), (d, m)}
        # We test both if p + 1 = s = t and if the difference if bigger
        # and also if the underlying undirected graph is not connected
        G = nx.DiGraph()
        G.add_nodes_from({0})

        G.add_edges_from({('a', 'm'), ('m', 'b'), ('c', 'm'), ('m', 'd')})
        assert_true(is_correctly_augmented(G))

        H = nx.DiGraph()
        H.add_edges_from({('a', 'm'), ('m', 'b'), ('c', 'm'), ('m', 'd'),
                          ('e', 'm'), ('m', 'f')})
        assert_true(is_correctly_augmented(H))

        G = nx.disjoint_union(G, H)
        assert_true(is_correctly_augmented(G))

        H.clear()
        H.add_nodes_from({0})
        G = nx.disjoint_union(G, H)
        assert_true(is_correctly_augmented(G))

    def test_A_critical_q_notnull_p_lower_s_lower_t(self):
        # tests correct behaviour if q = 0 and p < s < t.
        # We extend our crossroad graph by extending the central cross
        # one vertex to each side. As previously, we test
        # if s + 1 = t and if the difference is bigger.
        # Moreover, we test adding 1 resp. 2 isolated vertices.
        G = nx.DiGraph()
        G.add_edges_from({('a', 'p'), ('p', 'm'), ('m', 'n'),
                          ('n', 'b'), ('n', 'c'), ('d', 'q'),
                          ('q', 'm'), ('m', 'o'), ('o', 'e')})
        assert_true(is_correctly_augmented(G))
        G.add_edges_from({('o', 'f')})
        assert_true(is_correctly_augmented(G))

        G.add_node(0)
        assert_true(is_correctly_augmented(G))

        G.add_node(1)
        assert_true(is_correctly_augmented(G))

    """
    --------------------
    End of testing corner cases regarding s, t, p, q
    --------------------
    """

    def test_tree_and_reversed(self):
        # Testing correct behaviour on trees, expecting to connect all leaves and one
        # leaf with root.
        for i in range(0, 5):
            G: nx.DiGraph = nx.generators.classic.balanced_tree(2, i, create_using=nx.DiGraph)
            assert_true(is_correctly_augmented(G))
            G = G.reverse()
            assert_true(is_correctly_augmented(G))

    def test_several_disjoint_strongly_connected_components(self):
        # tests a correct behaviour of connecting isolated vertices when
        # there are more mutually disjoint strongly connected components,
        # this tests correct choice of representative and connecting only
        # isolated vertices.
        n = 0
        for i in range(0, 5):
            G: nx.DiGraph = nx.DiGraph()
            for j in range(2 ** i + n):
                C = nx.cycle_graph(i + 2, create_using=nx.DiGraph())
                G = nx.disjoint_union(G, C)
            n = n + 1
            assert_true(is_correctly_augmented(G))

    def test_random_graphs(self):
        # tests behaviour on (small) random graphs of different density.
        # Used to catch graph instances not caught in previous tests,
        # for which special tests should be created afterwards.
        for i in range(1, 100):
            p = 0.199
            while p < 1:
                G = nx.fast_gnp_random_graph(i, p, directed=True)
                assert_true(is_correctly_augmented(G))
                p += 0.2
