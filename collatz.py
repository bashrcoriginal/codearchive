import math
def next(mem, n):
    if n in mem:
        return mem[n]
    if n <= 1:
        return n
    if n % 2 == 0:
        mem[n] = next(mem, n//2) + 1
    else:
        mem[n] = next(mem, 3*n + 1) + 1
    return mem[n]

def collatz(m, n):
    mem = {}
    mx = 0
    for i in range(n, m-1, -1):
        mx = max(next(mem, i), mx)    
    return mx

print(collatz(0, 10000000))
