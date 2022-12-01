from kyber import params
from kyber.bits import bytesToBits

def cbd(b: bytes, n: int):
    assert len(b) // 64 == n
    bits = bytesToBits(b)
    f = []
    for i in range(256):
        ra = sum([int(bits[2*i*n + j], 2) for j in range(n)])
        rb = sum([int(bits[2*i*n + n + j], 2) for j in range(n)])
        f.append(ra - rb)
    return f

def parse(byteStream):
    j = 0
    a = [0 for _ in range(params.N)]
    while j < params.N:
        b = byteStream.read(3)
        d1 = b[0] + 256 * (b[1] % 16)
        d2 = b[1] // 16 + 16 * b[2]
        if d1 < params.Q:
            a[j] = d1
            j += 1
        if d2 < params.Q and j < params.N:
            a[j] = d2
            j += 1
    return a