from kyber.bits import bytesToBits
from kyber import params

def bitsToBytes(bits):
    return int(bits, base=2).to_bytes(len(bits) // 8, "big")

def poly_decode(bytes: bytes, l: int):
    bitsArray = bytesToBits(bytes)
    f = []
    for i in range(256):
        fi = 0
        for j in range(l):
            fi += int(bitsArray[i*l + j]) * (2 ** j)
        f.append(fi)
    return f

def poly_encode(polynomial, l: int):
    bitsArray = ""
    for coeff in polynomial:
        bits = bin(coeff)[2:]
        bits = "0" * l + bits
        bits = bits[-l:]
        bitsArray += bits[::-1]
    return bitsToBytes(bitsArray)

def vec_decode(b: bytes, l):
    poly = []
    size = len(b) // params.K
    for i in range(params.K):
        p = poly_decode(b[i * size: (i + 1) * size], l)
        poly.append(p)
    return poly

def vec_encode(v, l):
    res = b''
    for poly in v:
        res += poly_encode(poly, l)
    return res