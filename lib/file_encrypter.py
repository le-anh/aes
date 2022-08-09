import base64
from typing import Any, List, Optional, Union
from .ecc import Point
from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class FileEncrypter:
    data_encrypted: Any
    iv: bytes
    key_secret_encrypt: bytes
    ciphertext_pub_key: Point

    def __init__(self, key_public: Optional[int]) -> None:
        self.data_encrypted = b""
        self.iv = b""
        if key_public:
            key_secret_encrypt, self.ciphertext_pub_key = ECDH().get_encryption_key(key_public)
            self.key_secret_encrypt = ECDH().point_to_bytes_key(key_secret_encrypt)

    def Encrypt(self, file_in: str)->None:
        file_data = FileReader.Read(file_in)   # Read file
        encrypter = AES.new(self.key_secret_encrypt, AES.MODE_CBC)    # Encrypt it
        self.data_encrypted = encrypter.encrypt(pad(file_data, AES.block_size))
        self.iv = encrypter.iv
    
    def GetEncryptedData(self)->bytes:
        return self.data_encrypted

    def GetIV(self)->bytes:
        return self.iv
    
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, b''.join([self.data_encrypted, self.iv]), 'wb')
        self.__Save_Key_File(file_out)

    def __Save_Key_File(self, file_name):
        with open(file_name + ".key", 'w') as f:
            f.write("-----BEGIN KEY REQUEST-----\n")
            f.write(str(hex(self.ciphertext_pub_key.x))[2:] + "\n")
            f.write(str(hex(self.ciphertext_pub_key.y))[2:] + "\n")
            f.write("-----END KEY REQUEST-----")
