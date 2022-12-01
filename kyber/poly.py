from kyber import params
import numpy as np

def poly_mult(a, b):
    assert len(a) == params.N
    assert len(b) == params.N
    c = np.polymul(a, b)
    j = 0
    for i in range(256, len(c)):
        c[j] -= c[i]
        c[j] %= params.Q
        j += 1
    return c[:256]

def poly_add(a, b):
    assert len(a) == params.N
    assert len(b) == params.N
    return [(a_i + b_i) % params.Q for (a_i, b_i) in zip(a, b)]

def poly_sub(a, b):
    assert len(a) == params.N
    assert len(b) == params.N
    return [(a_i - b_i) for (a_i, b_i) in zip(a, b)]

def poly_reduce(a, q):
    assert len(a) == params.N
    return [a_i % q for a_i in a]

def vec_reduce(v, q):
    return [poly_reduce(poly, q) for poly in v]
