import networkx as nx
from typing import List, Set
from networkx.utils.decorators import not_implemented_for
from Algo.Util import getSourcesSinksIsolated


@not_implemented_for('undirected')
@not_implemented_for('multigraph')
def eswaran_tarjan(G: nx.DiGraph, is_condensation: bool = False) -> Set:
    """Returns a set of edges A such that G(V, E + A) is strongly connected.

    Parameters
    ----------
    G : NetworkX DiGraph
       A directed graph.

    is_condensation : bool
        Generic value False, True if G has no non-trivial strongly connected
        component, which will be checked. If G has a strongly connected component,
        exception HasACycle will be raised. If the parameter is False,
        strongly connected components will be computed.

    Returns
    -------
    A : Set
       Set of directed edges (u, v) such that G(V, E + A) is strongly connected

    Raises
    ------
    NetworkX.NotImplemented:
        If G is undirected or a multigraph.
    NetworkX.HasACycle:
        If G has a cycle and is_condensation=True

    Notes
    -----
    Modified version of Eswaran and Tarjan's algorithm https://epubs.siam.org/doi/abs/10.1137/0205044
    and it's correction due to S. Raghavan https://link.springer.com/chapter/10.1007/0-387-23529-9_2

    """

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

    sourcesSinksIsolated = getSourcesSinksIsolated(G_condensation)

    sources: Set = sourcesSinksIsolated[0]
    sinks: Set = sourcesSinksIsolated[1]
    isolated: Set = sourcesSinksIsolated[2]

    s: int = len(sources)  # Number of sinks
    t: int = len(sinks)  # Number ou sources
    q: int = len(isolated)  # Number of isolated vertices

    reverted = False

    if s > t:
        reverted = True
        s, t = t, s
        sources, sinks = sinks, sources
        G_condensation = G_condensation.reverse(copy=False)

    v_list: List = []
    w_list: List = []

    def search(x):
        stack = [x]
        unmarked.discard(x)

        while len(stack) > 0:
            x = stack.pop()
            unmarked.discard(x)
            # if x in unmarked:
            if x in sinks:
                return x

            # unmarked.remove(x)
            for y in G_condensation.neighbors(x):
                if y in unmarked:
                    # unmarked.discard(y)
                    stack.append(y)

        return None

    unmarked = set(G_condensation.nodes)
    # initialize all nodes as unmarked
    unmarked_sources: Set = (set(G_condensation.nodes)).intersection(sources)
    while len(unmarked_sources) > 0:  # some source is unmarked
        v = unmarked_sources.pop()  # "choose some unmarked source v"
        w = search(v)
        if w is not None:
            v_list.append(v)
            w_list.append(w)

    p: int = len(v_list)

    v_list.extend(sources.difference(set(v_list)))
    w_list.extend(sinks.difference(set(w_list)))

    v_list = list(map(lambda x: G_condensation.nodes[x]['members'].pop(), v_list))
    w_list = list(map(lambda x: G_condensation.nodes[x]['members'].pop(), w_list))
    x_list = list(map(lambda x: G_condensation.nodes[x]['members'].pop(), isolated))

    A: Set = set()

    for i in range(0, p - 1):  # Covers (w_0, v_1) ... (w_p-2, v_p-1)
        A.add((w_list[i], v_list[i+1]))

    for i in range(p, s):  # Covers (w_p, v_p) ... (w_s-1, v_s-1)
        A.add((w_list[i], v_list[i]))

    for i in range(s, t - 1):  # Covers (w_s, w_s+1) ... (w_t-2, w_t-1)
        A.add((w_list[i], w_list[i+1]))

    for i in range(0, q - 1):  # Covers (x_0, x_1) ... (x_q-2, x_q-1)
        A.add((x_list[i], x_list[i+1]))

    if p == 0:  # This also ensures that s == t == 0 and q > 1
        A.add((x_list[q-1], x_list[0]))  # Covers (x_q-1, x_0) closing the cycle
    else:  # p > 0
        if s == t:
            if q == 0:
                A.add((w_list[p - 1], v_list[0]))  # Covers (w_p-1, v_0) closing the cycle
            else:  # q > 0
                A.add((w_list[p - 1], x_list[0]))  # Covers (w_p-1, x_0)
                A.add((x_list[q - 1], v_list[0]))  # Covers (x_q-1, v_0) closing the cycle
        else:  # t > s
            A.add((w_list[p - 1], w_list[s]))  # Covers (w_p-1, w_s)
            if q == 0:
                A.add((w_list[t - 1], v_list[0]))  # Covers (w_t-1, v_0)
            else:  # q > 0
                A.add((w_list[t - 1], x_list[0]))  # Covers (w_t-1, x_0)
                A.add((x_list[q - 1], v_list[0]))  # Covers (x_q-1, v_0) closing the cycle

    if reverted:
        A = set(map(lambda e: (e[1], e[0]), A))

    return A
