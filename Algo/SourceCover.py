import networkx as nx
from typing import Dict, Set
from utils.AuxiliaryAlgorithms import get_sources_sinks_isolated
from utils.RedBlackTree import RedBlackTree


def source_cover(D: nx.DiGraph) -> Set:
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

    import time
    start_time = time.time()

    for sink in sinks:
        sinkAccessibility(sink, None)

    # We now solve the source cover problem using greedy algorithm

    fathers: Dict[object, Set] = {}
    for sink in children:
        for source in children[sink]:
            if sink not in fathers:
                fathers[sink] = set()
            fathers[sink].add(source)

    cover: Set = set()
    covered = 0

    red_black_tree = RedBlackTree()
    for source in sources:
        red_black_tree.add(len(children[source]), source)

    while covered < len(sinks):

        best_source = red_black_tree.extractMax()
        cover.add(best_source)
        covered += len(children[best_source])

        updated_sources: Dict = {}
        for sink in children[best_source]:
            for source in fathers[sink] - {best_source}:
                if source not in updated_sources:
                    updated_sources[source] = len(children[updated_sources])
                children[source].remove(sink)
            fathers.pop(sink)

        red_black_tree.remove(len(children[best_source]), best_source)
        children.pop(best_source)

        for source in updated_sources:
            red_black_tree.remove(updated_sources[source], source)
            if len(children[updated_sources]) > 0:
                red_black_tree.add(len(children[updated_sources]), source)

    if len(D.nodes) > 100:
        print("---source cover %s seconds ---" % (time.time() - start_time))
    return cover
