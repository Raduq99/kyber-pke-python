def poly_compress(x, d: int, q: int):
    return [round((2**d / q) * x_i) % 2**d for x_i in x]

def vec_compress(v, d, q):
    return [poly_compress(v_i, d, q) for v_i in v]

def poly_decompress(x, d: int, q: int):
    return [round((q / 2**d) * x_i) for x_i in x]

def vec_decompress(v, d, q):
    return [poly_decompress(v_i, d, q) for v_i in v]

