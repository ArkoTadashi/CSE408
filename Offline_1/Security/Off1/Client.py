import socket
import random
import math
import ast
from AESS import * 
from ECC import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		

port = 12345			

s.connect(('127.0.0.1', port))

while True :
    msg = s.recv(1024).decode().split('  ')
    #print(msg)
    k = int(msg[0])
    G = ast.literal_eval(msg[1])
    a = int(msg[2])
    b = int(msg[3])
    P = int(msg[4])
    A = ast.literal_eval(msg[5])
    #gg = str(msg[4]) 
    #tuple_values = gg[1:-1].split(', ')
    #Ka = (int(tuple_values[0]),int(tuple_values[0]))
    #fffffffffffffffffffffffffffffff
    #print(A)
    Kb = random.randint(2, P-1)
    B = scalar_multiply(Kb, G, a, P)    
    s.sendall((str(B)).encode())
    key = scalar_multiply(Kb, A, a, P)
    key = str(key[0])
    print(key, 'KEyyyyyyy')
    ct = s.recv(1024).decode()
    print(ct)
    hKey = process_key(key,k//4)
    tt ,key_list = getKeyList(hKey, k)
    dt, eTime = PrintDecrypt(ct, key_list, k)
    #c.sendall(dt.encode())

    print("Execution time details:")
    print("Key Scheduling :", (tt*1000), "ms")
    print("Decryption Time:", (eTime*1000), "ms")

    s.close()
print("\nConnection endddd")