from .ecc import Point
from .ecdh import ECDH
from .file_reader import FileReader
from .file_writer import FileWriter
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class FileEncrypter:
    encrypted_data: bytes
    iv: bytes
    encrypt_key: bytes
    ciphertext_pub_key: Point

    def __init__(self, key_public: int = None) -> None:
        self.data_encrypted = b""
        self.iv = b""
        if key_public:
            encrypt_key, self.ciphertext_pub_key = ECDH().get_encryption_key(key_public)
            self.encrypt_key = ECDH().point_to_bytes_key(encrypt_key)
            print(f"Cyphertext public key: {ECDH().point_to_bytes_key(self.ciphertext_pub_key)}")
            print(f"Encrypt key: {self.encrypt_key}")
    
    def Encrypt(self, file_in: str) -> None:
        file_data = FileReader.Read("original/" + file_in)   # Read file
        encrypter = AES.new(self.encrypt_key, AES.MODE_CBC)    # Encrypt it
        self.encrypted_data = encrypter.encrypt(pad(file_data, AES.block_size))
        self.iv = encrypter.iv
        print("File data was encrypted.")
    
    def GetEncryptedData(self) -> bytes:
        return self.encrypted_data

    def GetIV(self) -> bytes:
        return self.iv
    
    def SaveTo(self, file_out: str) -> None:
        FileWriter.Write("result/enc_" + file_out, b''.join([self.encrypted_data, self.iv]), 'wb')
        self.__Save_Key_File(file_out)
        print("Encrypted data was stored.")

    def __Save_Key_File(self, file_name: str) -> None:
        with open("result/key/" + file_name[:-3] + "key", 'w') as f:
            f.write("-----BEGIN KEY REQUEST-----\n")
            f.write(str(hex(self.ciphertext_pub_key.x))[2:] + "\n")
            f.write(str(hex(self.ciphertext_pub_key.y))[2:] + "\n")
            f.write("-----END KEY REQUEST-----")
