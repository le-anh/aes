import os
from typing import Optional, Union
from .pbkdf2_sha512 import Pbkdf2Sha512
from .aes_const import AesConst

class KeyIVGeneratorConst:
    DEF_ITR_NUM: int = 1024 * 512
    DEF_SALT: bytes = b"[]=?Aes_CiPhEr<>()"

class KeyIVGenerator:
    master_key: bytes
    master_iv: bytes
    internal_key: bytes
    internal_iv: bytes

    def __init__(self) -> None:
        self.master_key = b""
        self.master_iv = b""
        self.internal_key = b""
        self.internal_iv = b""

    def GenerateMaster(self, password: Union[str, bytes], salt: Optional[Union[str, bytes]], itr_num: Optional[int]) -> None:
        itr_num = KeyIVGeneratorConst.DEF_ITR_NUM if itr_num is None else itr_num
        if itr_num <= 0:
            raise ValueError(f"Invalid interation number ({itr_num})")

        salt = KeyIVGeneratorConst.DEF_SALT if salt is None else salt
        
        kdf = Pbkdf2Sha512.Compute(password, salt, itr_num)
        self.master_key = kdf[:AesConst.KeySize()]
        self.master_iv = kdf[AesConst.KeySize(): AesConst.KeySize() + AesConst.IVSize()]
    
    def GenerateInternal(self)->None:
        self.internal_key = os.urandom(AesConst.KeySize())
        self.internal_iv = os.urandom(AesConst.IVSize())

    def GetMasterKey(self)->bytes:
        return self.master_key
    
    def GetMasterIV(self)->bytes:
        return self.master_iv
    
    def GetInternalKey(self)->bytes:
        return self.internal_key
    
    def GetInternalIV(self)->bytes:
        return self.internal_iv