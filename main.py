from secrets import token_bytes
from kyber import keyGen, encrypt, decrypt
import sys

def pad(m: bytes) -> bytes:
    """ naive padding with 0x0 bytes"""
    assert len(m) <= 32, "Cannot encrypt more than 32 bytes"
    return m + b'0' * (32 - len(m))

def test(iter: int):
    print(f"Running {iter} tests...")
    pk, sk = keyGen()
    for i in range(iter):
        m = token_bytes(32)
        rand = token_bytes(32)
        cipher = encrypt(pk, m, rand)
        plain = decrypt(sk, cipher)
        assert plain == m, "Inconsistency found!"
        print(f"Test {i} successful.")
    print("Test run successful!")

def main():
    if len(sys.argv) == 1:
        test(10)
        return
    message = pad(sys.argv[1].encode("ascii"))
    print(message)
    pk, sk = keyGen()
    rand = token_bytes(32)
    cipher = encrypt(pk, message, rand)
    plain = decrypt(sk, cipher)
    print(f"Message: {message}\nDecryption: {plain}")
    assert plain == message, f"Plaintext and initial message are different:\n {message != plain}"

if __name__ == "__main__":
    main()