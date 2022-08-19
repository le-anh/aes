import hashlib
from random import randint
from typing import Tuple
from .ecc import ECC
from .parameter_initial import EccConst, AesConst, Point

class ECDH:
    def __init__(self) -> None:
        pass

    def get_public_key(self, priv_key: int) -> Point:
        pub_key = ECC().point_multiplication(priv_key)
        return pub_key
    
    def get_encryption_key(self, pub_key: Point) -> Tuple[Point, Point]:
        cipher_priv_key = randint(2, EccConst.N-1)
        cipher_pub_key = ECC().point_multiplication(cipher_priv_key, EccConst.G)
        encrypt_key = ECC().point_multiplication(cipher_priv_key, pub_key)
        return encrypt_key, cipher_pub_key

    def get_decryption_key(self, priv_key: int, cipher_pub_key: Point) -> Point:
        decrypt_key = ECC().point_multiplication(priv_key, cipher_pub_key)
        return decrypt_key
    
    def point_to_bytes_key(self, point: Point) -> bytes:
        return hashlib.sha256(str(point.x).encode() + str(point.y).encode()).digest()[:AesConst.key_size()]
