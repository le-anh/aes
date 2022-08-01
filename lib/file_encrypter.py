from datetime import datetime
from typing import List, Optional, Union
from .key_generator import KeyGenerator
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from memory_profiler import profile

class FileEncrypter:
    date_encrypted: bytes
    iv: bytes

    def __init__(self) -> None:
        self.date_encrypted = b""
        self.iv = b""
    
    @profile
    def Encrypt(self, file_in: str, passwords: List[Union[str, bytes]], salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = None)->None:
        # Generate key
        key_generator = KeyGenerator(passwords, salt, itr_num)
        # Read file
        file_data = FileReader.Read(file_in)
        # Encrypt it
        encrypter = AES.new(key_generator.GetMasterKey(), AES.MODE_CBC)
        self.date_encrypted = encrypter.encrypt(pad(file_data, AES.block_size))
        self.iv = encrypter.iv
    
    def GetEncryptedData(self)->bytes:
        return self.date_encrypted

    def GetIV(self)->bytes:
        return self.iv
    
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, b''.join([self.date_encrypted, self.iv]))