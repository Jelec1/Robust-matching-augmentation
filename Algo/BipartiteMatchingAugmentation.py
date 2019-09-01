import networkx as nx
from typing import List, Dict, Set

from Algo.EswaranTarjan import eswaran_tarjan
from Algo.SourceCover import sourceCover


# Param us bipartite undirected graph (U, W, E)
# Matching is expected to be a set of doubles (u, v) corresponding to a matching
# where u is from A and vis from B of a bipartite graph
def augmentGraph(G: nx.Graph, A: Set):
    D: nx.DiGraph = nx.DiGraph()

    if not nx.algorithms.bipartite.is_bipartite_node_set(G, A):
        raise Exception("G is not bipartite")

    M: Dict = nx.algorithms.bipartite.eppstein_matching(G, A)

    if not nx.algorithms.is_perfect_matching(G, M):
        raise Exception("G does not admit a perfect matching")

    for u in M:  # Looping through a dictionary
        if u not in A:
            continue

        w = M[u]  # Just to be sure we have one
        D.add_node(u)  # This is neccessary as not always edge is added

        # We cycle through all the edges in the set W to construct a directed graph D(G,M) from Theorem 11
        for uPrime in G.neighbors(w):
            # This is the construction of A, where edge[0] is u, edge[1] is w
            # and we are looking for u' =/= u
            if uPrime != u:
                D.add_edge(u, uPrime)

    # Now we remove for all u_e adjacent to a critical edge in matching, all edges but u_e reachable in u_e
    # Note that edge is critical iff strongly connected component u_e belongs to is trivial

    Di: List[nx.DiGraph] = [D.copy(), D.copy().reverse()]  # This is D resp D' in the paper
    condensation_i: List[nx.DiGraph] = [nx.DiGraph(), nx.DiGraph()]  # Corresponds to C(D) resp. C(D')
    A_i: List = [None, None]
    Ci: List = [None, None]  # Solution C_i of instances A_i, i \in {1,2}
    sources_i: List[Set] = [set(), set()]
    sinks_i: List[Set] = [set(), set()]

    X: Set = set()

    for i in {0, 1}:

        condensation_i[i] = nx.algorithms.components.condensation(Di[i])
        # Note that this actually uses Tarjan's algorithm as suggested in the paper
        # Actually, consider using it directly rather than assigning it to a variable

        for node in condensation_i[i]:

            if len(condensation_i[i].nodes[node]['members']) == 1:  # component is trivial
                u_e = condensation_i[i].nodes[node]['members'].pop()  # Python allows it only like this
                condensation_i[i].nodes[node]['members'].add(u_e)

                X.add(node)

                # Could spare some time by deleting edges from the reverse
                for v in nx.algorithms.traversal.depth_first_search.dfs_edges(condensation_i[i], node):
                    if v != node:
                        Di[i].remove_node(v)

                        if v in X:
                            X.remove(v)

        A_i[i] = nx.algorithms.components.condensation(condensation_i[i])

        for nodeIn in A_i[0].in_degree():  # iterates over doubles (vert, in_degree)
            node = nodeIn[0]
            inDegree = nodeIn[1]

            if inDegree == 0:
                sources_i[i].add(node)

        for nodeIn in A_i[0].out_degree():  # iterates over doubles (vert, in_degree)
            node = nodeIn[0]
            inDegree = nodeIn[1]

            if inDegree == 0:
                sinks_i[i].add(node)

        Ci[i] = sourceCover(A_i[i], sources_i[i], sinks_i[i])

    # Consider just marking edges yielded from DFS traversal
    def markVertices(graph: nx.DiGraph, vertex, mark, maxMark: int):  # We will by this method mark vertices using DFS
        if mark not in graph.nodes[vertex]:
            graph.nodes[vertex][mark] = 0

        if graph.nodes[vertex][mark] < maxMark:
            graph.nodes[vertex][mark] += 1
        for neighbour in graph.neighbors(vertex):
            markVertices(graph, neighbour, mark, maxMark)

    for source in Ci[0]:   # condensation_i[i].nodes[node]['members']
        markVertices(condensation_i[0], source, "C1X", 1)

    for source in Ci[1]:
        markVertices(condensation_i[0].reverse(copy=False), source, "XC2", 1)

    for critical in X:
        markVertices(condensation_i[0].reverse(copy=False), critical, "C1X", 2)
        markVertices(condensation_i[0], critical, "XC2", 2)

    D_dash_vertices: Set = set()

    for node in condensation_i[0]:
        if ("C1X" in condensation_i[0].nodes[node] and condensation_i[0].nodes[node]["C1X"] == 2) \
                or ("XC2" in condensation_i[0].nodes[node] and condensation_i[0].nodes[node]["XC2"] == 2):
            D_dash_vertices.add(node)

    D_dash = nx.classes.function.induced_subgraph(condensation_i[0], D_dash_vertices)

    L_star = eswaran_tarjan(D_dash)

    L = set()

    for edge in L_star:
        u = edge[0]
        v = edge[1]
        L.add((u.memberers.pop(), v.members.pop()))

    augmenting_edges = set()

    for edge in L:
        u = edge[0]
        w = edge[1]

    pass
