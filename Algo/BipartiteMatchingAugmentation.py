import networkx as nx
from typing import List, Dict, Set


def esweran_tarjan(G: nx.DiGraph):
    sink_not_found = True

    v_i = set()
    w_i = set()

    sources: Set = set()
    sinks: Set = set()

    for node in G:
        if G.in_degree(node) == 0 and G.out_degree(node) > 0:
            sources.add(node)
        elif G.in_degree(node) > 0 and G.out_degree(node) == 0:
            sources.add(node)




    marked_nodes = set()  # unmark all nodes
    unmarked_nodes = set()
    i = 0
    while len(unmarked_nodes.intersection(unmarked_nodes)) > 0:
        v = unmarked_nodes.intersection(unmarked_nodes) # some unmarked souce
        w = 0
        sink_not_found = True

        """
        Procedure SEARCH(X)
        """
        if v == 'is unmarked':
            if v == 'is a sink':
                w = v
                sink_not_found = False
            "mark v"

            # It is usually more convenient (and faster) to access the adjacency dictionary asG[n]:
            # [n for n in G[0]]
            for y in G.neighbors(v):
                if sink_not_found:
                    search(y)

        """
        end SEARCH
        """


        if w != 0:
            i = i + 1
            v_i[i] = v
            w_i[i] = w

    p = i








# Param us bipartite undirected graph (U, W, E)
# Matching is expected to be a set of doubles (u, v) corresponding to a matching
# where u is from A and vis from B of a bipartite graph
def augmentGraph(G: nx.DiGraph, M: Set):
    D = nx.DiGraph()

    for edge in M:
        u = edge[0]
        w = edge[1]
        # We cycle through all the edges in the set W to construct a directed graph D(G,M) from Theorem 11
        for uPrime in G.neighbors(w):
            # This is the construction of A, where edge[0] is u, edge[1] is w
            # and we are looking for u' =/= u
            if uPrime != u:
                D.add_edge(u, uPrime)

    # Now we remove for all u_e adjacent to a critical edge in matching, all edges but u_e reachable in u_e
    # Note that edge is critical iff strongly connected component u_e belongs to is trivial

    # !!!!!!!!Consult time complexity of this with  Obdrzalek
    """Unfortunately, this package cannot return a strongly connected component with a source vertex
    matchingLeftNodes = {u[0] for u in matching}

    while len(matchingLeftNodes) > 0: #note that len on sets and lists in python is in O(1)

        #We know that the set is not empty
        u = matchingLeftNodes.pop()
    """

    Di: List[nx.DiGraph] = [D.copy(), D.copy().reverse()]  # This is D resp D' in the paper
    condensation_i: List[nx.DiGraph] = [nx.DiGraph(), nx.DiGraph()]  # Corresponds to C(D) resp. C(D')
    Ci = [None, None]  # Solution C_i of instances A_i, i \in {1,2}
    strongComponents_i: List = [None, None]

    criticalVertices = set()

    for i in {0, 1}:

        strongComponents_i[i] = nx.strongly_connected_components(Di[i])
        # Note that this actually uses Tarjan's algorithm as suggested in the paper
        # Actually, consider using it directly rather than assigning it to a variable

        for component in strongComponents_i[i]:
            if len(component) == 1:  # component is trivial
                u_e = component[0]
                criticalVertices.add(u_e)

                # Could spare some time by deleting edges from the reverse
                for v in nx.algorithms.traversal.depth_first_search.dfs_edges(Di[i], u_e):
                    if v != u_e:
                        Di[i].remove_node(v)


        condensation_i[i] = nx.algorithms.components.condensation(Di[i])
        # Condensation_i[i] has an attribute "members" mapping vertices of the condensation to the original vertices
        # Still need to figure out whether I should do condensation together with DFS as suggested in the paper

        Ci[i] = sourceCover(Ci[i])

    sourcesAndSinks: Set = set()

    for nodeIn in condensation_i[0].in_degree():   # iterates over doubles (vert, in_degree)
        node = nodeIn[0]
        inDegree = nodeIn[1]

        if inDegree == 0:
            sourcesAndSinks.add(node)  # add all sources

    for nodeOut in condensation_i[1].out_degree():
        node = nodeOut[0]
        outDegree = nodeOut[1]

        if outDegree == 0:
            sourcesAndSinks.add(node)  # add all sinks

    X = set()

    for node in condensation_i[0]:
        # Note that node adjoint an edge is critical iff corresponding strongly connected component is trivial
        if len(node.members) == 1:
            X.add(node)


    DFS_SourcesAndSinksVerts: Set = set()

    DFS_Xverts: Set = set()

    for s in sourcesAndSinks:
        # Find out how to get index of given node
        DFS_SourcesAndSinksVerts.add(nx.algorithms.traversal.depth_first_search.dfs_tree(condensation_i[0], s))

    for x in X:
        DFS_Xverts.add(nx.algorithms.traversal.depth_first_search.dfs_tree(condensation_i[0], x))


    D_dash: nx.DiGraph = condensation_i[0].subgraph(DFS_Xverts.intersection(DFS_SourcesAndSinksVerts))











    pass


def sourceCover():
    return {}
