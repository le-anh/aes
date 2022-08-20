from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from .const import AesConst, Point
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class FileDecrypter:
    decrypted_data: bytes
    iv: bytes
    priv_key: int
    cipher_pub_key: Point
    decrypt_key: bytes

    def __init__(self, priv_key: int = None, file_key: str = None) -> None:
        self.decrypted_data = b""
        self.iv = b""
        self.priv_key = priv_key
        if file_key:
            with open("result/key/" + file_key + ".key", "r") as f:
                f.readline()
                self.cipher_pub_key = Point(int(f.readline(), 16), int(f.readline(), 16))
                decrypt_key = ECDH().get_decryption_key(self.priv_key, self.cipher_pub_key)
                self.decrypt_key = ECDH().point_to_bytes_key(decrypt_key)
                print(f"Decrypt key: {self.decrypt_key}")
    
    def decrypt(self, file_in: str) -> None:
        try:
            file_data = FileReader.read("result/enc_" + file_in)
            self.iv = file_data[-AesConst.iv_size():]
            file_data = file_data[:len(file_data)-AesConst.iv_size()]
            decrypter = AES.new(self.decrypt_key, AES.MODE_CBC, self.iv)
            self.decrypted_data = unpad(decrypter.decrypt(file_data), AesConst.pad_size())
            print(f"File data was decrypted.")
        except(ValueError, KeyError):
            print("Incorrect decryption")
    
    def get_decrypted_data(self) -> bytes:
        return self.decrypted_data
    
    def save_to(self, file_out: str) -> None:
        FileWriter.write("result/dec_" + file_out, self.get_decrypted_data().decode())
        print(f"Decrypted data was stored.")