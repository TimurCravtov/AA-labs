class Edge:
    def __init__(self, start: str, end: str, weight: int):
        self.start = start
        self.end = end
        self.weight = weight
    def __str__(self):
        return f"Edge {self.start} -> {self.end}, {self.weight}"
    def __repr__(self):
        return f"Edge({self.start}, {self.end}, {self.weight})"
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.start == other.start and self.end == other.end and self.weight == other.weight
    

class Graph:
    def __init__(self,  edgesList: list[Edge], verticesList: list[str] = None,):
        self.verticesList = verticesList if verticesList is not None else list(set([edge.start for edge in edgesList] + [edge.end for edge in edgesList]))
        self.edgesList = edgesList

    def to_adjacency_list(self):
        adjacency_list = {vertex: [] for vertex in self.verticesList}
        for edge in self.edgesList:
            adjacency_list[edge.start].append((edge.end, edge.weight))
            adjacency_list[edge.end].append((edge.start, edge.weight))
        return adjacency_list

    def __str__(self):
        return f"Graph with vertices: {self.verticesList} and edges: {self.edgesList}"
