from typing import Optional, Union
from .pbkdf2_sha512 import Pbkdf2Sha512
from .aes_const import AesConst

class KeyGeneratorConst:
    DEF_ITR_NUM: int = 1024 * 512   # it is recommended to use at least 1000000 (1 million) iterations. (https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html)
    DEF_SALT: bytes = b"[]=?Aes_CiPhEr<>()"

class KeyGenerator:
    master_key: bytes
   
    def __init__(self, password: Optional[Union[str, bytes]], salt: Optional[Union[str, bytes]], itr_num: Optional[int]) -> None:
        itr_num = KeyGeneratorConst.DEF_ITR_NUM if itr_num is None else itr_num
        if itr_num <= 0:
            raise ValueError(f"Invalid interation number ({itr_num})")
        salt = KeyGeneratorConst.DEF_SALT if salt is None else salt
        kdf = Pbkdf2Sha512.Compute(password, salt, itr_num)
        self.master_key = kdf[:AesConst.KeySize()]

    def GenerateMaster(self, password: Union[str, bytes], salt: Optional[Union[str, bytes]], itr_num: Optional[int]) -> None:
        itr_num = KeyGeneratorConst.DEF_ITR_NUM if itr_num is None else itr_num
        if itr_num <= 0:
            raise ValueError(f"Invalid interation number ({itr_num})")
        salt = KeyGeneratorConst.DEF_SALT if salt is None else salt
        kdf = Pbkdf2Sha512.Compute(password, salt, itr_num)
        self.master_key = kdf[:AesConst.KeySize()]
        self.master_iv = kdf[AesConst.KeySize(): AesConst.KeySize() + AesConst.IVSize()]
    
    def GetMasterKey(self)->bytes:
        return self.master_key