import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from algorithm.kruskal import min_span_tree_kruskal
from algorithm.prim import min_span_tree_prim

def generate_connected_weighted_graph(num_nodes: int, num_edges: int, weight_range=(1, 10)) -> nx.Graph:
    """Generate a connected weighted graph with specified parameters."""
    if num_edges < num_nodes - 1:
        raise ValueError("Number of edges must be at least (num_nodes - 1) for connectivity.")
    if num_edges > num_nodes * (num_nodes - 1) // 2:
        raise ValueError("Too many edges for the number of nodes.")
    
    # Start with a minimum spanning tree to ensure connectivity
    # First create a complete graph
    G = nx.complete_graph(num_nodes)
    
    # Create a random spanning tree using a random edge generator
    edge_weights = {(u, v): random.random() for u, v in G.edges()}
    nx.set_edge_attributes(G, edge_weights, 'weight')
    T = nx.minimum_spanning_tree(G)
    
    # The tree is our starting point
    G = T.copy()
    
    # Add remaining random edges until reaching the desired number
    remaining_edges = num_edges - (num_nodes - 1)  # Tree already has n-1 edges
    
    # Find potential edges to add (those not in our tree)
    all_possible_edges = list(nx.non_edges(G))
    
    if remaining_edges > 0 and all_possible_edges:
        selected_edges = random.sample(all_possible_edges, min(remaining_edges, len(all_possible_edges)))
        G.add_edges_from(selected_edges)
    
    # Relabel nodes and assign weights
    mapping = {i: f'v{i+1}' for i in range(num_nodes)}
    G = nx.relabel_nodes(G, mapping)
    
    # Assign weights to all edges
    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(*weight_range)
    
    return G

def run_benchmark(algorithm, graph):
    """Measure execution time of algorithm on given graph."""
    start_time = time.perf_counter()
    algorithm(graph)
    return time.perf_counter() - start_time

def benchmark_scenario(scenario_params):
    """Run a benchmark scenario and return the results."""
    num_nodes, num_edges, repetitions = scenario_params
    
    kruskal_times = []
    prim_times = []
    
    for _ in range(repetitions):
        G = generate_connected_weighted_graph(num_nodes, num_edges)
        kruskal_times.append(run_benchmark(min_span_tree_kruskal, G))
        prim_times.append(run_benchmark(min_span_tree_prim, G))
    
    return (np.mean(kruskal_times), np.mean(prim_times))

def main():
    # Set seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Benchmark parameters
    repetitions = 3
    max_workers = 4  # Adjust based on available CPU cores
    
    # Define scenarios
    # 1. Increasing vertices with fixed edge density
    nodes_range = np.arange(10, 500, 20)
    edge_density = 1.5
    scenario1_params = [(n, int(n * edge_density), repetitions) for n in nodes_range]
    
    # 2. Increasing edges with fixed vertices
    fixed_nodes = 500
    max_edges = fixed_nodes * (fixed_nodes - 1) // 2
    edge_steps = max(1, max_edges // 5)
    edge_range = np.arange(fixed_nodes - 1, max_edges, edge_steps)
    scenario2_params = [(fixed_nodes, e, repetitions) for e in edge_range]
    
    # 3. Dense graphs
    scenario3_params = [(n, n * 2, repetitions) for n in nodes_range]
    
    # 4. Sparse graphs
    scenario4_params = [(n, n, repetitions) for n in nodes_range]
    
    # Run benchmarks in parallel
    results = {}
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Run each scenario
        for scenario_num, params in enumerate([scenario1_params, scenario2_params, 
                                               scenario3_params, scenario4_params], 1):
            futures = [executor.submit(benchmark_scenario, p) for p in params]
            scenario_results = [future.result() for future in as_completed(futures)]
            
            # Sort results based on original parameter order
            if scenario_num == 1:
                x_values = nodes_range
            elif scenario_num == 2:
                x_values = edge_range
            else:
                x_values = nodes_range
                
            # Pair results with their x-values for sorting
            paired_results = list(zip(x_values, scenario_results))
            paired_results.sort(key=lambda x: x[0])
            
            # Extract sorted results
            sorted_results = [res for _, res in paired_results]
            kruskal_times = [res[0] for res in sorted_results]
            prim_times = [res[1] for res in sorted_results]
            
            results[f"scenario{scenario_num}"] = {
                "x_values": x_values,
                "kruskal_times": kruskal_times,
                "prim_times": prim_times
            }
    
    # Plotting
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    # Scenario 1: Edge Density
    axs[0, 0].plot(results["scenario1"]["x_values"], results["scenario1"]["kruskal_times"], 
                   label="Kruskal", marker='o')
    axs[0, 0].plot(results["scenario1"]["x_values"], results["scenario1"]["prim_times"], 
                   label="Prim", marker='s')
    axs[0, 0].set_title("Edge Density (edges = nodes * 1.5)")
    axs[0, 0].set_xlabel("Vertices")
    axs[0, 0].set_ylabel("Time (s)")
    axs[0, 0].legend()
    axs[0, 0].grid(True)
    
    # Scenario 2: Fixed Vertices
    axs[0, 1].plot(results["scenario2"]["x_values"], results["scenario2"]["kruskal_times"], 
                   label="Kruskal", marker='o')
    axs[0, 1].plot(results["scenario2"]["x_values"], results["scenario2"]["prim_times"], 
                   label="Prim", marker='s')
    axs[0, 1].set_title(f"Fixed Vertices (n = {fixed_nodes})")
    axs[0, 1].set_xlabel("Edges")
    axs[0, 1].set_ylabel("Time (s)")
    axs[0, 1].legend()
    axs[0, 1].grid(True)
    
    # Scenario 3: Dense Graphs
    axs[1, 0].plot(results["scenario3"]["x_values"], results["scenario3"]["kruskal_times"], 
                   label="Kruskal", marker='o')
    axs[1, 0].plot(results["scenario3"]["x_values"], results["scenario3"]["prim_times"], 
                   label="Prim", marker='s')
    axs[1, 0].set_title("Dense Graphs (edges = nodes * 2)")
    axs[1, 0].set_xlabel("Vertices")
    axs[1, 0].set_ylabel("Time (s)")
    axs[1, 0].legend()
    axs[1, 0].grid(True)
    
    # Scenario 4: Sparse Graphs
    axs[1, 1].plot(results["scenario4"]["x_values"], results["scenario4"]["kruskal_times"], 
                   label="Kruskal", marker='o')
    axs[1, 1].plot(results["scenario4"]["x_values"], results["scenario4"]["prim_times"], 
                   label="Prim", marker='s')
    axs[1, 1].set_title("Sparse Graphs (edges = nodes)")
    axs[1, 1].set_xlabel("Vertices")
    axs[1, 1].set_ylabel("Time (s)")
    axs[1, 1].legend()
    axs[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig('algorithm_performance_optimized.png', dpi=300)

if __name__ == "__main__":
    main()