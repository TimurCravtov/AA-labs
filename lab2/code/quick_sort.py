def partition(arr, low, high):
    
    pivot = arr[high]

    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            swap(arr, i, j)
    
    swap(arr, i + 1, high)
    return i + 1

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


def quick_sort(arr):
    _quick_sort(arr, 0, len(arr) - 1)

def _quick_sort(arr, low, high ):
    if low < high:
        
        # pi is the partition return index of pivot
        pi = partition(arr, low, high)
        
        _quick_sort(arr, low, pi - 1)
        _quick_sort(arr, pi + 1, high)