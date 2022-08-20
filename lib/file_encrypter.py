from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from .const import AesConst, Point
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class FileEncrypter:
    encrypted_data: bytes
    iv: bytes
    encrypt_key: bytes
    cipher_pub_key: Point

    def __init__(self, pub_key: int = None) -> None:
        self.encrypted_data = b""
        self.iv = b""
        if pub_key:
            encrypt_key, self.cipher_pub_key = ECDH().get_encryption_key(pub_key)
            self.encrypt_key = ECDH().point_to_bytes_key(encrypt_key)
            print(f"Cyphertext public key: {ECDH().point_to_bytes_key(self.cipher_pub_key)}")
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
    
    def save_to(self, file_out: str) -> None:
        FileWriter.write("result/enc_" + file_out, b''.join([self.get_encrypted_data(), self.get_iv()]), 'wb')
        self.save_file_key(file_out)
        print("Encrypted data was stored.")

    def save_file_key(self, file_name: str) -> None:
        with open("result/key/" + file_name[:-3] + "key", 'w') as f:
            f.write("-----BEGIN KEY REQUEST-----\n")
            f.write(str(hex(self.cipher_pub_key.x))[2:] + "\n")
            f.write(str(hex(self.cipher_pub_key.y))[2:] + "\n")
            f.write("-----END KEY REQUEST-----")
