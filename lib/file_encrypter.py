from typing import List, Optional, Union
from .key_iv_generator import KeyIVGenerator
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class FileEncrypter:
    date_encrypted: bytes

    def __init__(self) -> None:
        self.date_encrypted = b""
    
    def Encrypt(self, file_in: str, passwords: List[Union[str, bytes]], salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = None)->None:
        # Generate key and IV
        key_iv_generator = KeyIVGenerator()
        key_iv_generator.GenerateMaster(passwords, salt, itr_num)

        # Read file
        file_data = FileReader.Read(file_in)
        
        # Encrypt it
        encrypter = AES.new(key_iv_generator.GetMasterKey(), AES.MODE_CBC, key_iv_generator.GetMasterIV())
        self.date_encrypted = encrypter.encrypt(pad(file_data, AES.block_size))
    
    def GetEncryptedData(self)->bytes:
        return self.date_encrypted
    
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, self.date_encrypted)