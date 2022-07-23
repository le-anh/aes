from datetime import datetime
import hashlib

P = 47  # P is a prime
G = 2   # G is a primitive element in the subgroup with 23 elements

def exp_mod(a, b, p):
    result = 1
    for i in bin(b)[2:]:
        result *= result
        if int(i):
            result *= a
        result %= p
    return result

def get_public_key(private_key):
    return exp_mod(G, private_key, P)

def get_secret_key(public_key, private_key):
    secret_key = exp_mod(public_key, private_key, P)
    return hashlib.sha1(bytes(secret_key)).digest()[:16]