"""
Author: Tomas Jelinek
Last change: 18.9.2019

Description: Contains various auxiliary algorithms.
"""

import networkx as nx
from typing import Set
from networkx.utils.decorators import not_implemented_for


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
            visit_neighbor = action_on_neighbor(neighbor)
            if visit_neighbor:
                stack.append(neighbor)

    return None
