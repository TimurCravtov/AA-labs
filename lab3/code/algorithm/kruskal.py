import networkx as nx


def min_span_tree_kruskal(G: nx.Graph) -> nx.Graph:
    if not G.nodes:
        return nx.Graph()

    # Create a list of edges with weights
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])

    parent = {node: node for node in G.nodes}
    rank = {node: 0 for node in G.nodes}

    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])  # Path compression
        return parent[v]

    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            elif rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                rank[root_u] += 1
            return True
        return False

    mst = nx.Graph()

    for u, v, data in edges:
        if union(u, v):
            mst.add_edge(u, v, weight=data['weight'])

    return mst
