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