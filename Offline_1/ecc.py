import random
from sympy import isprime, mod_inverse
import time

def pointAddition(P, Q, a, p):
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P

    if P != Q:
        if Q[0] >= P[0]:
            s = ((Q[1] - P[1]) * mod_inverse(Q[0] - P[0], p) + p) % p
        else:
            s = ((P[1] - Q[1]) * mod_inverse(P[0] - Q[0], p) + p) % p
    else:
        if P[1] == 0:
            return (0, 0)
        else:
            s = ((3 * P[0]**2 + a) * mod_inverse(2 * P[1], p) + p) % p

    x = (s**2 - P[0] - Q[0]) % p
    y = (s * (P[0] - x) - P[1]) % p

    return x, y

def scalarMultiply(k, G, a, p):
    R = G
    for i in range(k.bit_length(), 0, -1):
        if (k >> (i-1)) & 1:
            R = pointAddition(R, R, a, p)
        R = pointAddition(R, G, a, p)
    return R

def generatePrime(lev):
    while True:
        x = random.getrandbits(lev)
        x |= (1 << lev-1) | 1

        if isprime(x):
            return x
        
def generateCurve(p):
    a = 109
    while True:
        b = random.randint(2, 100000)
        if isprime(b) == False:
            continue
        x = 4*a**3+27*b**2
        if x%p != 0:
            return a, b

def isSquare(yy, p):
    return pow(yy, (p - 1) // 2, p) == 1

def generatePoint(a, b, p):
    while True:
        x = random.randint(2, p-1)
        yy = (x**3 + a*x + b) % p

        if isSquare(yy, p):
            y = pow(yy, (p + 1) // 4, p)
            return x, y


def getInitial(lev):
    p = generatePrime(lev)
    a, b = generateCurve(p)
    x, y = generatePoint(a, b, p)
    G = (x, y)

    return G, a, p










def ecc(lev):
    G, a, p = getInitial(lev)
    
    ka = random.randint(p/2, p-1)
    kb = random.randint(p/2, p-1)

    startTime = time.time()
    A = scalarMultiply(ka, G, a, p) 
    ta = (time.time() - startTime)
    startTime = time.time()
    B = scalarMultiply(kb, G, a, p)
    tb = time.time() - startTime
    startTime = time.time()
    key = scalarMultiply(ka * kb, G, a, p)
    tc = time.time() - startTime
    return ta, tb, tc


def measureTime(lev, trials):
    timeA = []
    timeB = []
    timeKey = []

    for _ in range(trials):
        
        ta, tb, tc = ecc(lev)
        timeA.append(ta)
        timeB.append(tb)
        timeKey.append(tc)

    avgA = sum(timeA) / trials
    avgB = sum(timeB) / trials
    avgKey = sum(timeKey) / trials

    return avgA, avgB, avgKey


def main():
    levs = [128, 192, 256]  
    trials = 5  

    print(f"{'k':<5}{'A':<15}{'B':<15}{'Shared key R':<15}")
    for lev in levs:   
        avgA, avgB, avgKey = measureTime(lev, trials)
        print(f"{lev:<5}{avgA*1000:<15.10f}{avgB*1000:<15.10f}{avgKey*1000:<15.10f}")

if __name__ == "__main__":
    main()




