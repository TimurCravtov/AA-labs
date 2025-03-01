import matplotlib.pyplot as plt
import time
import random
import numpy as np
import os

# Get the directory where the script is executed
execution_dir = os.getcwd()

# Ensure the 'images/lab' directory exists inside the execution directory for the images
output_dir = os.path.join(execution_dir, "images", "lab")
os.makedirs(output_dir, exist_ok=True)

def sort_performance_analyzer(sort_func, sample_sizes=[10, 100, 300, 700]):
    array_types = ["random", "sorted", "partially_sorted"]
    colors = ["#eb9191", "#91ebcf", "#919eeb"]
    
    def random_array(n):
        return [random.randint(1, 1_000_000) for _ in range(n)]
    
    def swap_every_nth(arr, step=5):
        arr = arr[:]
        for i in range(0, len(arr) - step, step):
            arr[i], arr[i + step - 1] = arr[i + step - 1], arr[i]
        return arr
    
    results = {
        "times": {array_type: [] for array_type in array_types},
        "sample_sizes": sample_sizes
    }
    
    for size in sample_sizes:
        arrays = {
            "random": random_array(size),
            "sorted": sorted(random_array(size)),
            "partially_sorted": swap_every_nth(sorted(random_array(size)), max(5, size // 20))
        }
        
        for array_type in array_types:
            start = time.time()
            sort_func(arrays[array_type].copy())
            execution_time = time.time() - start
            results["times"][array_type].append(execution_time)
    
    # Save plot to the 'images/lab' directory
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x_positions = sample_sizes
    rects = []
    bar_width = min(np.diff(x_positions)) * 0.25 if len(x_positions) > 1 else x_positions[0] * 0.25
    
    for i, array_type in enumerate(array_types):
        offset = (i - (len(array_types) - 1) / 2) * bar_width
        positions = [x + offset for x in x_positions]
        
        rect = ax.bar(
            positions,
            results["times"][array_type],
            bar_width,
            label=f'{array_type.replace("_", " ").title()} Array',
            color=colors[i]
        )
        rects.append(rect)
    
    title = f"{sort_func.__name__.replace('_', ' ').title()} Performance by Array Type and Size"
    ax.set_xlabel('Array Size', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title(title, fontweight='bold')
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f"{size:,}" for size in sample_sizes])

    if max(sample_sizes) / min(sample_sizes) > 50:
        ax.set_xscale('log')
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_facecolor("#424c51")
    fig.patch.set_facecolor('white')

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f'{height:.4f}',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom',
                color='white', fontsize=8
            )
    
    for rect in rects:
        autolabel(rect)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{sort_func.__name__}.png"))
    plt.show()

    # Generate file name based on function name (first letters of each word, ignoring underscores)
    short_name = "".join(word[0] for word in sort_func.__name__.split("_"))
    results_file = os.path.join(execution_dir, f"{short_name}.txt")

    # Write results to the same directory where the script was executed
    with open(results_file, "w") as f:
        algorithm_name = sort_func.__name__.replace('_', ' ').title()
        f.write(f"{algorithm_name} Execution Times (seconds):\n\n")

        headers = ["Array Size"] + [array_type.replace("_", " ").title() for array_type in array_types]
        row_format = "{:<15}" + "{:<15}" * len(array_types)

        f.write(row_format.format(*headers) + "\n")
        f.write("-" * (15 * (len(array_types) + 1)) + "\n")

        for i, size in enumerate(sample_sizes):
            row = [size] + [results["times"][array_type][i] for array_type in array_types]
            f.write(row_format.format(
                size,
                *[f"{time:.6f}" for time in row[1:]]
            ) + "\n")

    return results

from bubble_sort import bubble_sort
from heap_sort import heap_sort
from quick_sort import quick_sort
from merge_sort import merge_sort
from bubble_sort_impr import bubble_sort_impr

# sort_performance_analyzer(bubble_sort_impr, sample_sizes=[300, 600, 700, 3000, 5000])

# sort_performance_analyzer(merge_sort, sample_sizes=[1000, 10_000, 20_000, 50_000, 200_000])

sort_performance_analyzer(heap_sort, sample_sizes=[1000, 10_000, 20_000, 50_000, 200_000])





