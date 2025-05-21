import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import numpy as np

from algorithm.dfs import dfs
from algorithm.bfs import bfs

def generate_connected_weighted_graph(num_nodes: int, num_edges: int, weight_range=(1, 10)) -> nx.Graph:
    if num_edges < num_nodes - 1:
        raise ValueError("Number of edges must be at least (num_nodes - 1) for connectivity.")
    if num_edges > num_nodes * (num_nodes - 1) // 2:
        raise ValueError("Too many edges for the number of nodes.")

    G = nx.complete_graph(num_nodes)
    edge_weights = {(u, v): random.random() for u, v in G.edges()}
    nx.set_edge_attributes(G, edge_weights, 'weight')
    T = nx.minimum_spanning_tree(G)
    G = T.copy()

    remaining_edges = num_edges - (num_nodes - 1)
    all_possible_edges = list(nx.non_edges(G))

    if remaining_edges > 0 and all_possible_edges:
        selected_edges = random.sample(all_possible_edges, min(remaining_edges, len(all_possible_edges)))
        G.add_edges_from(selected_edges)

    mapping = {i: f'v{i+1}' for i in range(num_nodes)}
    G = nx.relabel_nodes(G, mapping)

    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(*weight_range)

    return G

def run_traversal_benchmark(algorithm, graph, start_node):
    start_time = time.perf_counter()
    algorithm(graph, start_node)
    return time.perf_counter() - start_time

def benchmark_traversals(num_nodes, num_edges, repetitions):
    dfs_times = []
    bfs_times = []

    for _ in range(repetitions):
        G = generate_connected_weighted_graph(num_nodes, num_edges)
        start = list(G.nodes())[0]
        dfs_times.append(run_traversal_benchmark(dfs, G, start))
        bfs_times.append(run_traversal_benchmark(bfs, G, start))

    return (np.mean(dfs_times), np.mean(bfs_times))

def main():
    random.seed(42)
    np.random.seed(42)

    nodes = [10, 50, 100, 200, 300, 600, 1000]
    edge_density = 1.5
    repetitions = 5

    dfs_results = []
    bfs_results = []

    for n in nodes:
        e = int(n * edge_density)
        dfs_time, bfs_time = benchmark_traversals(n, e, repetitions)
        dfs_results.append(dfs_time)
        bfs_results.append(bfs_time)

    plt.plot(nodes, dfs_results, label='DFS', marker='o')
    plt.plot(nodes, bfs_results, label='BFS', marker='s')
    plt.xlabel("Number of Nodes")
    plt.ylabel("Time (s)")
    plt.title("DFS vs BFS Traversal Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("traversal_benchmark.png", dpi=300)

if __name__ == "__main__":
    main()
