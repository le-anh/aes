import base64
import json
from typing import Any, List, Optional, Union
from .ecc import Point
from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from .key_iv_generator import KeyIVGenerator
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class FileEncrypter:
    data_encrypted: Any
    iv: bytes
    key_secret_encrypt: Point
    ciphertext_pub_key: Point

    def __init__(self, key_public: Optional[int]) -> None:
        self.date_encrypted = b""
        self.iv = b""
        if key_public:
            self.key_secret_encrypt, self.ciphertext_pub_key = ECDH().get_encryption_key(key_public)
    
    def Encrypt(self, file_in: str, passwords: Optional[List[Union[str, bytes]]] = None, salt: Optional[Union[str, bytes]] = None, itr_num: Optional[int] = None)->None:
        file_data = FileReader.Read(file_in)   # Read file
        encrypter = AES.new(ECDH().point_to_bytes_key(self.key_secret_encrypt), AES.MODE_CBC)    # Encrypt it
        encrypted_data = encrypter.encrypt(pad(file_data, AES.block_size))
        encrypted_obj = {
            'ciphertext': str(base64.b64encode(encrypted_data))[2:-1],
            'iv': str(base64.b64encode(encrypter.iv))[2:-1],
            'x': str(hex(self.ciphertext_pub_key.x))[2:],
            'y': str(hex(self.ciphertext_pub_key.y))[2:]
        }
        self.data_encrypted = json.dumps(encrypted_obj)
        self.iv = encrypter.iv
    
    def GetEncryptedData(self)->bytes:
        return self.date_encrypted

    def GetIV(self)->bytes:
        return self.iv
    
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, self.data_encrypted)