import networkx as nx
from typing import Dict, Set
from utils.AuxiliaryAlgorithms import get_sources_sinks_isolated, fast_dfs, heapDelete, heapIncreaseValue
from utils.RedBlackTree import RedBlackTree
from networkx.utils.heaps import PairingHeap


def source_cover(D: nx.DiGraph, R: nx.DiGraph = None, sourcesSinksIsolated: (Set, Set, Set) = None) -> Set:
    import time
    start = time.time()

    if sourcesSinksIsolated is None:
        sources, sinks, isolated = get_sources_sinks_isolated(D)
    else:
        sources, sinks, isolated = sourcesSinksIsolated
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
    reachableSinks = set()

    def action_on_vertex(vertex):
        if vertex in sinks:
            children[source] = children[source] | {vertex}
            reachableSinks.add(vertex)
            return False
        return True

    def action_on_neighbor(vertex, parent):
        return True

    for source in sources:
        children[source] = set()
        fast_dfs(D, source, action_on_vertex, action_on_neighbor)

    print("----Flattening D", time.time() - start)
    start = time.time()

    # We now solve the source cover problem using greedy algorithm
    sinks = reachableSinks

    #fathers = {sink: source for source, sink in children.items()}
    fathers: Dict[object, Set] = {}
    for source in children:
        for sink in children[source]:
            if sink not in fathers:
                fathers[sink] = set()
            fathers[sink].add(source)

    cover: Set = set()
    covered = 0

    heap = PairingHeap()
    max_value = len(sinks)
    red_black_tree = RedBlackTree()
    for source in sources:
        # red_black_tree.add(len(children[source]), source)
        heap.insert(source, max_value - len(children[source]))

    while covered < len(sinks):

        #best_source = red_black_tree.extractMax()
        best_source = heap.pop()[0]
        cover.add(best_source)
        covered += len(children[best_source])

        updated_sources: Dict = {}
        for sink in children[best_source]:
            for source in fathers[sink] - {best_source}:
                children[source].remove(sink)
                updated_sources[source] = len(children[source])
            fathers.pop(sink)

        # red_black_tree.remove(len(children[best_source]), best_source)
        children.pop(best_source)

        for source in updated_sources:
            # red_black_tree.remove(updated_sources[source], source)
            if len(children[source]) > 0:
                # red_black_tree.add(len(children[source]), source)
                heapIncreaseValue(heap, source, max_value - len(children[source]))
            else:
                heapDelete(heap, source)

    print("----Greedy set cover", time.time() - start)
    start = time.time()
    return cover
