from datetime import datetime
from typing import List, Optional, Union
from numpy import longlong
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from memory_profiler import profile

class FileEncrypter:
    date_encrypted: bytes
    iv: bytes
    enc_time: longlong

    def __init__(self) -> None:
        self.date_encrypted = b""
        self.iv = b""
        self.enc_time = 0
    
    @profile
    def Encrypt(self, file_in: str, passwords: List[Union[str, bytes]], salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = None)->None:
        
        # Read file
        file_data = FileReader.Read(file_in)
        # Encrypt it
        encrypter = AES.new(passwords, AES.MODE_CBC)
        t0 = datetime.now()
        self.date_encrypted = encrypter.encrypt(pad(file_data, AES.block_size))
        t1 = datetime.now()
        self.iv = encrypter.iv
        self.enc_time = (t1-t0).total_seconds()*1000.0
    
    def GetEncryptedData(self)->bytes:
        return self.date_encrypted

    def GetIV(self)->bytes:
        return self.iv
    
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, b''.join([self.date_encrypted, self.iv]))

    def GetEncryptedTime(self):
        return self.enc_time