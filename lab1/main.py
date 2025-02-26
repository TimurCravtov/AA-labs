import matplotlib.pyplot as plt
import time
from tabulate import tabulate

# first method, recursion
def fib_rec(n):
    return n if n <= 1 else fib_rec(n-1) + fib_rec(n-2)


def plot(datapoints, data, title):


    plt.title(title, weight = "bold")
    plt.xticks(datapoints)
    plt.xlabel("$f_n$")
    plt.ylabel("T(s)")
    plt.grid()

    # some cute colours
    ax = plt.gca()
    ax.set_facecolor("#424c51")
    
    plt.plot(datapoints, data, marker="o", color="#eb9191")
    plt.show()


# second method, using matrix multimplication
def fib_matrix(n):
    F = [[1, 1],
         [1, 0]]
    if n == 0:
        return 0
    power(F, n - 1)
    return F[0][0]

def power(F, n):
    M = [[1, 1],
         [1, 0]]
    
    for _ in range(2, n + 1):
        multiply(F, M)

def multiply(F, M):
    x = F[0][0] * M[0][0] + F[0][1] * M[1][0]
    y = F[0][0] * M[0][1] + F[0][1] * M[1][1]
    z = F[1][0] * M[0][0] + F[1][1] * M[1][0]
    w = F[1][0] * M[0][1] + F[1][1] * M[1][1]
    
    F[0][0], F[0][1], F[1][0], F[1][1] = x, y, z, w




import math

from math import sqrt

PHI =  (1 + sqrt(5)) / 2


f = [ 0, 1, 1, 2, 3, 5 ]

# third method, using phi approximation
def fib_phi(n):
 
    if n < 6:
        return f[n]
 
    t = 5
    fn = 5
     
    while t < n:
        fn = round(fn * PHI)
        t+=1
     
    return fn

# second method, using iteration
def fib_it(n):
    a, b = 0, 1
    for i in range(0, n):
        a, b = b, a + b
    return a



def fibs_upto(n):
    fibs = [0, 1, 1]
    for f in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

from math import sqrt

# sixth methood, using binet formula
def fib_binet(n):
    phi = (1 + sqrt(5)) / 2
    psi = (1 - sqrt(5)) / 2
    return round((phi**n - psi**n) / sqrt(5))


# seventh methood, using fast doubling formula
def fib_fast_doubling(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    def fib_doubling(k):
        if k == 0:
            return (0, 1)
        
        Fk, Fk1 = fib_doubling(k // 2)

        F2k = Fk * (2 * Fk1 - Fk)
        F2k1 = Fk1**2 + Fk**2 
        
        return (F2k1, F2k + F2k1) if k % 2 else (F2k, F2k1)

    return fib_doubling(n)[0]


def calculate_func_exec_time(func, datapoints):

    times = []

    for dpt in datapoints:
        start = time.time()
        _ = func(dpt) # no need to use the value at this point
        times.append(time.time() - start)
    return times, datapoints



def print_custom_table(datapoints, times, float_format=".6f"):

    formatted_times = [f"{t:{float_format}}" for t in times]
    
    datapoints_str = [str(dp) for dp in datapoints]
    
    column_widths = [max(len(str(item)) for item in col) for col in zip(["Datapoint"] + datapoints_str, ["Execution Time"] + formatted_times)]

    separator = "+".join("-" * (w + 2) for w in column_widths)

    def format_row(row):
        return "| " + " | ".join(f"{str(val):<{w}}" for val, w in zip(row, column_widths)) + " |"

    print(separator)
    print(format_row(["Fn"] + datapoints_str))
    print(separator)
    print(format_row(["Time"] + formatted_times))
    print(separator)

nprange = lambda minim, maxim, division: range(minim, maxim, (maxim-minim) // division)
n = nprange(5, 30, 20)


def plot_fib_diff(datapoints):

    actual_fibs = fibs_upto(datapoints[-1] + 1)  # Include the last value in datapoints
    binet_fibs = [fib_phi(n) for n in datapoints]
    
    # Calculate the differences
    differences = [abs(actual_fibs[i] - binet_fibs[i]) for i in range(len(datapoints))]
    
    # Plotting
    plt.plot(datapoints, differences, color="#eb9191")
    plt.title("Difference Between Actual Fibonacci and Phi Approximation", weight="bold")
    plt.xlabel("Fibonacci Index")
    plt.ylabel("Difference")
    plt.grid()
    plt.show()


times, datapoints = calculate_func_exec_time(fib_binet, n)
print_custom_table(datapoints, times)



plot_fib_diff(range(0, 82))


