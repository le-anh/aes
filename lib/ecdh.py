import hashlib
from random import randint
from typing import Tuple
from .ecc import ECC
from .parameter_initial import EccConst, AesConst, Point

class ECDH:
    def __init__(self) -> None:
        pass

    def get_public_key(self, key_priv: int) -> Point:
        ecc = ECC()
        key_public = ecc.Point_Multiplication(key_priv)
        return key_public
    
    def get_key_secret(self, key_priv: int, key_pub: Point) -> Point:
        key_secret = ECC().Point_Multiplication(key_priv, key_pub)
        return hashlib.sha1(str(key_secret.x).encode()).digest()[:AesConst.BlockSize()]

    def get_encryption_key(self, pub_key: Point) -> Tuple[Point, Point]:
        ciphertext_priv_key = randint(2, EccConst.N-1)
        ciphertext_pub_key = ECC().Point_Multiplication(ciphertext_priv_key, EccConst.G)
        encrypt_key = ECC().Point_Multiplication(ciphertext_priv_key, pub_key)
        return encrypt_key, ciphertext_pub_key

    def get_decryption_key(self, priv_key: int, ciphertext_pub_key: Point) -> Point:
        decrypt_key = ECC().Point_Multiplication(priv_key, ciphertext_pub_key)
        return decrypt_key
    
    def point_to_bytes_key(self, point: Point) -> hex:
        return hashlib.sha1(str(point.x).encode()).digest()[:AesConst.BlockSize()]
