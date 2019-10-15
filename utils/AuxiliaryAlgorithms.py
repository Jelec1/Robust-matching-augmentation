"""
Author: Tomas Jelinek
Last change: 18.9.2019

Description: Contains various auxiliary algorithms.
"""

import networkx as nx
from typing import Set, Dict
from networkx.utils.decorators import not_implemented_for
from networkx.utils.heaps import PairingHeap


@not_implemented_for('undirected')
def get_sources_sinks_isolated(G: nx.DiGraph) -> (Set, Set, Set):
    """

    Parameters
    ----------
    G : NetworkX DiGraph
       A directed graph.

    Returns
    -------
    Dict of sets with keys 'sources', 'sinks', 'isolated'

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

    result = sources, sinks, isolated

    return result


def bipartite_to_D(G: nx.Graph, A: Set, M:Dict = None) -> nx.DiGraph:
    """ Transforms a bipartite graph to D as defined in the paper How to secure matching against edge failure

    Parameters
    ----------
    G : NetworkX Graph
       A bipartite graph.
    A : Set
        A bipartition of G.
    M : Dict
        A perfect bipartite matching of G, if none is provided,
        it will be computed.
    Returns
    -------
    A NetworkX DiGraph D.
    """
    D: nx.DiGraph = nx.DiGraph()
    if M is None:
        M = nx.algorithms.bipartite.eppstein_matching(G, A)

    for u in M:  # Construction of D, iterate over all keys in M
        if u in A:  # Add all edges from A to D
            w = M[u]
            D.add_node(u)

            for uPrime in G.neighbors(w):  # Construct edges of D
                if uPrime != u:
                    D.add_edge(u, uPrime)
    return D


def fast_dfs(G: nx.Graph, starting_vertex, action_on_vertex, action_on_neighbor):
    """
    Parameters
    ----------
    G : NetworkX Graph
       A graph to perform DFS on.
    starting_vertex : A vertex to start on
    action_on_vertex -> bool
        function action_on_vertex(vertex, G: nx.Graph=None) -> bool
        Performs operation(s) on current vertex specified by the function.
        If fast_dfs should continue, expecting True,
        if fast_dfs should terminate returning current vertex, expecting False.

    action_on_neighbor -> bool
        function action_on_neighbor(vertex, G: nx.Graph=None) -> bool
        Performs operation(s) on neighbors of current vertex specified by the function.
        If fast_dfs should add also neighbor to the stack, expected True, otherwise False

    Returns
    -------
    Some current vertex or None

    Notes
    -----

    """
    stack = [starting_vertex]  # The initial vertex

    while len(stack) > 0:
        current_vertex = stack.pop()
        if not action_on_vertex(current_vertex):
            return current_vertex

        for neighbor in G[current_vertex]:
            visit_neighbor = action_on_neighbor(neighbor, current_vertex)
            if visit_neighbor:
                stack.append(neighbor)

    return None


def heapIncreaseValue(heap: PairingHeap, key, new_value):
    """
    Parameters
    ----------
    heap : PairingHeap
       A minimum heap implemented by networking that supports decrease key using new insert
    key
        A hashable identifier of object whose key should be decreased
    new_value
        New value of the object

    Notes
    -----
    Serves as a wrap-up of the increase key operation. For decrease, use just insert with new key
    """
    min_value = heap.min()
    heap.insert(key, min_value - 1)
    heap.pop()
    heap.insert(key, new_value)
