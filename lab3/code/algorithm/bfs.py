import networkx as nx
import matplotlib.pyplot as plt
import random
import time


def bfs(graph: nx.Graph, start_node: int) -> list:
    """Perform BFS on the graph starting from the given node."""
    visited = set()
    queue = [start_node]
    bfs_order = []

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            bfs_order.append(node)
            # Add neighbors to queue
            queue.extend(graph.neighbors(node))

    return bfs_order

