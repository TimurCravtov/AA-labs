# using phi approximation
def fib_phi(n):
 
    if n < 6:
        return f[n]
 
    t = 5
    fn = 5
    
    while t < n:
        fn = round(fn * PHI)
        t+=1
    
    return fn