import base64
import json
from typing import List, Optional, Union
from .ecc import Point
from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

class FileDecrypter:
    data_encrypted: bytes
    iv: bytes
    iv_size: int
    priv_key: int
    ciphertext_pub_key: Point

    def __init__(self, priv_key: Optional[int] = None) -> None:
        self.data_encrypted = b""
        self.iv = b""
        self.iv_size = AES.block_size
        self.priv_key = priv_key
    
    def Decrypt(self, file_in: str, passwords: Optional[List[Union[str, bytes]]] = None, salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = None)->None:
        try:
            file_data = FileReader.Read(file_in, "r")    # Read file
            data_obj = json.loads(file_data)
            ciphertext = base64.b64decode(data_obj['ciphertext'])
            self.iv = base64.b64decode(data_obj['iv'])
            self.ciphertext_pub_key = Point(int(data_obj['x'], 16), int(data_obj['y'], 16))
            # file_data = file_data[:len(file_data)-self.iv_size]

            key_secret_decrypt = ECDH().get_decryption_key(self.priv_key, self.ciphertext_pub_key)
            decrypter = AES.new(ECDH().point_to_bytes_key(key_secret_decrypt), AES.MODE_CBC, self.iv)   # Decrypt it
            self.data_encrypted = unpad(decrypter.decrypt(ciphertext), AES.block_size)
        except(ValueError, KeyError):
            print("Incorrect decryption")
    
    def GetDecryptedData(self)->bytes:
        return self.data_encrypted
    
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, self.data_encrypted.decode())