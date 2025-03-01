import threading
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from bubble_sort import bubble_sort
from quick_sort import quick_sort 
from merge_sort import merge_sort
from heap_sort import heap_sort

import random
import queue

# Shared state
array_updates = queue.Queue()  # Queue to pass array updates to the main thread
sorting_complete = threading.Event()  # Event to signal when sorting is complete

# Time diff in milliseconds
def visualize_sorting(array, time_diff, sorting_func):
    function_title = sorting_func.__name__

    def visualize():
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.set_title(function_title.replace("_", " ").title())  
        bars = ax.bar(range(len(array)), array, color='#eb9191')
        ax.set_facecolor("#424c51")

        def update_fig(frame):
            try:
                # Get the latest array from the queue
                new_array = array_updates.get_nowait()
                for bar, height in zip(bars, new_array):
                    bar.set_height(height)
            except queue.Empty:
                pass  # No update available
            return bars

        ani = animation.FuncAnimation(fig, update_fig, interval=time_diff, blit=True, cache_frame_data=False)
        plt.show()

    def on_array_change(new_array):

        array_updates.put(new_array.copy())

    monitored_array = MonitoredArray(array.copy(), on_array_change, time_diff)

    sorting_thread = threading.Thread(target=sorting_func, args=(monitored_array,))
    sorting_thread.start()

    visualize()

    sorting_thread.join()
    sorting_complete.set() 

class MonitoredArray:
    def __init__(self, arr, callback, time_diff):
        self._arr = arr
        self._callback = callback
        self._time_diff = time_diff / 1000  # milliseconds to seconds

    def __getitem__(self, index):
        return self._arr[index]

    def __setitem__(self, index, value):
        self._arr[index] = value
        self._callback(self._arr) 
        time.sleep(self._time_diff) 

    def __len__(self):
        return len(self._arr)

    def __repr__(self):
        return repr(self._arr)

    def __iter__(self):
        return iter(self._arr)

    def copy(self):
        return self._arr.copy()

sorting_array = [random.randint(1, 200) for _ in range(20)]


visualize_sorting(sorting_array, 100, quick_sort)