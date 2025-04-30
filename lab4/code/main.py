import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from algorithm.kruskal import min_span_tree_kruskal
from algorithm.prim import min_span_tree_prim

def generate_connected_weighted_graph(num_nodes: int, num_edges: int, weight_range=(1, 10)) -> nx.Graph:
    if num_edges < num_nodes - 1:
        raise ValueError("Number of edges must be at least (num_nodes - 1) for connectivity.")
    if num_edges > num_nodes * (num_nodes - 1) // 2:
        raise ValueError("Too many edges for the number of nodes.")

    while True:
        G = nx.gnm_random_graph(num_nodes, num_edges)
        if nx.is_connected(G):
            break

    mapping = {i: f'v{i+1}' for i in range(num_nodes)}
    G = nx.relabel_nodes(G, mapping)

    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(*weight_range)

    return G

def measure_execution_time(algorithm, G):
    start_time = time.perf_counter()
    algorithm(G)
    return time.perf_counter() - start_time

# Experiment parameters
random.seed(42)
repetitions = 3

# Scenario 1: Increasing vertices, fixed edge density
nodes_range = list(range(10, 51, 10))
edge_density = 1.5
kruskal_times_1 = []
prim_times_1 = []
for n in nodes_range:
    e = int(n * edge_density)
    kruskal_total = 0
    prim_total = 0
    for _ in range(repetitions):
        G = generate_connected_weighted_graph(n, e)
        kruskal_total += measure_execution_time(min_span_tree_kruskal, G)
        prim_total += measure_execution_time(min_span_tree_prim, G)
    kruskal_times_1.append(kruskal_total / repetitions)
    prim_times_1.append(prim_total / repetitions)

# Scenario 2: Increasing edges, fixed vertices
fixed_nodes = 30
max_edges = fixed_nodes * (fixed_nodes - 1) // 2
edge_range = list(range(fixed_nodes - 1, max_edges, max_edges // 5))
kruskal_times_2 = []
prim_times_2 = []
for e in edge_range:
    kruskal_total = 0
    prim_total = 0
    for _ in range(repetitions):
        G = generate_connected_weighted_graph(fixed_nodes, e)
        kruskal_total += measure_execution_time(min_span_tree_kruskal, G)
        prim_total += measure_execution_time(min_span_tree_prim, G)
    kruskal_times_2.append(kruskal_total / repetitions)
    prim_times_2.append(prim_total / repetitions)

# Scenario 3: Dense graphs
nodes_range_dense = list(range(10, 51, 10))
kruskal_times_3 = []
prim_times_3 = []
for n in nodes_range_dense:
    e = n *2 # Simplified dense graph
    kruskal_total = 0
    prim_total = 0
    for _ in range(repetitions):
        G = generate_connected_weighted_graph(n, e)
        kruskal_total += measure_execution_time(min_span_tree_kruskal, G)
        prim_total += measure_execution_time(min_span_tree_prim, G)
    kruskal_times_3.append(kruskal_total / repetitions)
    prim_times_3.append(prim_total / repetitions)

# Scenario 4: Sparse graphs
nodes_range_sparse = list(range(10, 51, 10))
kruskal_times_4 = []
prim_times_4 = []
for n in nodes_range_sparse:
    e = n
    kruskal_total = 0
    prim_total = 0
    for _ in range(repetitions):
        G = generate_connected_weighted_graph(n, e)
        kruskal_total += measure_execution_time(min_span_tree_kruskal, G)
        prim_total += measure_execution_time(min_span_tree_prim, G)
    kruskal_times_4.append(kruskal_total / repetitions)
    prim_times_4.append(prim_total / repetitions)

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Subgraph 1
axs[0, 0].plot(nodes_range, kruskal_times_1, label="Kruskal", marker='o')
axs[0, 0].plot(nodes_range, prim_times_1, label="Prim", marker='s')
axs[0, 0].set_title("Edge Density (edges = nodes * 1.5)")
axs[0, 0].set_xlabel("Vertices")
axs[0, 0].set_ylabel("Time (s)")
axs[0, 0].legend()
axs[0, 0].grid(True)

# Subgraph 2
axs[0, 1].plot(edge_range, kruskal_times_2, label="Kruskal", marker='o')
axs[0, 1].plot(edge_range, prim_times_2, label="Prim", marker='s')
axs[0, 1].set_title(f"Fixed Vertices (n = {fixed_nodes})")
axs[0, 1].set_xlabel("Edges")
axs[0, 1].set_ylabel("Time (s)")
axs[0, 1].legend()
axs[0, 1].grid(True)

# Subgraph 3
axs[1, 0].plot(nodes_range_dense, kruskal_times_3, label="Kruskal", marker='o')
axs[1, 0].plot(nodes_range_dense, prim_times_3, label="Prim", marker='s')
axs[1, 0].set_title("Dense Graphs (edges = nodes * 2)")
axs[1, 0].set_xlabel("Vertices")
axs[1, 0].set_ylabel("Time (s)")
axs[1, 0].legend()
axs[1, 0].grid(True)

# Subgraph 4
axs[1, 1].plot(nodes_range_sparse, kruskal_times_4, label="Kruskal", marker='o')
axs[1, 1].plot(nodes_range_sparse, prim_times_4, label="Prim", marker='s')
axs[1, 1].set_title("Sparse Graphs (edges = nodes)")
axs[1, 1].set_xlabel("Vertices")
axs[1, 1].set_ylabel("Time (s)")
axs[1, 1].legend()
axs[1, 1].grid(True)

plt.tight_layout()
plt.savefig('algorithm_performance_optimized.png')