import networkx as nx
from typing import Dict, Set
from utils.AuxiliaryAlgorithms import get_sources_sinks_isolated, fast_dfs
from utils.RedBlackTree import RedBlackTree



def source_cover(D: nx.DiGraph, R = None) -> Set:
    import time
    start = time.time()

    sources, sinks, isolated = get_sources_sinks_isolated(D)
    sources = sources | isolated
    sinks = sinks | isolated

    if R is None:
        srh = time.time()
        R: nx.DiGraph = D.reverse(copy=False)
        print("-----Revertimg", time.time() - srh)
    children: Dict[object, Set] = {}
    vertexRank: Dict[object, int] = {}

    print("----Sources/sinks/isolated", time.time() - start)
    start = time.time()

    source = 0

    def action_on_vertex(vertex):
        return True

    def action_on_neighbor(vertex, parent):
        if vertex in sinks:
            children[source] = children[source] | {vertex}
        return True

    for source in sources:
        children[source] = {source}
        fast_dfs(D, source, action_on_vertex, action_on_neighbor)

    print("----Flattening D", time.time() - start)
    start = time.time()

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

    print("----Greedy set cover", time.time() - start)
    start = time.time()
    return cover
