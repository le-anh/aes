from typing import Union, Optional
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from .utils import Utils

class Pbkdf2:
    @staticmethod
    def Compute(password: Union[str, bytes], salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = 10000)->bytes:
        return PBKDF2(Utils.Decode(password), Utils.Encode(salt), SHA512.digest_size, itr_num, hmac_hash_module=SHA512)