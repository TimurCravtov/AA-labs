# first method, recursion
def fib_rec(n):
    return n if n <= 1 else fib_rec(n-1) + fib_rec(n-2)