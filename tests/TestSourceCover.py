"""
Author: Tomas Jelinek
Last change: 30.11.2019

Description: tests for the source_cover(G) function
"""

import networkx as nx
from src.algo.SourceCover import source_cover
from nose.tools import assert_set_equal, assert_true
from typing import Set


class TestSourceCover:

    def test_single_critical(self):
        # tests D consisting of single critical vertex
        # Source cover expected to cover it
        D: nx.DiGraph = nx.DiGraph()
        D.add_node(0)
        cover = source_cover(D, {0})
        assert_set_equal(cover, {0})

    def test_no_critical(self):
        # tests D consisting of single directed edge
        # Source cover expected to not cover it
        D: nx.DiGraph = nx.DiGraph()
        D.add_node(0)
        cover = source_cover(D, set())
        assert_set_equal(cover, set())

    def test_child_critical(self):
        # tests D consisting of non-critical 0 and path to critical 4.
        # Source cover is expected to be {0}
        D: nx.DiGraph = nx.path_graph(5, nx.DiGraph())
        D.add_edge(0, 1)
        cover = source_cover(D, {4})
        assert_set_equal(cover, {0})

    def test_child_non_critical(self):
        # tests D consisting of non-critical path.
        # Source cover is expected to be empty
        D: nx.DiGraph = nx.DiGraph()
        D.add_edge(0, 1)
        cover = source_cover(D, set())
        assert_set_equal(cover, set())

    def test_tree_leafs_critical(self):
        # tests D to be a tree, only leafs are critical
        # Source cover is expected to be {0} - the root
        D: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
        critical: Set = {node for node in D.nodes if D.out_degree(node) == 0}
        cover: Set = source_cover(D, critical)
        assert_set_equal(cover, {0})

    def test_tree_leafs_critical_and_isolated(self):
        # tests D to be a tree, only leafs are critical
        # and set of isolated
        # Source cover is expected to be  root(D1) | isolated
        D1: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
        D2: nx.DiGraph = nx.DiGraph()
        D2.add_nodes_from({i for i in range(100)})
        D = nx.compose(D1, D2)
        critical: Set = {node for node in D.nodes if D.in_degree(node) == 0}
        cover: Set = source_cover(D, critical)
        assert_set_equal(cover, critical)

    def test_two_disjoint_trees_leafs_critical(self):
        # tests two trees, only leafs are critical
        # Source cover is expected to be {0} - the root
        D1: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
        D2: nx.DiGraph = nx.balanced_tree(2, 6, nx.DiGraph())
        D = nx.compose(D1, D2)
        critical: Set = {node for node in D.nodes if D.out_degree(node) == 0}
        cover: Set = source_cover(D, critical)
        assert_set_equal(cover, {node for node in D.nodes if D.in_degree(node) == 0})  # Only roots form cover

    def test_tree_leafs_non_critical(self):
        # tests D to be a tree, no vertices are critcal
        # Source cover is expected to be empty
        D: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
        cover: Set = source_cover(D, set())
        assert_set_equal(cover, set())

    def test_tree_all_critical(self):
        # tests D to be a tree, all vertices are critical
        # Source cover is expected to be the root
        # tests correct functionality of deletion of vertices
        # reachable from a critical vertex
        D: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
        cover: Set = source_cover(D, set(D.nodes))
        assert_set_equal(cover, {0})

    def test_tree_all_critical_decoy(self):
        # tests D to be a tree, all vertices are critical
        # Source cover is expected to be the root
        # tests correct functionality of deletion of vertices
        # reachable from a critical vertex
        # There is also one "decoy" - a non-critical vertex 100
        # that covers two leafs. However, after the deletion,
        # the vertex 100 does not cover any critical vertex
        # any more. Hence, it should not be in the cover.
        D: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
        D.add_edges_from({(100, 50), (100, 51)})
        cover: Set = source_cover(D, set(D.nodes) - {100})
        assert_set_equal(cover, {0})

    def test_tree_multiple_sources_leafs_critical(self):
        # tests D to be a tree, only leafs are critical
        # There are multiple sources in the graphs, including two
        # covering all the vertices. However, the optimal solution is
        # still of size 1. tests if it correctly does not consider these
        # additional source.
        D: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
        D.add_edges_from({(65, 1), (65, 2), (66, 15), (65, 29), (66, 38), (67, 58)})
        critical = {node for node in D.nodes if D.out_degree(node) == 0}
        cover = source_cover(D, critical)
        assert_true(cover == {0} or cover == {65})  # Only two correct options

    def test_tree_multiple_sources_tree_critical(self):
        # tests D to be a tree, whole tree is critical
        # There are multiple sources in the graphs, including two
        # covering all the vertices. However, the optimal solution is
        # still of size 1. In addition to test_tree_multiple_sources_leafs_critical(),
        # this test also tests correctness of the deletion procedure.
        # If it proceeds correctly, it does not consider the newly added sources
        # as critical sinks, so the solution is still of size 1.
        D: nx.DiGraph = nx.balanced_tree(2, 5, nx.DiGraph())
        critical = set(D.nodes)
        D.add_edges_from({(65, 1), (65, 2), (66, 15), (65, 29), (66, 38), (67, 58)})
        cover = source_cover(D, critical)
        assert_true(cover == {0})  # All others are reachable from a critical vertex, so this is only viable option.

    def test_not_covering_non_critical(self):
        # Test for unbounded approximation factor as discussed
        # in section 2.1 the thesis. The optimal solution is 1. We use the
        # minimal solution. Expected source cover is of length 1 if it works correctly.
        D: nx.DiGraph = nx.DiGraph()
        D.add_nodes_from(["s_1,2", "s_3,4", "s_5,6", "t_1", "t_2,3", "t_4,5", "t_6,7", "t_8,9"])
        D.add_edges_from({
            ("s_1,2", "t_1"), ("s_3,4", "t_1"), ("s_5,6", "t_1"), ("s_3,4", "t_2,3"), ("s_3,4", "t_4,5"),
            ("s_5,6", "t_6,7"), ("s_5,6", "t_8,9")
        })
        cover = source_cover(D, {"t_1"})
        assert_true(len(cover) == 1)
