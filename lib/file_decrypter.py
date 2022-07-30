from typing import List, Optional, Union
from .key_generator import KeyGenerator
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

class FileDecrypter:
    data_encrypted: bytes
    iv: bytes
    iv_size: int

    # Contructor
    def __init__(self) -> None:
        self.data_encrypted = b""
        self.iv = b""
        self.iv_size = AES.block_size
    
    # Decrypt
    def Decrypt(self, file_in: str, passwords: List[Union[str, bytes]], salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = None)->None:
        key_generator = KeyGenerator(passwords, salt, itr_num)
        # Read file
        file_data = FileReader.Read(file_in)
        self.iv = file_data[-self.iv_size:]
        file_data = file_data[:len(file_data)-self.iv_size]
        # Decrypt it
        decrypter = AES.new(key_generator.GetMasterKey(), AES.MODE_CBC , self.iv)
        self.data_encrypted = unpad(decrypter.decrypt(file_data), AES.block_size)
    
    # Get decrypted data
    def GetDecryptedData(self)->bytes:
        return self.data_encrypted
    
    # Save to file
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, self.data_encrypted)
    