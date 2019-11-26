"""
Author: Tomas Jelinek
Last change: 27.11.2019

Description: Tests for the source_tarjan(G) function
"""

import networkx as nx
from Algo.BipartiteMatchingAugmentation import source_cover
from nose.tools import assert_set_equal, assert_raises, assert_false, assert_true
from utils.AuxiliaryAlgorithms import get_sources_sinks_isolated
from collections import Set


def test_single_critical():
    # Tests D consisting of single critical vertex
    # Source cover expected to cover it
    D: nx.DiGraph = nx.DiGraph()
    D.add_node(0)
    cover = source_cover(D, {0})
    assert_set_equal(cover, {0})


def test_no_critical():
    # Tests D consisting of single directed edge
    # Source cover expected to not cover it
    D: nx.DiGraph = nx.DiGraph()
    D.add_node(0)
    cover = source_cover(D, set())
    assert_set_equal(cover, set())


def test_child_critical():
    # Tests D consisting of non-critical 0 connected to critical 1
    # Source cover is expected to be {0}
    D: nx.DiGraph = nx.DiGraph()
    D.add_edge(0, 1)
    cover = source_cover(D, {1})
    assert_set_equal(cover, {0})


def test_child_non_critical():
    # Tests D consisting of non-critical 0 connected to critical 1
    # Source cover is expected to be empty
    D: nx.DiGraph = nx.DiGraph()
    D.add_edge(0, 1)
    cover = source_cover(D, set())
    assert_set_equal(cover, set())


def test_tree_leafs_critical():
    # Tests D to be a tree, only leafs are critical
    # Source cover is expected to be {0} - the root
    D: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
    critical = {node for node in D.nodes if D.out_degree(node) == 0}
    cover = source_cover(D, critical)
    assert_set_equal(cover, {0})


def test_tree_leafs_non_critical():
    # Tests D to be a tree, no vertices are critcal
    # Source cover is expected to be empty
    D: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
    cover = source_cover(D, set())
    assert_set_equal(cover, set())






"""
gadfgasdfg
asdfadsfgafdgadfgasdgasd

fgasdgasd

import  time
import random

for i in range(1):
    start = time.time()
    G: nx.DiGraph = nx.generators.classic.balanced_tree(2, 16, create_using=nx.DiGraph)
    print(time.time() - start)
    # G = nx.algorithms.traversal.dfs_tree(G, 0)
    sources = set()
    a = len(G)

    print("DFS------")
    start = time.time()
    nx.algorithms.traversal.dfs_tree(G, 0)
    print(time.time() - start)
    print("DFS------")

    for i in range(len(G) + 1, len(G) + 1 + 100):
        j = random.randint(1, a - 1)
        G.add_edge(i, j)
        sources.add(i)
    start = time.time()
    torem = set()
    for n in G:
        r = random.randint(0, 100)
        if r <= 1:
            torem.add(n)
    G.remove_nodes_from(torem)
    for u in range(1, 100):
        p = r = random.randint(0, len(G) - 10)
        s = r = random.randint(p + 1, len(G) - 1)
        G.add_edge(p, s)
    print(len(G))
    res = source_cover(G, {n for n in G if G.in_degree(n) == 0}, {n for n in G if G.out_degree(n) == 0})
    print(time.time() - start)

    print(res)
    print("---------------------")
"""