import networkx as nx
from Tests.TestBipartiteMatchingAugmentation import D_to_bipartite
from Algo.BipartiteMatchingAugmentation import bipartite_matching_augmentation

class TestPerformance:

    def test_performance(self):
        # Tests random graph, which must be very sparse due to time complexity
        # Also test the

        for i in range(100):
            D: nx.DiGraph = nx.generators.random_graphs.erdos_renyi_graph(1000, 0.001, directed=True)
            D.remove_node(0)
            D.remove_edges_from([(u, v) for (u, v) in D.edges() if u < v])
            G, A, M = D_to_bipartite(D)
            bipartite_matching_augmentation(G, A)

