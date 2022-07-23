import hashlib
import random
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

P = 115792089237316195423570985008687907853269984665640564039457584007908834671663  # P = 2^256 - 2^32 - 977
A = 1
B = 7
G = Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # order of E

def gcd(a, b):
    while b > 0:
        r = a % b
        a = b
        b = r
    return a

def invert(n, P=P):
    if n < 0: n = P + n
    a1, a2, a3 = 1, 0, P
    b1, b2, b3 = 0, 1, n
    while True:
        if b3 == 0:
            return "no inverse"
        if b3 == 1:
            return b2 if b2 >= 0 else P+b2
        q = a3//b3
        t1, t2, t3 = a1 - q * b1, a2 - q * b2, a3 - q * b3
        a1, a2, a3 = b1, b2, b3
        b1, b2, b3 = t1, t2, t3

def Point_Double(Q):
    if Q.y:
        s = ((3*Q.x*Q.x + A) * invert(2*Q.y)) % P
        x = (s*s - Q.x -Q.x) % P
        y = (s*(Q.x - x) - Q.y) % P
        return Point(x, y)
    return Point(0, 0)

def Point_Add(Q1, Q2):
    if Q2.x - Q1.x:
        s = ((Q2.y - Q1.y) * invert(Q2.x - Q1.x)) % P
        x = (s*s - Q1.x - Q2.x) % P
        y = (s*(Q1.x - x) - Q1.y) % P
        return Point(x, y)
    return Point(0, 0)

def Point_Multiplication(d, Q=G):
    T = Point(Q.x, Q.y)
    for i in bin(d)[3:]:
        T = Point_Double(T)
        if(int(i)):
            T = Point_Add(T, Q)
    return T

def get_public_key(d, Q=G):
    return Point_Multiplication(d, Q)

def get_secret_key(d, Q):
    result_point = Point_Multiplication(d, Q)
    return hashlib.sha1(str(result_point.x).encode()).digest()[:16]

def encryption_key(pub_key):
    ciphertext_priv_key = random.randint(1, N-1)
    ciphertext_pub_key = Point_Multiplication(ciphertext_priv_key, G)
    shared_ecc_key = Point_Multiplication(ciphertext_priv_key, pub_key)
    return hashlib.sha1(str(shared_ecc_key.x).encode()).digest()[:16], ciphertext_pub_key

def decryption_key(priv_key, ciphertext_pub_key):
    shared_ecc_key = Point_Multiplication(priv_key, ciphertext_pub_key)
    return hashlib.sha1(str(shared_ecc_key.x).encode()).digest()[:16]

def test():
    key_priv_a = 1023
    key_priv_b = 9081
    key_pub_a = Point_Multiplication(key_priv_a, G)
    key_pub_b = Point_Multiplication(key_priv_b, G)

    # key_secret_a = Point_Multiplication(key_priv_a, key_pub_b)
    # key_secret_b = Point_Multiplication(key_priv_b, key_pub_a)
    # print(key_secret_a.x, key_secret_a.y)
    # print(key_secret_b.x, key_secret_b.y)

    shared_ecc_key, ciphertext_pub_key = encryption_key(key_pub_b)
    shared_ecc_key2 = decryption_key(key_priv_b, ciphertext_pub_key)
    print(shared_ecc_key)
    print(shared_ecc_key2)

# test()