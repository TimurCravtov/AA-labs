import networkx as nx
import heapq


def min_span_tree_prim(G: nx.Graph) -> nx.Graph:
    if not G.nodes:
        return nx.Graph()

    mst = nx.Graph()
    visited = set()
    min_heap = []

    # Start from an arbitrary node
    start_node = list(G.nodes)[0]
    visited.add(start_node)

    # Push all edges from the start node into the heap
    for neighbor in G.neighbors(start_node):
        weight = G[start_node][neighbor]['weight']
        heapq.heappush(min_heap, (weight, start_node, neighbor))

    while min_heap and len(visited) < G.number_of_nodes():
        weight, u, v = heapq.heappop(min_heap)

        if v not in visited:
            visited.add(v)
            mst.add_edge(u, v, weight=weight)

            for neighbor in G.neighbors(v):
                if neighbor not in visited:
                    heapq.heappush(min_heap, (G[v][neighbor]['weight'], v, neighbor))

    return mst
