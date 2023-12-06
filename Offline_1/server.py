
import socket
from aes import * 
import math
from ecc import *
import random
import pickle

host = "localhost"
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(5)

    c, addr = s.accept()
    print('Got connection from', addr)


    # print('\n')
    # print('AES Level')
    # lev = input()
    # print('Input key for AES Transmission')
    # key = input()


    # ini = IV(int(lev))
    # print(ini)

    # sendingData = pickle.dumps((lev, key, ini))
    # c.sendall(sendingData)


    # print('Text to send')
    # text = input()

    # hexText = text.encode("utf-8").hex()
    # hexKey = key.encode("utf-8").hex()
    # print("\nPlain Text:")
    # print("In ASCII:", text)
    # print("In HEX:", hexText)
    # print("\nKey:")
    # print("In ASCII:", key)
    # print("In HEX:", hexKey)
    # print()

    # lev = int(lev)
    # hexKey = keyChecking(hexKey, lev)
    # keys = keyScheduling(hexKey, lev)

    # hexText = addCBCPadding(hexText)
    # hexTexts = textListGenerator(hexText)

    # cipherText = encrypt(hexTexts, keys, lev, ini)

    # print("Cipher Text:")
    # print("In Hex:", cipherText)
    # print("In ASCII:", bytearray.fromhex(cipherText).decode('Latin1'))
    # print()

    # c.sendall(cipherText.encode())



    # print(c.recv(1024).decode())


    ## FILE

    print('\n')
    print('AES Level')
    lev = int(input())
    print('Input key for AES Transmission')
    key = input()


    hexKey = key.encode("utf-8").hex()
    hexKey = keyChecking(hexKey, lev)
    keys = keyScheduling(hexKey, lev)



    print("Input File name with extension: ")
    fileName = input()
    
    print("Input File Location: ")
    filePath = input()
    with open(filePath, 'rb') as file:
        fileData = bytearray(file.read())

    chunk = 128
    print(fileData)
    totalChunks = int(math.ceil(len(fileData)/chunk))
    print(totalChunks)

    sendingData = pickle.dumps((lev, totalChunks, key, fileName))
    c.sendall(sendingData)


    for i in range(0, len(fileData), chunk):
        ini = IV(int(lev))

        data = fileData[i:i+chunk]
        hexData = ''.join(['{:02x}'.format(byte) for byte in data])
        print('File HexData: ')
        print(hexData)

        hexText = addCBCPadding(hexData)
        hexTexts = textListGenerator(hexText)

        cipherText = encrypt(hexTexts, keys, lev, ini)

        print("Cipher HexData:")
        print("In Hex:", cipherText)
        print()


        sendingData = pickle.dumps((ini, cipherText))
        c.sendall(sendingData)





    ### ECC


    # print('\n')
    # print('Key Level')
    # lev = int(input())

    
    # G, a, p = getInitial(lev)

    # aa = random.randint(p/2, p-1)
    # A = scalarMultiply(aa, G, a, p)

    # c.sendall((str(lev)+' '+str(G[0])+' '+str(G[1])+' '+str(a)+' '+str(p)+' '+str(A[0])+' '+str(A[1])).encode())

    # B = c.recv(1024).decode().split(' ')
    # Ba = int(B[0])
    # Bb = int(B[1])
    # B = (Ba, Bb)


    # key = scalarMultiply(aa, B, a, p)

    # hexKey = hex(key[0])
    # ini = hex(key[1])

    # hexKey = hexKey[2:]
    # ini = ini[2:]

    # hexKey = keyChecking(hexKey, lev)
    # ini = keyChecking(ini, lev)


    # print('Text to send')
    # text = input()

    # hexText = text.encode("utf-8").hex()
    # print("\nPlain Text:")
    # print("In ASCII:", text)
    # print("In HEX:", hexText)
    # print("\nKey:")
    # print("In ASCII:", key)
    # print("In HEX:", hexKey)
    # print()

    # keyStart = time.time()
    # keys = keyScheduling(hexKey, lev)
    # keyEnd = time.time()

    # hexText = addCBCPadding(hexText)
    # hexTexts = textListGenerator(hexText)

    # encStart = time.time()
    # cipherText = encrypt(hexTexts, keys, lev, ini)
    # encEnd = time.time()

    # print("Cipher Text:")
    # print("In Hex:", cipherText)
    # print("In ASCII:", bytearray.fromhex(cipherText).decode('Latin1'))
    # print()

    # c.sendall(cipherText.encode())


    # print(c.recv(1024).decode())

        
    s.close()

print("Connection closed")



