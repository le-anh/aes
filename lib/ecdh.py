import hashlib
from Crypto.Cipher import AES
from .ecc import ECC

class ECDH:
    def __init__(self) -> None:
        pass

    def get_key_public(self, key_priv):
        key_public = ECC().Point_Multiplication(key_priv)
        return key_public
    
    def get_key_secret(self, key_priv, key_pub):
        key_secret = ECC().Point_Multiplication(key_priv, key_pub)
        return hashlib.sha1(str(key_secret.x).encode()).digest()[:AES.block_size]