from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from .const import AesConst, Point
from .kdf import Pbkdf2
from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from Crypto.Util.Padding import pad

class FileEncrypter:
    encrypted_data: bytes
    iv: bytes
    encrypt_key: bytes
    cipher_pub_key: Point
    kdf_key: bytes

    def __init__(self, pub_key: Point = None) -> None:
        self.encrypted_data = b""
        self.iv = b""
        self.kdf_key = b""
        if pub_key:
            encrypt_key, self.cipher_pub_key = ECDH().get_encryption_key(pub_key)
            self.encrypt_key = ECDH().point_to_bytes_key(encrypt_key)
            # self.kdf_key = Pbkdf2.Compute(self.encrypt_key)
            # print(f'kdf key (encryption): {self.kdf_key}')
            print(f"Cipher public key: {ECDH().point_to_bytes_key(self.cipher_pub_key)}")
            print(f"Encrypt key: {self.encrypt_key}")
    
    def encrypt(self, file_in: str) -> None:
        file_data = FileReader.read("original/" + file_in)
        encrypter = AES.new(self.encrypt_key, AES.MODE_CBC)
        self.encrypted_data = encrypter.encrypt(pad(file_data, AesConst.pad_size()))
        self.iv = encrypter.iv
        print("File data was encrypted.")
    
    def get_encrypted_data(self) -> bytes:
        return self.encrypted_data

    def get_iv(self) -> bytes:
        return self.iv

    def get_tag(self, send_priv_key: int, receive_pub_key: Point) -> bytes:
        cmac_key = ECDH().point_to_bytes_key(ECDH().get_cmac_key(send_priv_key, receive_pub_key))
        tag = CMAC.new(cmac_key, msg=self.get_encrypted_data(), ciphermod=AES)
        return tag.digest()
    
    def save_to(self, file_out: str, send_priv_key: int, receive_pub_key: Point) -> None:
        print(20*'=' + "Encryption" + 20*'=')
        print(f'iv: {self.get_iv()}')
        print(f'tag: {self.get_tag(send_priv_key, receive_pub_key)}')
        if self.get_encrypted_data():
            FileWriter.write("result/enc_" + file_out, b''.join([self.get_encrypted_data(), self.get_iv(), self.get_tag(send_priv_key, receive_pub_key)]), 'wb')
            self.save_file_key(file_out)
            print("Encrypted data was saved.")
        else:
            print("Encrypted data empty.")

    def save_file_key(self, file_name: str) -> None:
        with open("result/key/" + file_name[:-3] + "key", 'w') as f:
            f.write("-----BEGIN KEY REQUEST-----\n")
            f.write(str(hex(self.cipher_pub_key.x))[2:] + "\n")
            f.write(str(hex(self.cipher_pub_key.y))[2:] + "\n")
            f.write("-----END KEY REQUEST-----")
