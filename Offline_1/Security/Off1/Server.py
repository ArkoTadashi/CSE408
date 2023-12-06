import socket
import random
import math
import ast
from AESS import * 
from ECC import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
print ("Socket successfully created")
port = 12345	
s.bind(('', port))		
print ("socket binded to %s" %(port))

s.listen()	
print ("socket is listening")		

while True:

    c, addr = s.accept()	
    print ('Got connection from', addr )
    
    print("\nEnter Key Level :")
    #k = input()
    k = 128
    G,a,b,P = getGaP(k)
    Ka = random.randint(2, P-1)
    A = scalar_multiply(Ka, G, a, P) 
    temp = str(k)+'  '+str(G)+'  '+str(a)+'  '+str(b)+'  '+str(P)+'  '+str(A) 
    c.sendall((temp).encode())

    B = c.recv(1024).decode()
    #print(B)
    B = ast.literal_eval(B)
    key = scalar_multiply(Ka,B, a, P)
    key = str(key[0])
    print(key,"keyyyyy\n")

    print("Enter temp text:")
    #temp_text = input()
    temp_text='Amar matha kharap h0ye geI0 esh0b ki AESVVVgyugyibhy0'
    #temp_text="Never gonna give you up"
    hText = process_text(temp_text,k/4)
    hKey = process_key(key,k//4)
    
    firstPrint(key,hKey,temp_text,hText)
    h = padd(temp_text)
    htxtArr = txtArrCreate(h)
    tt ,key_list = getKeyList(hKey, k)
    ct, eTime = PrintEncrypt(htxtArr, key_list, k)
    c.sendall(ct.encode())
    print("Execution time details:")
    print("Key Scheduling :", (tt*1000), "ms")
    print("Encryption Time:", (eTime*1000), "ms")
    print(c.recv(1024).decode())
    
    s.close()

print("Connection closed")
