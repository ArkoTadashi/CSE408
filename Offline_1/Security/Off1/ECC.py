import time
import random
from sympy import isprime, mod_inverse

# Function to check if a number is a quadratic residue modulo P
def is_quadratic_residue(x, P):
    k = pow(x, (P - 1) // 2, P)
    if k == 1:
        return True
    else:
        return False

# Function to find a random prime number for the field
def generate_prime(bits):
    while True:
        t = random.getrandbits(bits)
        if isprime(t):
            return t

# Function to find a suitable point on the elliptic curve
def find_point(a, b, P):
    while True:
        x = random.randint(0, P - 1)
        y_squared = (x**3 + a*x + b) % P
        if is_quadratic_residue(y_squared, P):
            y = pow(y_squared, (P + 1) // 4, P)
            return (x, y)

# Function to perform scalar multiplication on the elliptic curve
def scalar_multiply(k, G, a, P):
    #print(type(k),"\n")
    #print(k)
    R = G
    for i in range(k.bit_length(), 0, -1):
        if (k >> (i-1)) & 1:
            R = add_points(R, R, a, P)
        R = add_points(R, G, a, P)
       # print(R,"\n")
    return R

# Function to add two points on the elliptic curve
def add_points(P1, P2, a, P):
    if P1 is None:
        return P2
    if P2 is None:
        return P1

    x1, y1 = P1
    x2, y2 = P2
    if P1 != P2 and y1 == y2 :
       return (0,0)
    if P1[1] == 0 and P1 == P2:
            return (0, 0)
    if P1 != P2:
        m = ((y2 - y1) * mod_inverse(x2 - x1, P)) % P
    else:
        m = ((3 * x1**2 + a) * mod_inverse(2 * y1, P)) % P

    x3 = (m**2 - x1 - x2) % P
    y3 = (m * (x1 - x3) - y1) % P

    return (x3, y3)

# Function to perform Elliptic Curve Diffie-Hellman
def perform_ecdh( key_length):
    P = generate_prime(key_length)
    a = random.randint(2,P-1)
    k = (4* a**3) % P 
    b = random.randint(2,P-1) 
    while (k + 27*b*b) % P == 0 :
        b = random.randint(2,P-1)
    G = find_point(a, b, P)
    
    Ka = random.randint(2, P-1)
    Kb = random.randint(2, P-1)

    start_time = time.time()
    A = scalar_multiply(Ka, G, a, P) 
    ta = (time.time() - start_time)
    start_time = time.time()
    B = scalar_multiply(Kb, G, a, P)
    tb = time.time() - start_time
    start_time = time.time()
    shared_key = scalar_multiply(Ka * Kb, G, a, P)
    tc = time.time() - start_time
    return ta,tb,tc,A, B, shared_key

def getGaP(key_length):
    P = generate_prime(key_length)
    a = random.randint(2,P-1)
    k = (4* a**3) % P 
    b = random.randint(2,P-1) 
    while (k + 27*b*b) % P == 0 :
        b = random.randint(2,P-1)
    G = find_point(a, b, P)
    return G,a,b,P


def measure_time( key_length, trials):
    times_A = []
    times_B = []
    times_shared_key = []

    for _ in range(trials):
        
        ta,tb,tc, A, B, shared_key = perform_ecdh( key_length)
        times_A.append(ta)
        times_B.append(tb)
        times_shared_key.append(tc)

    avg_time_A = sum(times_A) / trials
    avg_time_B = sum(times_B) / trials
    avg_time_shared_key = sum(times_shared_key) / trials

    return avg_time_A, avg_time_B, avg_time_shared_key


def main():
    key_lengths = [128, 192, 256]  
    trials = 5  

    print(f"{'k':<5}{'A':<15}{'B':<15}{'Shared key R':<15}")
    for key_length in key_lengths:   
        avg_time_A, avg_time_B, avg_time_shared_key = measure_time(key_length, trials)
        print(f"{key_length:<5}{avg_time_A:<15.10f}{avg_time_B:<15.10f}{avg_time_shared_key:<15.10f}")

if __name__ == "__main__":
    main()
