from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from .const import AesConst, Point
from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from Crypto.Util.Padding import unpad

class FileDecrypter:
    decrypted_data: bytes
    decrypt_key: bytes

    def __init__(self, priv_key: int = None, file_key: str = None) -> None:
        self.decrypted_data = b""
        if file_key:
            with open("result/key/" + file_key + ".key", "r") as f:
                f.readline()
                cipher_pub_key = Point(int(f.readline(), 16), int(f.readline(), 16))
                decrypt_key = ECDH().get_decryption_key(priv_key, cipher_pub_key)
                self.decrypt_key = ECDH().point_to_bytes_key(decrypt_key)
                print(f"Decrypt key: {self.decrypt_key}")
    
    def decrypt(self, file_in: str, receive_priv_key: int, send_pub_key: Point) -> None:
        try:
            file_data = FileReader.read("result/enc_" + file_in)
            tag, file_data = file_data[-(AesConst.block_size()):], file_data[:-(AesConst.block_size())]
            iv, file_data = file_data[-AesConst.iv_size():], file_data[:-AesConst.iv_size()]
            cmac_key = ECDH().point_to_bytes_key(ECDH().get_cmac_key(receive_priv_key, send_pub_key))
            tag_check = CMAC.new(cmac_key, msg=file_data, ciphermod=AES)
            try:
                tag_check.verify(tag)
                # iv = file_data[-(AesConst.iv_size()+(AesConst.block_size()*2)):-(AesConst.block_size()*2)]
                # file_data = file_data[:len(file_data)-AesConst.iv_size()]
                decrypter = AES.new(self.decrypt_key, AES.MODE_CBC, iv)
                self.decrypted_data = unpad(decrypter.decrypt(file_data), AesConst.pad_size())
                print(f"File data was decrypted.")

            except ValueError:
                print("Tag is invalid.")

            print(20*'=' + "Decryption" + 20*'=')
            print(f'iv: {iv}')
            print(f'tag: {tag}')
            
        except(ValueError, KeyError):
            print("Incorrect decryption")
    
    def get_decrypted_data(self) -> bytes:
        return self.decrypted_data
    
    def save_to(self, file_out: str) -> None:
        if self.get_decrypted_data():
            FileWriter.write("result/dec_" + file_out, self.get_decrypted_data().decode())
            print(f"Decrypted data was saved.")
        else:
            print(f"Decrypted data empty.")