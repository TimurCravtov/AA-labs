import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from algorithm.dijkstra import dijkstra
from algorithm.floyd_warshall import floyd_warshall

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

def run_benchmark_dijkstra(graph):
    start_time = time.perf_counter()
    dijkstra(graph, list(graph.nodes)[0])
    return time.perf_counter() - start_time

def run_benchmark_floyd(graph):
    start_time = time.perf_counter()
    floyd_warshall(graph)
    return time.perf_counter() - start_time

def benchmark_scenario(scenario_params):
    num_nodes, num_edges, repetitions = scenario_params
    dijkstra_times = []
    floyd_times = []

    for _ in range(repetitions):
        G = generate_connected_weighted_graph(num_nodes, num_edges)
        dijkstra_times.append(run_benchmark_dijkstra(G))
        floyd_times.append(run_benchmark_floyd(G))
    
    return (np.mean(dijkstra_times), np.mean(floyd_times))

def main():
    random.seed(42)
    np.random.seed(42)

    repetitions = 3
    max_workers = 4
    nodes_range = np.arange(100, 600, 100)
    
    sparse_params = [(n, int(n * 1.5), repetitions) for n in nodes_range]
    dense_params = [(n, int(n * (n - 1) * 0.5 * 0.9), repetitions) for n in nodes_range]  # 90% dense

    def run_all(params):
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(benchmark_scenario, p) for p in params]
            ordered = [f.result() for f in as_completed(futures)]
        return ordered

    sparse_results = run_all(sparse_params)
    dense_results = run_all(dense_params)

    # Sort by node count
    sparse = list(zip(nodes_range, sparse_results))
    dense = list(zip(nodes_range, dense_results))
    sparse.sort(key=lambda x: x[0])
    dense.sort(key=lambda x: x[0])

    x_vals = [p[0] for p in sparse]
    dijkstra_sparse = [p[1][0] for p in sparse]
    dijkstra_dense = [p[1][0] for p in dense]
    floyd_sparse = [p[1][1] for p in sparse]
    floyd_dense = [p[1][1] for p in dense]

    # Plot Dijkstra
    plt.figure(figsize=(10, 5))
    plt.plot(x_vals, dijkstra_sparse, marker='o', label="Sparse")
    plt.plot(x_vals, dijkstra_dense, marker='s', label="Dense")
    plt.title("Dijkstra: Sparse vs Dense Graphs")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("dijkstra_sparse_dense.png", dpi=300)

    # Plot Floyd-Warshall
    plt.figure(figsize=(10, 5))
    plt.plot(x_vals, floyd_sparse, marker='o', label="Sparse")
    plt.plot(x_vals, floyd_dense, marker='s', label="Dense")
    plt.title("Floyd-Warshall: Sparse vs Dense Graphs")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("floyd_sparse_dense.png", dpi=300)

if __name__ == "__main__":
    main()
