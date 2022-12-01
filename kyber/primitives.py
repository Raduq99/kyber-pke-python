from Crypto.Hash import cSHAKE128, SHAKE256, SHA3_256, SHA3_512

def prf(b: bytes, nonce: int):
    shake = SHAKE256.new(b + nonce.to_bytes(1, "little"))
    return shake

def xof(b: bytes, i: int, j: int):
    shake = cSHAKE128.new(b, i.to_bytes(1, "little") + j.to_bytes(1, "little"))
    return shake

def H(b: bytes):
    hash = SHA3_256.new(b)
    return hash.digest()

def G(b: bytes):
    hash = SHA3_512.new(b)
    digest = hash.digest()
    return (digest[:32], digest[32:])

def kdf(b: bytes):
    shake = SHAKE256.new(b)
    return shake