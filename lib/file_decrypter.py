from .ecc import Point
from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class FileDecrypter:
    decrypted_data: bytes
    iv: bytes
    iv_size: int
    priv_key: int
    ciphertext_pub_key: Point
    decrypt_key: bytes

    def __init__(self, priv_key: int = None, file_key: str = None) -> None:
        self.decrypted_data = b""
        self.iv = b""
        self.iv_size = AES.block_size
        self.priv_key = priv_key
        if file_key:
            with open("result/key/" + file_key + ".key", "r") as f:
                f.readline()
                self.ciphertext_pub_key = Point(int(f.readline(), 16), int(f.readline(), 16))
                decrypt_key = ECDH().get_decryption_key(self.priv_key, self.ciphertext_pub_key)
                self.decrypt_key = ECDH().point_to_bytes_key(decrypt_key)
                print(f"Decrypt key: {self.decrypt_key}")
    
    def Decrypt(self, file_in: str) -> None:
        try:
            file_data = FileReader.Read("result/enc_" + file_in)    # Read file
            self.iv = file_data[-self.iv_size:]
            file_data = file_data[:len(file_data)-self.iv_size]
            decrypter = AES.new(self.decrypt_key, AES.MODE_CBC, self.iv)   # Decrypt it
            self.decrypted_data = unpad(decrypter.decrypt(file_data), AES.block_size)
            print(f"File data was decrypted.")
        except(ValueError, KeyError):
            print("Incorrect decryption")
    
    def GetDecryptedData(self) -> bytes:
        return self.decrypted_data
    
    def SaveTo(self, file_out: str) -> None:
        FileWriter.Write("result/dec_" + file_out, self.decrypted_data.decode())
        print(f"Decrypted data was stored.")