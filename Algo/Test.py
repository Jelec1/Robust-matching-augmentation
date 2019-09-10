import networkx as nx
from Algo.BipartiteMatchingAugmentation import bipartite_matching_augmentation
import time


G = nx.path_graph(10)

H: nx.Graph = nx.induced_subgraph(G, {i for i in range(9)})

H.remove_node(5)



T: nx.Graph = nx.balanced_tree(2, 10)

for n in nx.algorithms.dfs_preorder_nodes(T, 0):
  if n % 10 == 0:
    T.remove_node(n)

A = [i for i in range(1000)]
B = [2*i for i in range(1000)]

start_time = time.time()
D = {}
for i in A:
  D[i] = 1
for i in B:
  if i in D:
    D[i] = D[i] + 1

C = set()
for i in D:
  if D[i] == 2:
    C.add(D[i])
end = time.time()
print("--- %s seconds ---" % (end - start_time))

start_time = time.time()
C = set(A).intersection(set(B))
end = time.time()
print("--- %s seconds ---" % (end - start_time))





# applicator(arr, x)