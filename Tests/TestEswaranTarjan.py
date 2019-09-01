from nose.tools import assert_set_equal
import networkx as nx
from Algo.EswaranTarjan import eswaran_tarjan

def test_empty():
    print("Testing empty graph")
    assert_set_equal(eswaran_tarjan(nx.Graph()), set(), "Expected empty set")

def test_trivial():
    print("Testing graph with exactly one vertex")
    assert_set_equal(eswaran_tarjan(nx.Graph({})), set(), "Expected empty set")