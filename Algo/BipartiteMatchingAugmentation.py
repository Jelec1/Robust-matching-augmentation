import networkx as nx
from typing import Dict, Set

from Algo.EswaranTarjan import eswaran_tarjan
from Algo.SourceCover import sourceCover


# Param us bipartite undirected graph (U, W, E)
# Matching is expected to be a set of doubles (u, v) corresponding to a matching
# where u is from A and vis from B of a bipartite graph
def bipartite_matching_augmentation(G: nx.Graph, A: Set):
    D: nx.DiGraph = nx.DiGraph()

    if not nx.algorithms.bipartite.is_bipartite_node_set(G, A):
        raise Exception("G is not bipartite")

    if len(A) <= 1:
        raise  Exception("G cannot be augmented as A contains only one vertex.")

    M: Dict = nx.algorithms.bipartite.eppstein_matching(G, A)

    if not nx.algorithms.is_perfect_matching(G, M):
        raise Exception("G does not admit a perfect matching")

    for u in M:  # Looping through a dictionary
        if u not in A:
            continue

        w = M[u]  # Just to be sure we have one
        D.add_node(u)  # This is necessary as not always edge is added

        # We cycle through all the edges in the set W to construct a directed graph D(G,M) from Theorem 11
        for uPrime in G.neighbors(w):
            # This is the construction of A, where edge[0] is u, edge[1] is w
            # and we are looking for u' =/= u
            if uPrime != u:
                D.add_edge(u, uPrime)

    # Now we remove for all u_e adjacent to a critical edge in matching, all edges but u_e reachable in u_e
    # Note that edge is critical iff strongly connected component u_e belongs to is trivial

    X: Set = set()

    condensation_of_D: nx.DiGraph = nx.algorithms.components.condensation(D)

    A_0 = nx.induced_subgraph(condensation_of_D, condensation_of_D.nodes)
    A_1 = nx.induced_subgraph(condensation_of_D.reverse(copy=False), condensation_of_D.nodes)

    for node in condensation_of_D:

        if len(condensation_of_D.nodes[node]['members']) == 1:  # node is incident to a critical edge
            X.add(node)

            if node in A_0.nodes:
                nodes = set(A_0.nodes) - set(nx.algorithms.dfs_preorder_nodes(A_0, node)) | {node}
                A_0 = nx.induced_subgraph(condensation_of_D, nodes)

            if node in A_1.nodes:
                nodes = set(A_1.nodes) - set(nx.algorithms.dfs_preorder_nodes(A_1.reverse(copy=False), node)) | {node}
                A_1 = nx.induced_subgraph(condensation_of_D.reverse(copy=False), nodes)

    if len(X) == 0:
        return set()

    C_0 = sourceCover(A_0)
    C_1 = sourceCover(A_1)

    def markVertices(graph: nx.DiGraph, vertex, mark, maxMark: int):
        stack = [vertex]
        if mark not in graph.nodes[vertex]:
            graph.nodes[vertex][mark] = 0
        if graph.nodes[vertex][mark] < maxMark:
            graph.nodes[vertex][mark] += 1

        while stack:
            vertex = stack.pop()

            for neighbour in graph.neighbors(vertex):

                if mark not in graph.nodes[neighbour]:
                    graph.nodes[neighbour][mark] = 0

                if graph.nodes[neighbour][mark] < maxMark:
                    graph.nodes[neighbour][mark] += 1
                    stack.append(neighbour)

    for source in C_0:  # condensation_i[i].nodes[node]['members']
        markVertices(condensation_of_D, source, "C1X", 1)

    for source in C_1:
        markVertices(condensation_of_D.reverse(copy=False), source, "XC2", 1)

    for critical in X:
        markVertices(condensation_of_D.reverse(copy=False), critical, "C1X", 2)
        markVertices(condensation_of_D, critical, "XC2", 2)

    D_dash_vertices: Set = set()

    for node in condensation_of_D:
        if ("C1X" in condensation_of_D.nodes[node] and condensation_of_D.nodes[node]["C1X"] == 2) \
                or ("XC2" in condensation_of_D.nodes[node] and condensation_of_D.nodes[node]["XC2"] == 2):
            D_dash_vertices.add(node)

    if len(D_dash_vertices) == 1:
        vert = next(iter(D_dash_vertices))
        D_dash_vertices.add(next(iter(set(condensation_of_D.nodes) - {vert})))

    D_dash = nx.classes.function.induced_subgraph(condensation_of_D, D_dash_vertices)
    L_star: Set = eswaran_tarjan(D_dash)


    # TODO : maybe rather for loop and yield?
    return set(map(lambda e: (next(iter(condensation_of_D.nodes[e[1]]['members'])),
                              M[next(iter(condensation_of_D.nodes[e[0]]['members']))]), L_star))
