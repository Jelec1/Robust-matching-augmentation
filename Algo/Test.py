import networkx as nx


G = nx.DiGraph()
G.add_nodes_from({'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'})
G.add_edges_from({('A', 'B'),
                 ('B', 'D'),
                 ('D', 'F'),
                 ('F', 'H'),
                 ('A', 'C'),
                 ('C', 'E'),
                 ('E', 'G'),
                 ('G', 'H'),
                 ('D', 'A')})


print(nx.dfs_tree(G, source = 'A'))

print(nx.drawing.nx_agraph.to_agraph )

