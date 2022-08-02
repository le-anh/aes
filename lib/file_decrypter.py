from base64 import encode
import base64
import encodings
import json
from typing import List, Optional, Union
from .file_reader import FileReader
from .file_writer import FileWriter
from .key_iv_generator import KeyIVGenerator
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

class FileDecrypter:
    data_encrypted: bytes
    iv: bytes
    iv_size: int

    def __init__(self) -> None:
        self.data_encrypted = b""
        self.iv = b""
        self.iv_size = AES.block_size
        self.dec_time = 0
    
    def Decrypt(self, file_in: str, passwords: List[Union[str, bytes]], salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = None)->None:
        # try:
        key_generator = KeyIVGenerator(passwords, salt, itr_num)
        # key_generator.GenerateMaster(passwords, salt, itr_num)

        file_data = FileReader.Read(file_in)    # Read file
        # self.iv = file_data[-self.iv_size:]
        data_obj = json.loads(file_data)
        ciphertext = base64.b64decode(data_obj['ciphertext']) #  bytes(data_obj['ciphertext'].encode("utf-8"))
        self.iv = base64.b64decode(data_obj['iv'])
        print(ciphertext)
        print((self.iv))
        # file_data = file_data[:len(file_data)-self.iv_size]
        decrypter = AES.new(key_generator.GetMasterKey(), AES.MODE_CBC, self.iv)   # Decrypt it
        self.data_encrypted = unpad(decrypter.decrypt(ciphertext), AES.block_size)
        print(self.data_encrypted[2:-1])
        # except(ValueError, KeyError):
        #     print("Incorrect decryption")
    
    def GetDecryptedData(self)->bytes:
        return self.data_encrypted
    
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, self.data_encrypted.decode())