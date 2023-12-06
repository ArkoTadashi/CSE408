from BitVector import *
import time
from collections import deque
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

def addRoundKey(matty, hKey):
    rmatty = [
    [BitVector(hexstring=hKey[i + j * 8: i + j * 8 + 2]) for j in range(4)]          #chaangeessss
    for i in range(0, 8, 2)
    ]  

    new_matty = [
    [matty[i][j] ^ rmatty[i][j] for j in range(4)]
    for i in range(4)
    ]

    return new_matty


def byteSubstitution(matt):
   matt = [
    [BitVector(intVal=Sbox[matt[i][j].intValue()], size=8) for j in range(4)]
    for i in range(4)
   ]
   return matt

def byteSubstitutionInverse(matt):
   matt = [
    [BitVector(intVal=InvSbox[matt[i][j].intValue()], size=8) for j in range(4)]
    for i in range(4)
   ]
   return matt


def row_shift(matt):
    s_mat = [row[i:] + row[:i] for i, row in enumerate(matt)]
    return s_mat

def inv_row_shift(matt):
    s_mat = [row[-i:] + row[:-i] for i, row in enumerate(matt)]
    return s_mat

def getG(wd, rc):
    wd = wd[8:] + wd[:8]
    tempp = BitVector(bitstring = wd)
    h = 0
    for i in range(4):
        tempp[i*8:(i+1)*8] = BitVector(intVal = Sbox[tempp[i*8:(i+1)*8].intValue()], size=8)
    h = 1
    tempp[0:8] ^= rc
    h = 2
    return tempp

def key_Scheduling(key,k):
    key_bytes = k//8
    w_c = k//32
    rc = BitVector(intVal=0x01,size=8)
    num_rounds = None
    if key_bytes == 16:
        num_rounds = 10
    elif key_bytes == 24:
        num_rounds = 12
    elif key_bytes == 32:
        num_rounds = 14
    tot_w = 4 * (num_rounds + 1)
   
    key_ws = [None] * tot_w
    #key_ws = [BitVector(hexstring=key[8*i:8*(i+1)]) for i in range(w_c)]
    for i in range(w_c):
        key_ws[i] = BitVector(hexstring=key[i*8:(i+1)*8])
    for i in range(w_c, tot_w):
        tt = key_ws[i-1]
        if i % w_c != 0:
            key_ws[i] =key_ws[i-1] ^ key_ws[i-w_c]     
        else:
            tt = getG(tt, rc)
            key_ws[i] = key_ws[i-w_c] ^ tt
            rc = rc.gf_multiply_modular(BitVector(intVal = 2, size = 8), BitVector(intVal= 0B000100011011, size = 9), 8)

    chabi = [(key_ws[i*4] + key_ws[i*4+1] + key_ws[i*4+2] + key_ws[i*4+3]).get_bitvector_in_hex() for i in range(num_rounds+1)]
    return chabi

def mixColumns(matty):
    res = []
    for i in range(4):
        res_row = []
        for j in range(4):
            res_row.append(BitVector(intVal=0, size=8))
        res.append(res_row)
    
    for i in range(4):
        for j in range(4):
            t = BitVector(intVal=0, size=8)
            for l in range(4):
                pp = Mixer[i][l].gf_multiply_modular(matty[l][j], BitVector(intVal=0B000100011011, size=9), 8)   
                t ^=pp
            res[i][j] = t
    
    return res

def Inv_mixColumns(matty):
    res = []
    for i in range(4):
        res_row = []
        for j in range(4):
            res_row.append(BitVector(intVal=0, size=8))
        res.append(res_row)
    
    for i in range(4):
        for j in range(4):
            t = BitVector(intVal=0, size=8)
            for l in range(4):
                pp = InvMixer[i][l].gf_multiply_modular(matty[l][j], BitVector(intVal=0B000100011011, size=9), 8)   
                t ^=pp
            res[i][j] = t
    
    return res

def createMat(linee):
    res = []
    for i in range(4):
        res_row = []
        for j in range(4):
            res_row.append(BitVector(intVal=0, size=8))
        res.append(res_row)
    for i in range(0, 32, 2):
        res[(i//2)%4][i//8] = BitVector(hexstring=linee[i:i+2])
    return res

def mtx_decd(mtx):
    ec_text = "".join(mtx[j][i].get_bitvector_in_hex() for i in range(4) for j in range(4))
    return ec_text


def encrypt(whole_text, keyList, k):
    ec_text = ""
    key_bytes = k//8
    w_c = k//32
    ivec = '0'* int(32)
    rc = BitVector(intVal=1,size=8)
    num_rounds = None
    if key_bytes == 16:
        num_rounds = 10
    elif key_bytes == 24:
        num_rounds = 12
    elif key_bytes == 32:
        num_rounds = 14
    
    iv = BitVector(hexstring=ivec)

    for n_text in whole_text:
        temp = BitVector(hexstring = n_text)
        temp ^= iv
        temp = temp.get_bitvector_in_hex()
        mtx = createMat(temp)
        mtx = addRoundKey(mtx, keyList[0])
        
        for i in range(num_rounds):
            mtx = byteSubstitution(mtx)
            mtx = row_shift(mtx)
            if i != num_rounds-1:
                mtx = mixColumns(mtx)
            mtx = addRoundKey(mtx, keyList[i+1])       
        ivec = mtx_decd(mtx)
        iv = BitVector(hexstring = ivec)
        ec_text += ivec

    return ec_text


def decrypt(ec_text, keyList, k):
    key_bytes = k//8
    w_c = k//32
    ivec = '0'* int(32)
    ec_texts = [ec_text[i:i+32] for i in range(0, len(ec_text), 32)]
    n_text = ""

    iv = BitVector(hexstring=ivec)

    for txt in ec_texts:
        num_rounds = None
        if key_bytes == 16:
           num_rounds = 10
        elif key_bytes == 24:
           num_rounds = 12
        elif key_bytes == 32:
           num_rounds = 14
        mtx = createMat(txt)
        mtx = addRoundKey(mtx, keyList[num_rounds])
        for i in range(num_rounds):
            mtx = inv_row_shift(mtx)
            mtx = byteSubstitutionInverse(mtx)
            mtx = addRoundKey(mtx, keyList[num_rounds-i-1])
            if i != num_rounds-1:
                mtx = Inv_mixColumns(mtx)

        temp = mtx_decd(mtx)
        temp = BitVector(hexstring=temp)
        temp ^= iv
        n_text += temp.get_bitvector_in_hex()
        ivec = txt
        iv = BitVector(hexstring=ivec)

    return n_text


def process_text(temp_text,m):
    # Convert temp_text to hex
    hex_text = temp_text.encode("utf-8").hex()
    if len(hex_text) % 32 != 0:
        num_zeroes = 32 - (len(hex_text) % 32)
        
        hex_text += '0' * int(num_zeroes) 
    else :
        hex_text += '0' * 32
    return hex_text
def padd(temp_text):
    # Convert temp_text to hex
    hex_text = temp_text.encode("utf-8").hex()
    if len(hex_text) % 32 != 0:
        num_zeroes = (32 - (len(hex_text) % 32))
        num_zeroes = num_zeroes//2
        pd = hex(num_zeroes)
        j = num_zeroes + 4
        pd = pd[2:]
        hex_text = hex_text + num_zeroes*('0' + pd)  
    else :
        hex_text += '0' * 32
    return hex_text

def process_key(key, m):
    hKey = key.encode("utf-8").hex()
    print(hKey)
    if len(hKey) < m :
       x = m - len(hKey)
       hKey += '0' * int(x)
    else :
        hKey = hKey[:m]
    return hKey
       
def print_with_space(input_string):
    result = ' '.join([input_string[i:i+2] for i in range(0, len(input_string), 2)])
    print("In HEX:",result)


def txtArrCreate(txt):
    return [txt[i:i+32] for i in range(0, len(txt), 32)]

def dePadd(tt):
    if tt[-1] != '0':
        pp = tt[-1]
        dd = int(pp, 16)
        tt = tt[:-(2*dd)]
        return tt       
    return tt[:-32]

def firstPrint(key,hKey,temp_txt,hText):
    print("\nKey:")
    print("In ASCII:", key)
    print_with_space(hKey)
    print("\ntemp Text:")
    print("In ASCII:", temp_txt)
    print_with_space(hText)
    print() 

def PrintEncrypt(htxtArr, key_list, k):
    start = time.time()
    ct = encrypt(htxtArr, key_list, k)
    eTime= time.time() - start
    print("Cipher Text:")
    h = print_with_space(ct)
    print("In ASCII:", bytearray.fromhex(ct).decode('Latin1'))
    print()
    return ct , eTime

def PrintDecrypt(ct, key_list, k):
    start = time.time()
    
    dt = decrypt(ct, key_list, k)
    tt = time.time() - start
    dt = dePadd(dt)
    print("Deciphered Text:")
    h = print_with_space(dt)
    print("In ASCII:", bytearray.fromhex(dt).decode('Latin1'))
    print()
    return dt, tt

def getKeyList(hKey, k):
    start = time.time()
    key_list = key_Scheduling(hKey, k)
    tt = time.time() - start
    print(key_list)
    return tt,key_list

if __name__ == "__main__":
    k = 128
    print("Enter temp text:")
    #temp_text = input()
    temp_text='Amar matha kharap h0ye geI0 esh0b ki AESVVVgyugyibhy0'
    #temp_text="Never gonna give you up"
    print("Enter key:")
    #key = input()
    key ='Thats my Kung Fu' 
    #"BUET CSE19 Batche"
    hText = process_text(temp_text,k/4)
    hKey = process_key(key,k//4)
    
    firstPrint(key,hKey,temp_text,hText)
   
    h = padd(temp_text)
    htxtArr = txtArrCreate(h)
    print(htxtArr)
    
    tt ,key_list = getKeyList(hKey, k)
    ct,eTime = PrintEncrypt(htxtArr, key_list, k)
    dt,dTime = PrintDecrypt(ct, key_list, k)
    
    print("Execution time details:")
    print("Key Scheduling :", (tt*1000), "ms")
    print("Encryption Time:", (eTime*1000), "ms")
    print("Decryption Time:", (dTime*1000), "ms")

