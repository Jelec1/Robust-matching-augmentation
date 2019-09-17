"""
Author: Tomas Jelinek
Last change: 12.9.2019

Description: Implementation of the bipartite matching augmentation algorithm
due to Implementation is based on BINDEWALD, Viktor; HOMMELSHEIM, Felix; MÜHLENTHALER, Moritz; SCHAUDT, Oliver.
        How to Secure Matchings Against Edge Failures. CoRR. 2018, vol. abs/1805.01299. Available from arXiv:
        1805.01299
"""
import networkx as nx
from typing import Dict, Set
from Algo.EswaranTarjan import eswaran_tarjan
from Algo.SourceCover import sourceCover
from networkx.utils.decorators import not_implemented_for
from Exceptions.Exceptions import BipartiteGraphNotAugmentableException


@not_implemented_for('directed')
@not_implemented_for('multigraph')
def bipartite_matching_augmentation(G: nx.Graph, A: Set, M: Dict = None):
    """Returns a set of edges A such that G(V, E + A) is strongly connected.

        Parameters
        ----------
        G : NetworkX Graph
           A bipartite graph G = (A + B, E), where G can be augmented, that is |A + B| >= 4.
           G must also admit a perfect matching.
        A : Set
            A bipartition of G, where |A| = |A + B| / 2
        M: Dict = None
            A perfect bipartite matching of G, for each edge {a, b} in M holds M[a] = b, M[b] = a.
            If M is not given, it will be computed using eppstein_matching(G, A)

        Returns
        -------
        L : Set
           Set of edges from E(G) - M such that G admits a perfect matching even after a single arbitrary
           edge is removed. Edges are in form of (a, b), where a is from A and b from B

        Raises
        ------
        NetworkX.NotImplemented:
            If G is directed or a multigraph.

        Notes
        -----
        Implementation is based on BINDEWALD, Viktor; HOMMELSHEIM, Felix; MÜHLENTHALER, Moritz; SCHAUDT, Oliver.
        How to Secure Matchings Against Edge Failures. CoRR. 2018, vol. abs/1805.01299. Available from arXiv:
        1805.01299
        """

    if len(A) <= 1:  # Graph consisting of only one vertex at each bipartition cannot be augmented.
        raise BipartiteGraphNotAugmentableException("G cannot be augmented.")

    if M is None:  # User can specify her own matching for speed-up
        M: Dict = nx.algorithms.bipartite.eppstein_matching(G, A)

    D: nx.DiGraph = nx.DiGraph()

    for u in M:  # Construction of D, iterate over all keys in M
        if u in A:  # Add all edges from A to D
            w = M[u]
            D.add_node(u)

            for uPrime in G.neighbors(w):  # Construct edges of D
                if uPrime != u:
                    D.add_edge(u, uPrime)

    X: Set = set()  # A set of vertices of D_condensation corresponding to trivial strong components of D

    D_condensation: nx.DiGraph = nx.algorithms.components.condensation(D)

    # We init A_0, A_1 to be the full subgraph of D, implemented as a graph view
    A_0 = nx.induced_subgraph(D_condensation, D_condensation.nodes)
    A_1 = nx.induced_subgraph(D_condensation.reverse(copy=False), D_condensation.nodes)

    for node in D_condensation:

        # Each trivial strong component is incident to some critical edge
        if len(D_condensation.nodes[node]['members']) == 1:
            X.add(node)

            if node in A_0.nodes:  # Remove all vertices reachable from trivial strong component in A_0
                nodes = (set(A_0.nodes) - set(nx.algorithms.dfs_preorder_nodes(A_0, node))) | {node}
                A_0 = nx.induced_subgraph(D_condensation, nodes)

            if node in A_1.nodes:  # Remove all vertices reachable from trivial strong component in A_1
                nodes = (set(A_1.nodes) - set(nx.algorithms.dfs_preorder_nodes(A_1.reverse(copy=False), node))) | {node}
                A_1 = nx.induced_subgraph(D_condensation.reverse(copy=False), nodes)

    if len(X) == 0:  # If there is no trivial strong component, G admits a perfect matching after edge removal
        return set()

    # Use sourceCover to choose ln(n) approximation of choice of sources that cover all sinks in C_0, resp. C_1
    C_0 = sourceCover(A_0)
    C_1 = sourceCover(A_1)

    def mark_vertices(graph: nx.DiGraph, vertex, mark, max_mark: int):
        # A subroutine marks all vertices reachable from DFS search that are not already marked.
        # Starting from several vertices thus runs in O(n + m). Used while loop to prevent stack overflow.

        stack = [vertex]
        if mark not in graph.nodes[vertex]:
            graph.nodes[vertex][mark] = 0
        if graph.nodes[vertex][mark] < max_mark:
            graph.nodes[vertex][mark] += 1

        while stack:
            vertex = stack.pop()

            for neighbour in graph.neighbors(vertex):

                if mark not in graph.nodes[neighbour]:
                    graph.nodes[neighbour][mark] = 0

                if graph.nodes[neighbour][mark] < max_mark:
                    graph.nodes[neighbour][mark] += 1
                    stack.append(neighbour)

    for source in C_0:
        mark_vertices(D_condensation, source, "C1X", 1)

    for source in C_1:
        mark_vertices(D_condensation.reverse(copy=False), source, "XC2", 1)

    for critical in X:
        mark_vertices(D_condensation.reverse(copy=False), critical, "C1X", 2)
        mark_vertices(D_condensation, critical, "XC2", 2)

    D_hat_vertices: Set = set()

    # Vertices C1X or C2X paths are an intersection of vertices that received max mark.
    for node in D_condensation:
        if ("C1X" in D_condensation.nodes[node] and D_condensation.nodes[node]["C1X"] == 2) \
                or ("XC2" in D_condensation.nodes[node] and D_condensation.nodes[node]["XC2"] == 2):
            D_hat_vertices.add(node)

    # Marginal case when single vertex cannot be connected to form non-trivial strongly connected component.
    # We need to add another arbitrary vertex, which always exists as |V(D)| is guaranteed to be > 2 and contains
    # at least one trivial strong component.
    if len(D_hat_vertices) == 1:
        vert = next(iter(D_hat_vertices))
        D_hat_vertices.add(next(iter(set(D_condensation.nodes) - {vert})))

    D_hat = nx.classes.function.induced_subgraph(D_condensation, D_hat_vertices)
    L_star: Set = eswaran_tarjan(D_hat, is_condensation=True)

    # Map vertices from L to vertices of L*
    return set(map(lambda e: (next(iter(D_condensation.nodes[e[1]]['members'])),
                              M[next(iter(D_condensation.nodes[e[0]]['members']))]), L_star))
