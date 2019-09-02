from nose.tools import assert_set_equal, assert_raises, assert_false, assert_equal, assert_true
import networkx as nx
from Algo.EswaranTarjan import eswaran_tarjan
# from networkx.testing import assert_graphs_equal


class TestEswaranTarjan:

    def test_directed(self):
        # print("Testing on directed graph, no exception expected")
        exception = False
        try:
            eswaran_tarjan(nx.DiGraph())
        except:
            exception = True
        assert_false(exception, "eswaran_tarjan should be implemented for networkx.DiGraph")

    def test_wrong_graph_type(self):
        # print("Testing on unsupported graph types, exception networkx.NetworkXNotImplemented expected")
        # print("-networkx.Graph()")
        assert_raises(nx.NetworkXNotImplemented, eswaran_tarjan, nx.Graph())
        # print("-networkx.MultiGraph()")
        assert_raises(nx.NetworkXNotImplemented, eswaran_tarjan, nx.MultiGraph())
        # print("-networkx.MultiDiGraph()")
        assert_raises(nx.NetworkXNotImplemented, eswaran_tarjan, nx.MultiDiGraph())

    def test_non_condensation(self):
        # print("Testing non condensed graph with is_condensation=True, exception networkx.HasACycle expected")
        G: nx.DiGraph = nx.cycle_graph(range(1, 4), nx.DiGraph())
        assert_raises(nx.HasACycle, eswaran_tarjan, G, True)
        G.add_node(0)
        assert_raises(nx.HasACycle, eswaran_tarjan, G, True)
        G.clear()
        G.add_edges_from({(0, 1), (1, 0)})
        assert_raises(nx.HasACycle, eswaran_tarjan, G, True)

    def test_empty(self):
        # print("Testing empty graph.")
        assert_set_equal(eswaran_tarjan(nx.DiGraph()), set(), "Expected empty set")

    def test_trivial(self):
        # print("Testing graph with one vertex.")
        assert_set_equal(eswaran_tarjan(nx.complete_graph(1, nx.DiGraph())), set(), "Expected empty set")

    def test_directed_path_joins_ends(self):
        # print("Testing if called on directed path, correctly connects path ends")
        for i in range(2, 11):
            assert_set_equal(eswaran_tarjan(nx.path_graph(i, nx.DiGraph())), {(i - 1, 0)})

    def test_tree(self):
        for i in range(0, 5):
            G: nx.DiGraph = nx.generators.classic.balanced_tree(2, i, create_using=nx.DiGraph)
            A = eswaran_tarjan(G)
            G.add_edges_from(A)
            cond = nx.algorithms.condensation(G)
            assert_equal(len(cond.nodes), 1)

            G: nx.DiGraph = nx.generators.classic.balanced_tree(2, i, create_using=nx.DiGraph)
            G = G.reverse()
            A = eswaran_tarjan(G)
            G.add_edges_from(A)
            cond = nx.algorithms.condensation(G)
            assert_equal(len(cond.nodes), 1)

    def test_isolated(self):
        n = 0
        for i in range(5):
            G: nx.DiGraph = nx.DiGraph()
            G.add_nodes_from({j for j in range(2**i + n)})
            n = n + 1
            G.add_edges_from(eswaran_tarjan(G))
            assert_true(nx.algorithms.is_strongly_connected(G))


