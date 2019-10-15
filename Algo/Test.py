import os

from multiprocessing import Process
import time
import networkx as nx
T = nx.balanced_tree(2, 17, create_using=nx.DiGraph())

def negatebitstring(str):
    new = ""

    for bit in str:
        if bit == "0":
            new = new + "1"
        else:
            new = new + "0"

    return new


def RM(x,y):

    if y == 1:
        return ["00","01","10","11"]

    x =RM(x, y-1)

    left = [a + a for a in x]
    right = [a + negatebitstring(a) for a in x]

    print(left, right)
    return left + right

RM(1, 4)


"""
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
    
"""