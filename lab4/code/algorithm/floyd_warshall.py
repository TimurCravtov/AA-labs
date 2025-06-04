import networkx as nx

def floyd_warshall(graph: nx.Graph) -> dict:
    nodes = list(graph.nodes)
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}
    
    for node in nodes:
        dist[node][node] = 0
    
    for u, v, data in graph.edges(data=True):
        weight = data['weight']
        dist[u][v] = weight
        dist[v][u] = weight  # if undirected

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist

