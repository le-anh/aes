from typing import Union
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from .utils import Utils

class Pbkdf2Sha512:
    @staticmethod
    def Compute(password: Union[str, bytes], salt: Union[str, bytes], itr_num: int)->bytes:
        return PBKDF2(Utils.Decode(password), Utils.Encode(salt), SHA512.digest_size, itr_num, hmac_hash_module=SHA512)