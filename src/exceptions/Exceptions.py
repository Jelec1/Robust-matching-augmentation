"""
Author: Tomas Jelinek
Last change: 12.9.2019

Description: Implementation of exceptions relating to the bipartite matching augmentation algorithm.
"""
import networkx as nx


class bipartite_ghraph_not_augmentable_exception(nx.NetworkXException):
    """Exception raised if a bipartite graph cannot be augmented so that
    the graph admits a perfect matching even after a single arbitrary edge is removed."""
