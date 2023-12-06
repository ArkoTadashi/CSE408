
from importlib import import_module
import time
import random
from BitVector import *


Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]



def IV():
    x = random.getrandbits(128)
    x |= (1 << 127) | 1

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


    ini = IV()

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


    ini = IV()

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
    aes()

if __name__ == "__main__":
    main()