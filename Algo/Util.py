import networkx as nx
from typing import List, Set
from networkx.utils.decorators import not_implemented_for


@not_implemented_for('undirected')
def getSourcesSinksIsolated(G: nx.DiGraph):
    """

    Parameters
    ----------
    G : NetworkX DiGraph
       A directed graph.

    Returns
    -------
    (source, sinks, isolated)
       Returns a triplet of sets (sources, sinks, isolated vertices) of G

    Notes
    -----
    A source is defined as a vertex with no incoming and at least one outcoming arc,
    a sink is a vertex with at least one incoming and no outcoming arc and
    an isolated vertex has neither incoming nor outcoming arc.

    """
    isolated: Set = set()
    sources: Set = set()
    sinks: Set = set()

    for vertex in G.nodes:
        inDegree: int = G.in_degree(vertex)
        outDegree: int = G.out_degree(vertex)

        if inDegree == 0 and outDegree == 0:
            isolated.add(vertex)
        elif inDegree == 0:
            sources.add(vertex)
        elif outDegree == 0:
            sinks.add(vertex)

    return sources, sinks, isolated

