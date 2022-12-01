def byteToBits(inputByte):
    bits = bin(inputByte)[2:]
    padding = "0" * (8 - len(bits))
    return padding + bits

def bytesToBits(inputBytes: bytes):
    bitsArray = ""
    for byte in inputBytes:
        bitsArray += byteToBits(byte)
    return bitsArray
