"""
Author: Tomas Jelinek
Last change: 15.10.2019

Description: Implementation of the source cover algorithm proposed by
        BINDEWALD, Viktor; HOMMELSHEIM, Felix; MÜHLENTHALER, Moritz; SCHAUDT, Oliver.
        How to Secure Matchings Against Edge Failures. CoRR. 2018, vol. abs/1805.01299. Available from arXiv:
        1805.01299
"""

import networkx as nx
from typing import Dict, Set
from utils.AuxiliaryAlgorithms import get_sources_sinks_isolated, fast_traversal, heapDelete, heapIncreaseValue
from networkx.utils.heaps import PairingHeap


def source_cover(D: nx.DiGraph, critical_vertices: Set,
                 sourcesSinksIsolated: (Set, Set, Set) = None) -> Set:
    """
    Computes a log n approximation of the minimal cardinality set of sources such that each
    critical vertex is reachable.

    Parameters
    ----------
    D : NetworkX DiGraph
        A directed acyclic graph.
    critical_vertices : Set
        Set of critical vertices of D
    --R : NetworkX DiGraph
    --    Reversed graph D, optional.
    sourcesSinksIsolated : (Set, Set, Set)
        Set of sources, weak_sinks and isolated vertices of D.

    Returns
    -------
    cover : Set
        Set of sources that form a log n approximation cover of the critical vertices.

    References
    ----------
       [1]  BINDEWALD, Viktor; HOMMELSHEIM, Felix; MÜHLENTHALER, Moritz; SCHAUDT, Oliver.
        How to Secure Matchings Against Edge Failures. CoRR. 2018, vol. abs/1805.01299. Available from arXiv:
        1805.01299

    """
    import time
    start = time.time()

    if sourcesSinksIsolated is None:
        sources, sinks, isolated = get_sources_sinks_isolated(D)
    else:
        sources, sinks, isolated = sourcesSinksIsolated
    sources = sources | isolated  # We consider each isolated as a source
    # sinks = sinks | isolated  # We consider each isolated as a sink

    deleted_vertices = set()  # All vertices reachable from a critical vertex

    # weak_sinks = sinks & critical_vertices
    weak_sinks = critical_vertices

    children: Dict[object, Set] = {}  # Contains all reachable critical vertices from given source

    print("----Sources/weak_sinks/isolated", time.time() - start)
    start = time.time()

    def action_on_vertex_delete_reachable(vertex):
        return True

    def action_on_neighbor_delete_reachable(vertex, parent):
        neighbor_already_visited = vertex in deleted_vertices
        deleted_vertices.add(vertex)
        return not neighbor_already_visited

    for critical in critical_vertices:
        fast_traversal(D, critical, action_on_vertex_delete_reachable, action_on_neighbor_delete_reachable)

    weak_sinks = weak_sinks - deleted_vertices

    visited = set()

    def action_on_vertex_add_sinks(vertex):
        visited.add(vertex)
        if vertex in weak_sinks:
            children[source].add(vertex)
        return True

    def action_on_neighbor_add_sinks(vertex, parent):
        # Avoid processing the same vertex twice, which makes this traversal a DFS
        # Also, do not visit deleted vertices
        return vertex not in visited and vertex not in deleted_vertices

    for source in sources:
        visited = set()  # Set of visited vertices, to avoid processing twice
        children[source] = set()
        fast_traversal(D, source, action_on_vertex_add_sinks, action_on_neighbor_add_sinks)

    print("----Flattening D", time.time() - start)
    start = time.time()

    # Inverts the children table, i.e. assigns each source pointer on its "father" source
    fathers: Dict[object, Set] = {}
    for source in children:
        for sink in children[source]:
            if sink not in fathers:
                fathers[sink] = set()
            fathers[sink].add(source)

    cover: Set = set()  # Set of covered weak_sinks
    covered = 0  # Number of covered weak_sinks

    heap = PairingHeap()  # Minimum heap to choose the best vertex to be covered
    max_value = len(weak_sinks)  # Maximum possible size of set, used to simulate max heap via min heap
    for source in sources:  # Fill the heap, the value is number of weak_sinks it covers
        heap.insert(source, max_value - len(children[source]))

    while covered < len(weak_sinks):  # Until we cover all weak_sinks

        best_source = heap.pop()[0]  # Pop source covering the most uncovered weak_sinks
        cover.add(best_source)
        covered += len(children[best_source])

        updated_sources: Set = set()
        for sink in children[best_source]:  # For each newly covered sink
            for source in fathers[sink] - {best_source}:  # Update the info about sources containing covered sink
                updated_sources.add(source)
                children[source].remove(sink)  # Remove it from the set of weak_sinks it covers
            fathers.pop(sink)  # Remove covered sink from the fathers set

        children.pop(best_source)  # Remove best source from the source table

        for source in updated_sources:  # Now update info about all updated sources
            if len(children[source]) > 0:  # If still covers anything, update (increase) the value in min-heap
                heapIncreaseValue(heap, source, max_value - len(children[source]))
            else:  # If given source does not cover any new, delete it from the heap
                heapDelete(heap, source)

    print("----Greedy set cover", time.time() - start)
    start = time.time()
    return cover
