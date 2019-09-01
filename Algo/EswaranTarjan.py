import networkx as nx
from typing import List, Set
from networkx.utils.decorators import not_implemented_for

@not_implemented_for('undirected')
@not_implemented_for('multigraph')
def eswaran_tarjan(G: nx.DiGraph, is_condensation: bool = False):

    #if not G.is_directed():
    #    raise nx.NetworkXNotImplemented("G is not a directed graph")

    G_condensation: nx.DiGraph

    if not is_condensation:
        G_condensation = nx.algorithms.condensation(G)
    else:
        if not nx.algorithms.dag.is_directed_acyclic_graph(G):
            raise nx.HasACycle("G has a cycle, acyclic graph expected")
        G_condensation = G

    if len(G_condensation.nodes) <= 1:
        return set()

    unmarked: Set = set()

    isolated: List = []
    sources: Set = set()
    sinks: Set = set()

    for vertex in G_condensation.nodes:
        inDegree: int = G_condensation.in_degree(vertex)
        outDegree: int = G_condensation.out_degree(vertex)

        if inDegree == 0 and outDegree == 0:
            isolated.append(vertex)
        elif inDegree == 0:
            sources.add(vertex)
        elif outDegree == 0:
            sinks.add(vertex)

    s: int = len(sources)
    t: int = len(sinks)
    q: int = len(isolated)

    reverted = False

    if s > t:
        s, t = t, s
        sources, sinks = sinks, sources
        G_condensation = G_condensation.reverse(copy=False)

    v_list: List = []
    w_list: List = []

    def search(x):
        stack = [x]

        while len(stack) > 0:
            x = stack.pop()
            if x in unmarked:
                if x in sinks:
                    global w
                    w = x
                    break

                unmarked.remove(x)
                for y in G_condensation.neighbors(x):
                    if y in unmarked:
                        stack.append(y)

    # initialize all nodes as unmarked
    unmarked_sources: Set = (set(G_condensation.nodes)).intersection(sources)
    while len(unmarked_sources) > 0:  # some source is unmarked
        v = unmarked_sources.pop()  # "choose some unmarked source v"
        w = None
        search(v)
        if w is not None:
            v_list.append(v)
            w_list.append(w)

    p = len(v_list)

    v_list.extend(sources.difference(set(v_list)))
    w_list.extend(sinks.difference(set(w_list)))

    A: Set = set()

    for i in range(0, p - 1):
        A.add((w_list[i], v_list[i + 1]))

    for i in range(p, s):
        A.add((w_list[i], v_list[i]))

    if q == 0:
        if s == t:
            A.add((w_list[p - 1], v_list[0]))
        else:  # q = 0, s < t
            A.add((w_list[p - 1], w_list[s]))
            A.update({(w_list[i], w_list[i + 1]) for i in range(s, t - 1)})
    else:  # q > 0, s <= t
        A.add((w_list[p - 1], w_list[s + 1]))
        A.update({(w_list[i], w_list[i + 1]) for i in range(s, t - 1)})
        A.add((w_list[t - 1], isolated[0]))
        A.update({(isolated[i], isolated[i + 1]) for i in range(0, q - 1)})
        A.add((isolated[q - 1], v_list[0]))

    if reverted:
        return {(G_condensation.nodes[e[1]]['members'].pop(), G_condensation.nodes[e[0]]['members'].pop()) for e in A}
    else:
        return {(G_condensation.nodes[e[0]]['members'].pop(), G_condensation.nodes[e[1]]['members'].pop()) for e in A}
