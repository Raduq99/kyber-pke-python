from .params import N, K, Q, N1, N2, DU, DV
from .compress import poly_compress, poly_decompress, vec_compress, vec_decompress
from .encoding import poly_decode, poly_encode, vec_decode, vec_encode
from .poly import poly_add, poly_mult, poly_sub, vec_reduce
from .primitives import G, prf, xof
from .sampling import cbd, parse
import secrets

def keyGen():
    nonce = 0
    # init random seeds
    d = secrets.token_bytes(32)
    rho, delta = G(d)
    # generate matrix A
    A = [[0 for _ in range(K)] for _ in range(K)]
    for i in range(K):
        for j in range(K):
            A[i][j] = parse(xof(rho, j, i))
    # generate secret s
    s = []
    for i in range(K):
        seed = prf(delta, nonce).read(64 * N1)
        s.append(cbd(seed, N1))
        nonce += 1
    # generate error e
    e = []
    for i in range(K):
        seed = prf(delta, nonce).read(64 * N1)
        e.append(cbd(seed, N1))
        nonce += 1
    # t = A * s
    t = [[] for _ in range(K)]
    for i in range(K):
        t[i] = [0 for _ in range(N)]
        for j in range(K):
            t[i] = poly_add(t[i], poly_mult(A[i][j], s[j]))
    # t + e
    for i in range(K):
        t[i] = poly_add(t[i], e[i])

    pk = vec_encode(vec_reduce(t, Q), 12) + rho
    sk = vec_encode(vec_reduce(s, Q), 12)
    return (pk, sk)


def encrypt(pk, m, rand):
    assert len(m) == 32
    nonce = 0
    # decode pk
    rho = pk[-32:]
    t = vec_decode(pk[:-32], 12)
    # generate matrix At (A transposed)
    At = [[0 for _ in range(K)] for _ in range(K)]
    for i in range(K):
        for j in range(K):
            At[i][j] = parse(xof(rho, i, j))
    # generate randomness r
    r = []
    for i in range(K):
        seed = prf(rand, nonce).read(64 * N1)
        r.append(cbd(seed, N1))
        nonce += 1
    # generate error e1
    e1 = []
    for i in range(K):
        seed = prf(rand, nonce).read(64 * N2)
        e1.append(cbd(seed, N2))
        nonce += 1
    # generate error e2
    seed = prf(rand, nonce).read(64 * N2)
    e2 = cbd(seed, N2)
    # u = At * r + e1
    u = [[] for _ in range(K)]
    for i in range(K):
        u[i] = [0 for _ in range(N)]
        for j in range(K):
            u[i] = poly_add(u[i], poly_mult(At[i][j], r[j]))
    for i in range(K):
        u[i] = poly_add(u[i], e1[i])
    # v = t * r + e2 + m
    v = [0 for _ in range(N)]
    for i in range(K):
        v = poly_add(v, poly_mult(t[i], r[i]))
    v = poly_add(v, e2)
    v = poly_add(v, poly_decompress(poly_decode(m, 1), 1, Q))
    # generate ciphertext
    c1 = vec_encode(vec_compress(u, DU, Q), DU)
    c2 = poly_encode(poly_compress(v, DV, Q), DV)
    return c1 + c2

def decrypt(sk, c):
    # decode ciphertext and sk
    sep = DU * K * N // 8
    c1, c2 = c[:sep], c[sep:]
    u = vec_decompress(vec_decode(c1, DU), DU, Q)
    v = poly_decompress(poly_decode(c2, DV), DV, Q)
    s = vec_decode(sk, 12)
    # compute message m = v - s*u
    m = [0 for _ in range(N)]
    for i in range(K):
        m = poly_add(m, poly_mult(s[i], u[i]))
    m = poly_sub(v, m)
    m = poly_compress(m, 1, Q)
    return poly_encode(m, 1)