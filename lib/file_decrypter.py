from typing import Optional
from .ecc import Point
from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class FileDecrypter:
    data_encrypted: bytes
    iv: bytes
    iv_size: int
    priv_key: int
    ciphertext_pub_key: Point
    key_secret_decrypt: bytes

    def __init__(self, priv_key: Optional[int] = None, file_key: Optional[str] = None) -> None:
        self.data_encrypted = b""
        self.iv = b""
        self.iv_size = AES.block_size
        self.priv_key = priv_key
        if file_key:
            with open(file_key, "r") as f:
                f.readline()
                self.ciphertext_pub_key = Point(int(f.readline(), 16), int(f.readline(), 16))
                secret_decrypt = ECDH().get_decryption_key(self.priv_key, self.ciphertext_pub_key)
                self.key_secret_decrypt = ECDH().point_to_bytes_key(secret_decrypt)
                print(f"Decrypt key: {self.key_secret_decrypt}")
    
    def Decrypt(self, file_in: str)->None:
        try:
            file_data = FileReader.Read(file_in)    # Read file
            self.iv = file_data[-self.iv_size:]
            file_data = file_data[:len(file_data)-self.iv_size]
            decrypter = AES.new(self.key_secret_decrypt, AES.MODE_CBC, self.iv)   # Decrypt it
            self.data_encrypted = unpad(decrypter.decrypt(file_data), AES.block_size)
            print(f"File data was decrypted.")

        except(ValueError, KeyError):
            print("Incorrect decryption")
    
    def GetDecryptedData(self)->bytes:
        return self.data_encrypted
    
    def SaveTo(self, file_out: str)->None:
        FileWriter.Write(file_out, self.data_encrypted.decode())
        print(f"Decrypted data was stored.")