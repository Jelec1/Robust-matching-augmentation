"""
Author: Tomas Jelinek
Last change: 12.9.2019

Description: Implementation of the bipartite matching augmentation algorithm
due to Implementation is based on BINDEWALD, Viktor; HOMMELSHEIM, Felix; MÜHLENTHALER, Moritz; SCHAUDT, Oliver.
        How to Secure Matchings Against Edge Failures. CoRR. 2018, vol. abs/1805.01299. Available from arXiv:
        1805.01299
"""

import networkx as nx
from typing import Dict, Set, List
from Algo.EswaranTarjan import eswaran_tarjan
from Algo.SourceCover import source_cover
from utils.AuxiliaryAlgorithms import fast_dfs, bipartite_to_D
from networkx.utils.decorators import not_implemented_for
from Exceptions.Exceptions import BipartiteGraphNotAugmentableException
from multiprocessing import Pool
import time

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

    start = time.time()
    verystart = time.time()

    if M is None:  # User can specify her own matching for speed-up
        M: Dict = nx.algorithms.bipartite.eppstein_matching(G, A)

    print("Constructing matching", time.time() - start)
    start = time.time()

    D: nx.DiGraph = bipartite_to_D(G, A, M)

    print("Computing D", time.time() - start)
    start = time.time()

    X: Set = set()  # A set of vertices of D_condensation corresponding to trivial strong components of D

    D_condensation: nx.DiGraph = nx.algorithms.components.condensation(D)

    print("Computing condensation", time.time() - start)
    start = time.time()

    A_0 = D_condensation.copy()
    A_1 = D_condensation.reverse(copy=True)

    print("Making two copies", time.time() - start)
    start = time.time()

    for node in D_condensation:
        # Each trivial strong component is incident to some critical edge
        if len(D_condensation.nodes[node]['members']) == 1:
            X.add(node)

            vertices_to_remove: Set = set()

            # Defines action for fast_dfs, i.e. add current vertex
            def action_on_vertex(current_vertex):
                vertices_to_remove.add(current_vertex)
                return True

            # Action on neighbor, just continue with the neighbor
            def action_on_neighbor(neighbor, parent):
                return True

            if node in A_0.nodes:  # Remove all vertices reachable from trivial strong component in A_0
                vertices_to_remove = set()
                fast_dfs(A_0, node, action_on_vertex, action_on_neighbor)
                vertices_to_remove.remove(node)
                A_0.remove_nodes_from(vertices_to_remove)

            if node in A_1.nodes:  # Remove all vertices reachable from trivial strong component in A_0
                vertices_to_remove = set()
                fast_dfs(A_1, node, action_on_vertex, action_on_neighbor)
                vertices_to_remove.remove(node)
                A_1.remove_nodes_from(vertices_to_remove)

    if len(X) == 0:  # If there is no trivial strong component, G admits a perfect matching after edge removal
        return set()

    print("Deleting reachable from X", time.time() - start)
    start = time.time()

    # Use source_cover to choose ln(n) approximation of choice of sources that cover all sinks in C_0, resp. C_1
    C_0 = source_cover(A_0)
    C_1 = source_cover(A_1)

    print("Twice source cover", time.time() - start)
    start = time.time()

    # We can run both independently in parallel
    #pool = Pool(2)
    #r2 = pool.apply_async(source_cover, (A_0,))
    #r3 = pool.apply_async(source_cover, (A_1,))
    #C_0 = r2.get()
    #C_1 = r3.get()

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
        fast_dfs(D_condensation, source, action_on_vertex_CX, action_on_neighbor_CX)  # Reachable from C_0 (search for X)

    for critical in X:
        fast_dfs(D_condensation, critical, action_on_vertex_CX, action_on_neighbor_CX)  # Reachable from X (search for C_2)
        fast_dfs(D_condensation_reverse, critical, action_on_vertex_XC, action_on_neighbor_XC)  # Reachable from X (search for C_1)

    for source in C_1:
        fast_dfs(D_condensation_reverse, source, action_on_vertex_XC, action_on_neighbor_XC)  # Reachable from C_2 (search for X)

    D_hat_vertices = CX_vertices & XC_vertices  # Intersection

    # Marginal case when single vertex cannot be connected to form non-trivial strongly connected component.
    # We need to add another arbitrary vertex, which always exists as |V(D)| is guaranteed to be > 2 and contains
    # at least one trivial strong component.
    if len(D_hat_vertices) == 1:
        vert = next(iter(D_hat_vertices))
        D_hat_vertices.add(next(iter(set(D_condensation.nodes) - {vert})))

    print("Computing D_hat", time.time() - start)
    start = time.time()

    D_hat = nx.classes.function.induced_subgraph(D_condensation, D_hat_vertices)
    L_star: Set = eswaran_tarjan(D_hat, is_condensation=True)

    print("Eswaran Tarjan", time.time() - start)
    print("TOTAL:", time.time() - verystart)
    start = time.time()

    # Map vertices from L to vertices of L*
    return set(map(lambda e: (next(iter(D_condensation.nodes[e[1]]['members'])),
                              M[next(iter(D_condensation.nodes[e[0]]['members']))]), L_star))
