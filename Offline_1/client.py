
import socket
from aes import *
from ecc import *
import random
import ast
import math
import pickle
		 

host = "localhost"
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    # data = s.recv(1024)
    # recData = pickle.loads(data)

    # lev = recData[0]
    # key = recData[1]
    # ini = recData[2]

    # hexKey = key.encode("utf-8").hex()

    # print(ini)


    # cipherText = s.recv(1024).decode()

    # print("Receieved Cipher Text:")
    # print("In Hex:", cipherText)
    # print("In ASCII:", bytearray.fromhex(cipherText).decode('Latin1'))
    # print()

    # lev = int(lev)
    # hexKey = keyChecking(hexKey, lev)
    # keys = keyScheduling(hexKey, lev)

    # hexText = decrypt(cipherText, keys, lev, ini)

    # hexText = removeCBCPadding(hexText)
    # print("Deciphered Text:")
    # print("In Hex:", hexText)
    # print("In ASCII:", bytearray.fromhex(hexText).decode('Latin1'))
    # print()


    # s.sendall('Text received in AES CBC Mode'.encode())



    ## FILE

    # data = s.recv(1024)
    # recData = pickle.loads(data)

    # lev = int(recData[0])
    # totalChunks = recData[1]
    # key = recData[2]
    # fileName = recData[3]

    # hexKey = key.encode("utf-8").hex()
    # hexKey = keyChecking(hexKey, lev)
    # keys = keyScheduling(hexKey, lev)

    # filePath = 'client/' + fileName

    # print(totalChunks)
    # fileData = bytearray()
    # cnt = 0
    # while cnt != totalChunks:
    #     receivedData = s.recv(1024)
    #     data = pickle.loads(receivedData)

    #     ini = data[0]
    #     text = data[1]
        
    #     print("Receieved Cipher Hex:")
    #     print("In Hex:", text)
    #     print()

    #     hexText = decrypt(text, keys, lev, ini)
    #     hexText = removeCBCPadding(hexText)
    #     print("Deciphered Hex:")
    #     print("In Hex:", hexText)
    #     print()

    #     data = bytearray.fromhex(hexText)
    #     fileData.extend(data)
    #     cnt += 1

    #     ack = 'Receieved chunk: ' + str(cnt)
    #     ack = pickle.dumps(ack)
    #     s.sendall(ack)


    # with open(filePath, 'wb') as file:
    #     file.write(fileData)



    #ECC

    data = s.recv(20000).decode().split(' ')

    lev = data[0]
    lev = int(lev)
    Ga = int(data[1])
    Gb = int(data[2])
    G = (Ga, Gb)
    a = int(data[3])
    p = int(data[4])
    Aa = int(data[5])
    Ab = int(data[6])
    A = (Aa, Ab)

    bb = random.randint(p/2, p-1)
    B = scalarMultiply(bb, G, a, p)
    
    s.sendall((str(B[0])+' '+str(B[1])).encode())

    key = scalarMultiply(bb, A, a, p)

    hexKey = hex(key[0])
    ini = hex(key[1])

    hexKey = hexKey[2:]
    ini = ini[2:]


    hexKey = keyChecking(hexKey, lev)
    ini = keyChecking(ini, lev)

    ini = ini[:32]


    cipherText = s.recv(1024).decode()

    print("Receieved Cipher Text:")
    print("In Hex:", cipherText)
    print("In ASCII:", bytearray.fromhex(cipherText).decode('Latin1'))
    print()

    
    keys = keyScheduling(hexKey, lev)

    hexText = decrypt(cipherText, keys, lev, ini)

    hexText = removeCBCPadding(hexText)
    print("Deciphered Text:")
    print("In Hex:", hexText)
    print("In ASCII:", bytearray.fromhex(hexText).decode('Latin1'))
    print()


    s.sendall('Text received'.encode())



    s.close()

print("Connection closed")


