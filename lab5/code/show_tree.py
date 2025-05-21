import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from algorithm.kruskal import min_span_tree_kruskal
from algorithm.prim import min_span_tree_prim
from main import generate_connected_weighted_graph 

def show_random_graph(graph: nx.Graph, filename="random_graph.png"):
    """Display and save the initial randomly generated weighted graph."""
    pos = nx.spring_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.title("Initial Random Graph")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

def show_span_trees(graph: nx.Graph, filename="span_trees.png"):
    """Display and save MSTs using Kruskal and Prim algorithms side by side."""
    kruskal_tree = min_span_tree_kruskal(graph)
    prim_tree = min_span_tree_prim(graph)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    pos = nx.spring_layout(graph)

    for ax, tree, title in zip(axes, [kruskal_tree, prim_tree], ['Kruskal MST', 'Prim MST']):
        edge_labels = nx.get_edge_attributes(tree, 'weight')
        nx.draw(tree, pos, with_labels=True, node_color='lightgreen', edge_color='black', ax=ax)
        nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels, ax=ax)
        ax.set_title(title)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

if __name__ == "__main__":
    G = generate_connected_weighted_graph(10, 15)
    show_random_graph(G, "random_graph.png")
    show_span_trees(G, "span_trees.png")
