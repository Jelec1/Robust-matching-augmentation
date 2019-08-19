import networkx as nx
from typing import List, Dict, Set
import math


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
        v = unmarked_nodes.intersection(unmarked_nodes)  # some unmarked souce
        w = 0
        sink_not_found = True

        def search(v):
            if v in unmarked_nodes:  # is unmarked
                if v in sinks:  # is a sink
                    w = v
                    sink_not_found = False
                marked_nodes.add(v)  # mark v
                unmarked_nodes.remove(v)

                # It is usually more convenient (and faster) to access the adjacency dictionary asG[n]:
                # [n for n in G[0]]
                for y in G.neighbors(v):
                    if sink_not_found:
                        search(y)

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

    Di: List[nx.DiGraph] = [D.copy(), D.copy().reverse()]  # This is D resp D' in the paper
    condensation_i: List[nx.DiGraph] = [nx.DiGraph(), nx.DiGraph()]  # Corresponds to C(D) resp. C(D')
    Ci: List = [None, None]  # Solution C_i of instances A_i, i \in {1,2}
    sources_i:List[Set] = List[None, None]
    sinks_i:List[Set] = List[None, None]

    X:Set = set()

    for i in {0, 1}:

        condensation_i[i] = nx.algorithms.components.condensation(Di[i])
        # Note that this actually uses Tarjan's algorithm as suggested in the paper
        # Actually, consider using it directly rather than assigning it to a variable

        for node in condensation_i[i]:
            if len(node.members) == 1:  # component is trivial
                u_e = node.pop()  # This is the only member of the set, nothing better
                node.add(u_e)

                X.add(node)

                # Could spare some time by deleting edges from the reverse
                for v in nx.algorithms.traversal.depth_first_search.dfs_edges(condensation_i[i], node):
                    if v != node:
                        Di[i].remove_node(v)

                        if v in X:
                            X.remove(v)

        for nodeIn in condensation_i[0].in_degree():  # iterates over doubles (vert, in_degree)
            node = nodeIn[0]
            inDegree = nodeIn[1]

            if inDegree == 0:
                sources_i.add(node)

        for nodeIn in condensation_i[0].out_degree():  # iterates over doubles (vert, in_degree)
            node = nodeIn[0]
            inDegree = nodeIn[1]

            if inDegree == 0:
                sinks_i.add(node)

        Ci[i] = sourceCover(condensation_i[i])



    pass

def sourceCover(D: nx.DiGraph, sources: Set, sinks: Set):
    # TODO use better dictionaries for logarithmic complexity
    # TODO use union find data structure for sets
    # TODO split the graph into components and calculate source cover on these (also in parallel)

    R: nx.DiGraph = D.reverse(copy=False)
    children: Dict[object, Set] = {}
    vertexRank: Dict[object, int] = {}

    def sinkAccessibility(vertex, parent):
        if vertex not in vertexRank:  # as we can be sure that that vertex has never ever been accessed before
            vertexRank[vertex] = R.in_degree(vertex)
            if parent is None:
                children[vertex] = {vertex}
            else:
                children[vertex] = children[parent]
        else:
            children[vertex] = children[vertex] | children[parent]  # it surely already has an entry
        vertexRank[vertex] = vertexRank[vertex] - 1  # it is surely >= 1 as we must have gotten there from a parent
        if vertexRank[vertex] <= 0:  # for source it can actually go under 1
            for child in R.neighbors(vertex):
                sinkAccessibility(child, vertex)

    for sink in sinks:
        sinkAccessibility(sink, None)

    # We now solve the source cover problem using greedy algorithm
    cover: Set = set()
    covered: Set = set()

    while len(covered) < len(sinks):
        r_min = math.inf
        best_source = None
        discard = set()

        for source in sources:
            will_be_covered = len(children[source] - covered)
            if will_be_covered == 0:
                continue

            r_i = 1 / will_be_covered  # c_i = len(children[source])
            if r_i < r_min:
                best_source = source
                r_min = r_i

        sources = sources - discard
        covered = covered | children[best_source]
        cover.add(best_source)
        sources.remove(best_source)

    return cover
