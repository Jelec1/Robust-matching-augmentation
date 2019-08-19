class Edge:

    pass


class DirectedEdge(Edge):
    def __init__(self, u, v):
        self.e = (u, v)


class UndirectedEdge(Edge):
    def __init__(self, u , v):
        self.e = {u, v}