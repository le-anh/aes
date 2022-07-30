from typing import List, Optional, Union
from .key_iv_generator import KeyIVGenerator
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

class FileDecrypter:
    data_encrypted: bytes

    # Contructor
    def __init__(self) -> None:
        self.data_encrypted = b""
    
    # Decrypt
    def Decrypt(self, file_in: str, passwords: List[Union[str, bytes]], salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = None)->None:
         # Generate key and IV
        key_iv_generator = KeyIVGenerator()
        key_iv_generator.GenerateMaster(passwords, salt, itr_num)

        # Read file
        file_data = FileReader.Read(file_in)
        
        # Decrypt it
        decrypter = AES.new(key_iv_generator.GetMasterKey(), AES.MODE_CBC, key_iv_generator.GetMasterIV())
        self.data_encrypted = unpad(decrypter.decrypt(file_data), AES.block_size)
        
    
    # Get decrypted data
    def GetDecryptedData(self)->bytes:
        return self.data_encrypted
    
    # Save to file
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, self.data_encrypted)
    