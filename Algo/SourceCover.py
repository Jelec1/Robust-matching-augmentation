from math import inf
import networkx as nx
from typing import List, Dict, Set
from Algo.Util import get_sources_sinks_isolated


def sourceCover(D: nx.DiGraph) -> Set:

    sources, sinks, isolated = get_sources_sinks_isolated(D)

    sources = sources | isolated
    sinks = sinks | isolated

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
        r_min = inf
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
