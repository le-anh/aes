import hashlib
from random import randint, random
from Crypto.Cipher import AES
from .ecc import EccConst, ECC

class ECDH:
    def __init__(self) -> None:
        pass

    def get_key_public(self, key_priv):
        ecc = ECC()
        key_public = ecc.Point_Multiplication(key_priv)
        return key_public
    
    def get_key_secret(self, key_priv, key_pub):
        key_secret = ECC().Point_Multiplication(key_priv, key_pub)
        return hashlib.sha1(str(key_secret.x).encode()).digest()[:AES.block_size]

    def get_encryption_key(self, pub_key):
        ciphertext_priv_key = randint(2, EccConst.N-1)
        ciphertext_pub_key = ECC().Point_Multiplication(ciphertext_priv_key, EccConst.G)
        shared_ecc_key = ECC().Point_Multiplication(ciphertext_priv_key, pub_key)
        return shared_ecc_key, ciphertext_pub_key

    def get_decryption_key(self, priv_key, ciphertext_pub_key):
        shared_ecc_key = ECC().Point_Multiplication(priv_key, ciphertext_pub_key)
        return shared_ecc_key
    
    def point_to_bytes_key(self, point):
        return hashlib.sha1(str(point.x).encode()).digest()[:AES.block_size]
    
    def compress_point(self, point):
        return hex(point.x) + hex(point.y % 2)[2:]
