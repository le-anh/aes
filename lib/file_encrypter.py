import base64
import json
from typing import Any, List, Optional, Union
from .file_reader import FileReader
from .file_writer import FileWriter
from .key_iv_generator import KeyIVGenerator
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class FileEncrypter:
    data_encrypted: Any
    iv: bytes

    def __init__(self) -> None:
        self.date_encrypted = b""
        self.iv = b""
        self.enc_time = 0
    
    def Encrypt(self, file_in: str, passwords: List[Union[str, bytes]], salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = None)->None:
        key_generator = KeyIVGenerator(passwords, salt, itr_num)
        # key_generator.GenerateMaster(passwords, salt, itr_num)

        file_data = FileReader.Read(file_in)    # Read file
        encrypter = AES.new(key_generator.GetMasterKey(), AES.MODE_CBC)    # Encrypt it
        encrypted_data = encrypter.encrypt(pad(file_data, AES.block_size))
        print(encrypted_data)
        print(base64.b64encode(encrypted_data))
        print(encrypter.iv)
        print(base64.b64encode(encrypter.iv))
       
        encryptedObj = {
            'ciphertext': str(base64.b64encode(encrypted_data))[2:-1],
            'iv': str(base64.b64encode(encrypter.iv))[2:-1]
        }
        # self.date_encrypted = encrypter.encrypt(pad(file_data, AES.block_size))

        self.data_encrypted = json.dumps(encryptedObj)
        self.iv = encrypter.iv
    
    def GetEncryptedData(self)->bytes:
        return self.date_encrypted

    def GetIV(self)->bytes:
        return self.iv
    
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, self.data_encrypted)
        # FileWriter.Write(file_out, b''.join([self.data_encrypted, self.iv]))