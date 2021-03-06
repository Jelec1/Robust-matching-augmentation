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
from src.algo.EswaranTarjan import eswaran_tarjan
from src.algo.SourceCover import source_cover
from src.utils.AuxiliaryFunctions import fast_traversal
from networkx.utils.decorators import not_implemented_for
from src.exceptions.Exceptions import bipartite_ghraph_not_augmentable_exception


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

        References
        ----------
        [1]  BINDEWALD, Viktor; HOMMELSHEIM, Felix; MÜHLENTHALER, Moritz; SCHAUDT, Oliver.
        How to Secure Matchings Against Edge Failures. CoRR. 2018, vol. abs/1805.01299. Available from arXiv:
        1805.01299

        """

    if len(A) <= 1:  # Graph consisting of only one vertex at each bipartition cannot be augmented.
        raise bipartite_ghraph_not_augmentable_exception("G cannot be augmented.")

    if M is None:  # User can specify her own matching for speed-up
        M: Dict = nx.algorithms.bipartite.eppstein_matching(G, A)

    D: nx.DiGraph = nx.DiGraph()

    for u in M:  # Construction of D, iterate over all keys in M
        if u in A:  # Add all edges from A to D
            w = M[u]
            D.add_node(u)

            outgoing: int = 0
            for uPrime in G.neighbors(w):  # Construct edges of D
                if uPrime != u:
                    D.add_edge(u, uPrime)

    D_condensation: nx.DiGraph = nx.algorithms.components.condensation(D)  # Condensation - acyclic digraph

    X: Set = set()  # A set of vertices of D_condensation corresponding to trivial strong components of D
    isolated: Set = set()  # Set of isolated vertices
    sources: Set = set()  # Set of vertices that are not isolated and have no ingoing arc
    sinks: Set = set()  # Set of vertices that are not isolated and have no outgoing arc

    # We do not use function sources, sinks, isolated for performance reasons
    # Because we would either have to loop twice or check one more condition in the loop
    # if we were to modify the function.
    for vertex in D_condensation.nodes:
        inDegree: int = D_condensation.in_degree(vertex)
        outDegree: int = D_condensation.out_degree(vertex)

        if len(D_condensation.nodes[vertex]['members']) == 1:
            # Each trivial strong component is incident to some critical edge
            X.add(vertex)
        if inDegree == 0 and outDegree == 0:
            # Isolated: neither ingoing nor outgoing arc
            isolated.add(vertex)
        elif inDegree == 0:
            # Source: no ingoing arc and not isolated
            sources.add(vertex)
            # Sink: no outgoing arc and not isolated
        elif outDegree == 0:
            sinks.add(vertex)

    A_0 = D_condensation
    A_1 = D_condensation.reverse(copy=False)

    if len(X) == 0:  # If there is no trivial strong component, G admits a perfect matching after edge removal
        return set()

    # Use source_cover to choose ln(n) approximation of choice of sources that cover all sinks in C_0, resp. C_1
    C_0 = source_cover(A_0, X, (sources, sinks, isolated))
    C_1 = source_cover(A_1, X, (sinks, sources, isolated))

    # We now determine vertices that lie either on C_1X paths or XC_2 paths
    # Vertices on C_1X paths are those visited when traveling from C_1 to X on
    # D_condensation and from X to C_1 on D_condensation_reverse
    CX_vertices = set()
    XC_vertices = set()
    D_condensation_reverse = D_condensation.reverse(copy=False)

    # Now, specify arguments for the fast DFS traversal
    def action_on_vertex_CX(current_vertex):
        CX_vertices.add(current_vertex)  # We have reached it from C, so add it in
        return True

    def action_on_neighbor_CX(neighbor, current_vertex):
        return neighbor not in CX_vertices

    def action_on_vertex_XC(current_vertex):
        XC_vertices.add(current_vertex)
        return True

    def action_on_neighbor_XC(neighbor, current_vertex):
        return neighbor not in XC_vertices

    for source in C_0:
        # Reachable from C_0 (search for X)
        fast_traversal(D_condensation, source, action_on_vertex_CX, action_on_neighbor_CX)

    for critical in X:
        # Reachable from X (search for C_2)
        fast_traversal(D_condensation, critical, action_on_vertex_CX, action_on_neighbor_CX)
        # Reachable from X (search for C_1)
        fast_traversal(D_condensation_reverse, critical, action_on_vertex_XC, action_on_neighbor_XC)

    for source in C_1:
        # Reachable from C_2 (search for X)
        fast_traversal(D_condensation_reverse, source, action_on_vertex_XC, action_on_neighbor_XC)

    D_hat_vertices = CX_vertices & XC_vertices  # Intersection

    # Marginal case when single vertex cannot be connected to form non-trivial strongly connected component.
    # We need to add another arbitrary vertex, which always exists as |V(D)| is guaranteed to be > 2 and contains
    # at least one trivial strong component.
    if len(D_hat_vertices) == 1:
        vert = next(iter(D_hat_vertices))
        D_hat_vertices.add(next(iter(set(D_condensation.nodes) - {vert})))

    #  Update sources, sinks, isolated as intersection with D_hat_vertices
    sources &= D_hat_vertices
    sinks &= D_hat_vertices
    isolated &= D_hat_vertices

    D_hat = nx.classes.function.induced_subgraph(D_condensation, D_hat_vertices)
    L_star: Set = eswaran_tarjan(D_hat, is_condensation=True, sourcesSinksIsolated=(sources, sinks, isolated))

    # Map vertices from L to vertices of L*
    return set(map(lambda e: (next(iter(D_condensation.nodes[e[1]]['members'])),
                              M[next(iter(D_condensation.nodes[e[0]]['members']))]), L_star))
