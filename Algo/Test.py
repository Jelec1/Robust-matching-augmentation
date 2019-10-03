import os

from multiprocessing import Process
import time
import networkx as nx
T = nx.balanced_tree(2, 17, create_using=nx.DiGraph())

mean = 0
for i in range(10):

    start = time.time()
    x = set(nx.algorithms.traversal.dfs_preorder_nodes(T, 0))

    end1 = time.time() - start

    from utils.AuxiliaryAlgorithms import fast_dfs


    verts = set()
    # Defines action for fast_dfs, i.e. add current vertex
    def action_on_vertex(current_vertex):
        verts.add(current_vertex)
        return True


    # Action on neighbor, just continue with the neighbor
    def action_on_neighbor(neighbor):
        return True

    start = time.time()
    fast_dfs(T, 0, action_on_vertex, action_on_neighbor)


    end2 = time.time() - start

    mean += 0.1 * end2/end1

    print(mean)