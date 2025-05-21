import networkx as nx
import matplotlib.pyplot as plt
import random
import time


def dfs(graph: nx.Graph, start_node: int) -> list:

    visited = set()
    stack = [start_node]
    dfs_order = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            dfs_order.append(node)
            # Add neighbors to stack in reverse order for correct DFS order
            stack.extend(reversed(list(graph.neighbors(node))))

    return dfs_order

