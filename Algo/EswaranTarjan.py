import networkx as nx
from typing import List, Set


def eswaran_tarjan(G: nx.DiGraph):
    if len(G.nodes) <= 1:
        return set()

    marked: Set = set()
    unmarked: Set = set()

    isolated: List = []
    sources: Set = set()
    sinks: Set = set()

    for vertex in G.nodes:
        inDegree: int = G.in_degree(vertex)
        outDegree: int = G.out_degree(vertex)

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
    graph: nx.DiGraph

    if s > t:
        s, t = t, s
        sources, sinks = sinks, sources
        graph = G.reverse(copy=False)
    else:
        graph = G

    w = None
    sink_not_found = None

    v_list: List = []
    w_list: List = []

    def search(x):
        if x in unmarked:  # "x is unmarked"
            if x in sinks:  # "x is a sink"
                global w
                w = x
                global sink_not_found
                sink_not_found = False

            marked.add(x)  # mark x
            unmarked.remove(x)

            for y in graph.neighbors(x):
                if sink_not_found:
                    search(y)

    "initialize all nodes as unmarked"
    unmarked = set(graph.nodes)

    unmarked_sources: Set = unmarked.intersection(sources)
    while len(unmarked_sources) > 0:  # some source is unmarked
        v = unmarked_sources.pop()  # "choose some unmarked source v"
        w = None
        sink_not_found = True
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
        return {(e[1], e[0]) for e in A}
    else:
        return A
