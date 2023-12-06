
from bitVector import *
import time
import random


def IV(lev):
    x = random.getrandbits(lev)
    x |= (1 << lev-1) | 1

    x = hex(x)
    x = x[2:]

    return x

def keyChecking(key, lev):
    l = len(key)
    sz = lev//4

    if l >= sz:
        key = key[:sz]
    else:
        pad = (sz-1)//2
        key += pad*'00'
    
    return key

def textListGenerator(text):
    texts = []
    for i in range(0, len(text), 32):
        texts.append(text[i:i+32])
    
    return texts

def addCBCPadding(text):
    l = len(text)
    if l%32:
        pad = (32-(l%32))//2
        hexPad = hex(pad)
        hexPad = hexPad[2:]
        text += pad*('0'+hexPad)
    else:
        text += 16*('00')

    return text

def removeCBCPadding(text):
    if text[-1] == '0':
        text = text[:-32]
    else:
        hexPad = text[-1]
        pad = int(hexPad, 16)
        text = text[:-(2*pad)]
    
    return text


def g(w, roundConstant):
    w = w[8:] + w[:8]
    bitWord = BitVector(bitstring=w)

    for i in range(4):
        bitWord[i*8:(i+1)*8] = BitVector(intVal=Sbox[bitWord[i*8:(i+1)*8].intValue()], size=8)
    bitWord[0:8] ^= roundConstant

    return bitWord

def constructMatrix(text):
    matrix = [[BitVector(hexstring='00') for _ in range(4)] for _ in range(4)]
    for i in range(0, 32, 2):
        x = (i//2)%4
        y = i//8
        matrix[x][y] = BitVector(hexstring=text[i:i+2])

    return matrix

def addRoundKey(matrix, key):
    keyMatrix = constructMatrix(key)
    mat = [[BitVector(hexstring='00') for _ in range(4)] for _ in range(4)]

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            mat[i][j] = matrix[i][j]^keyMatrix[i][j]

    return mat

def substituteBytes(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = BitVector(intVal=Sbox[matrix[i][j].intValue()], size=8)
    
    return matrix

def inverseSubstituteBytes(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = BitVector(intVal=InvSbox[matrix[i][j].intValue()], size=8)
    
    return matrix

def shiftRows(matrix):
    for i in range(len(matrix)):
        matrix[i] = matrix[i][i:] + matrix[i][:i]

    return matrix

def inverseShiftRows(matrix):
    for i in range(len(matrix)):
        matrix[i] = matrix[i][-i:] + matrix[i][:-i]

    return matrix

def mixColumns(matrix):
    mat = [[BitVector(hexstring='00') for _ in range(4)] for _ in range(4)]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            sum = BitVector(hexstring='00')
            for k in range(len(matrix)):
                x = Mixer[i][k].gf_multiply_modular(matrix[k][j], BitVector(intVal=0x11b, size=9), 8)
                sum ^= x
            mat[i][j] = sum
    
    return mat

def inverseMixColumns(matrix):
    mat = [[BitVector(hexstring='00') for _ in range(4)] for _ in range(4)]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            sum = BitVector(hexstring='00')
            for k in range(len(matrix[i])):
                x = InvMixer[i][k].gf_multiply_modular(matrix[k][j], BitVector(intVal=0x11b, size=9), 8)
                sum ^= x
            mat[i][j] = sum
    
    return mat


def decodeMatrix(matrix):
    cipherText = ""
    for i in range(4):
        for j in range(4):
            cipherText += matrix[j][i].get_bitvector_in_hex()

    return cipherText


def keyScheduling(key, lev):
    words = lev//32
    roundCount = words + 6
    total = (roundCount+1)*4
    
    keyWords = [None for i in range(total)]
    roundConstant = BitVector(intVal=0x01, size=8)

    for i in range(words):
        keyWords[i] = BitVector(hexstring=key[i*8:(i+1)*8])

    for i in range(words, total):
        temp = keyWords[i-1]
        if i % words == 0:
            temp = g(temp, roundConstant)
            keyWords[i] = keyWords[i-words] ^ temp
            roundConstant = roundConstant.gf_multiply_modular(BitVector(intVal=0x02, size=8), BitVector(intVal=0x11b, size=9), 8)
        else:
            keyWords[i] = keyWords[i-words] ^ keyWords[i-1]

    keys = []
    for i in range(roundCount+1):
        keys.append((keyWords[i*4] + keyWords[i*4+1] + keyWords[i*4+2] + keyWords[i*4+3]).get_bitvector_in_hex())

    return keys




def encrypt(plainTexts, keys, lev, IV):
    cipherText = ""
    roundCount = lev//32 + 6

    initialization = IV
    ini = BitVector(hexstring=initialization)

    for plainText in plainTexts:
        plain = BitVector(hexstring=plainText)
        plain ^= ini
        plain = plain.get_bitvector_in_hex()
        matrix = constructMatrix(plain)
        matrix = addRoundKey(matrix, keys[0])

        for i in range(roundCount):
            matrix = substituteBytes(matrix)
            matrix = shiftRows(matrix)
            if i != roundCount-1:
                matrix = mixColumns(matrix)
            matrix = addRoundKey(matrix, keys[i+1])

            
        initialization = decodeMatrix(matrix)
        ini = BitVector(hexstring=initialization)



        cipherText += initialization

    return cipherText


def decrypt(cipherText, keys, lev, IV):
    cipherTexts = [cipherText[i:i+32] for i in range(0, len(cipherText), 32)]

    plainText = ""
    initialization = IV
    ini = BitVector(hexstring=initialization)

    for text in cipherTexts:
        roundCount = lev//32 + 6
        matrix = constructMatrix(text)
        matrix = addRoundKey(matrix, keys[roundCount])

        for i in range(roundCount):
            matrix = inverseShiftRows(matrix)
            matrix = inverseSubstituteBytes(matrix)
            matrix = addRoundKey(matrix, keys[roundCount-i-1])
            if i != roundCount-1:
                matrix = inverseMixColumns(matrix)

        plain = decodeMatrix(matrix)
        plain = BitVector(hexstring=plain)
        plain ^= ini
        plainText += plain.get_bitvector_in_hex()
        initialization = text
        ini = BitVector(hexstring=initialization)

    return plainText




def encryptCTR(plainTexts, keys, lev, IV):
    cipherText = ""
    roundCount = lev//32 + 6

    initialization = IV
    ini = BitVector(hexstring=initialization)
    counter = 0

    for plainText in plainTexts:
        cnt = hex(counter)
        cnt = cnt[2:]
        cnt = (lev//4-len(cnt))*'0' + cnt
        cnt = BitVector(hexstring=cnt)
        nonce = ini^cnt
        nonce = nonce.get_bitvector_in_hex()
        matrix = constructMatrix(nonce)
        matrix = addRoundKey(matrix, keys[0])

        for i in range(roundCount):
            matrix = substituteBytes(matrix)
            matrix = shiftRows(matrix)
            if i != roundCount-1:
                matrix = mixColumns(matrix)
            matrix = addRoundKey(matrix, keys[i+1])

            
        cipher = decodeMatrix(matrix)
        cipher = BitVector(hexstring=cipher)
        text = BitVector(hexstring=plainText)
        text = cipher^text
        counter += 1
        cipherText += text.get_bitvector_in_hex()

    return cipherText


def decryptCTR(cipherText, keys, lev, IV):
    cipherTexts = [cipherText[i:i+32] for i in range(0, len(cipherText), 32)]

    plainText = ""
    initialization = IV
    ini = BitVector(hexstring=initialization)
    counter = 0

    for text in cipherTexts:
        roundCount = lev//32 + 6
        cnt = hex(counter)
        cnt = cnt[2:]
        cnt = (lev//4-len(cnt))*'0' + cnt
        cnt = BitVector(hexstring=cnt)
        nonce = ini^cnt
        nonce = nonce.get_bitvector_in_hex()
        matrix = constructMatrix(nonce)
        matrix = addRoundKey(matrix, keys[0])

        for i in range(roundCount):
            matrix = substituteBytes(matrix)
            matrix = shiftRows(matrix)
            if i != roundCount-1:
                matrix = mixColumns(matrix)
            matrix = addRoundKey(matrix, keys[i+1])

        cipher = decodeMatrix(matrix)
        cipher = BitVector(hexstring=cipher)
        plain = BitVector(hexstring=text)
        plain = cipher^plain

        counter += 1
        plainText += plain.get_bitvector_in_hex()

    return plainText








def aes():
    print('Key Length: ')
    lev = int(input())
    print('Key: ')
    key = input()
    print('Text: ')
    text = input()


    ini = IV(lev)

    hexText = text.encode("utf-8").hex()
    hexKey = key.encode("utf-8").hex()
    print("\nPlain Text:")
    print("In ASCII:", text)
    print("In HEX:", hexText)
    print("\nKey:")
    print("In ASCII:", key)
    print("In HEX:", hexKey)
    print()

    hexKey = keyChecking(hexKey, lev)
    keyStart = time.time()
    keys = keyScheduling(hexKey, lev)
    keyEnd = time.time()

    hexText = addCBCPadding(hexText)
    print(len(hexText))
    print(hexText)
    hexTexts = textListGenerator(hexText)

    encStart = time.time()
    cipherText = encrypt(hexTexts, keys, lev, ini)
    encEnd = time.time()

    print("Cipher Text:")
    print("In Hex:", cipherText)
    print("In ASCII:", bytearray.fromhex(cipherText).decode('Latin1'))
    print()

    decStart = time.time()
    hexText = decrypt(cipherText, keys, lev, ini)
    decEnd = time.time()

    hexText = removeCBCPadding(hexText)
    print("Deciphered Text:")
    print("In Hex:", hexText)
    print("In ASCII:", bytearray.fromhex(hexText).decode('Latin1'))
    print()


    print("Execution time details:")
    print("Key Scheduling :", ((keyEnd-keyStart)*1000), "ms")
    print("Encryption Time:", ((encEnd-encStart)*1000), "ms")
    print("Decryption Time:", ((decEnd-decStart)*1000), "ms")


def aesCTR():
    print('Key Length: ')
    lev = int(input())
    print('Key: ')
    key = input()
    print('Text: ')
    text = input()


    ini = IV(lev)

    hexText = text.encode("utf-8").hex()
    hexKey = key.encode("utf-8").hex()
    print("\nPlain Text:")
    print("In ASCII:", text)
    print("In HEX:", hexText)
    print("\nKey:")
    print("In ASCII:", key)
    print("In HEX:", hexKey)
    print()

    hexKey = keyChecking(hexKey, lev)
    keyStart = time.time()
    keys = keyScheduling(hexKey, lev)
    keyEnd = time.time()

    hexText = addCBCPadding(hexText)
    print(len(hexText))
    print(hexText)
    hexTexts = textListGenerator(hexText)

    encStart = time.time()
    cipherText = encryptCTR(hexTexts, keys, lev, ini)
    encEnd = time.time()

    print("Cipher Text:")
    print("In Hex:", cipherText)
    print("In ASCII:", bytearray.fromhex(cipherText).decode('Latin1'))
    print()

    decStart = time.time()
    hexText = decryptCTR(cipherText, keys, lev, ini)
    decEnd = time.time()

    hexText = removeCBCPadding(hexText)
    print("Deciphered Text:")
    print("In Hex:", hexText)
    print("In ASCII:", bytearray.fromhex(hexText).decode('Latin1'))
    print()


    print("Execution time details:")
    print("Key Scheduling :", ((keyEnd-keyStart)*1000), "ms")
    print("Encryption Time:", ((encEnd-encStart)*1000), "ms")
    print("Decryption Time:", ((decEnd-decStart)*1000), "ms")


def main():
    aesCTR()

if __name__ == "__main__":
    main()