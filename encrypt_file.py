from Crypto.Cipher import AES
from base64 import b64encode
import json
from file_reader import FileReader
from file_writer import FileWriter

class FileEncrypter:

    encrypted_bytes:bytes
    
    # Constructor
    def __init__(self):
        self.encrypted_bytes = b''

    # Encrypt
    def Encrypt(self, file_in: str, passwords: str):
        # Read file
        file_data = FileReader.Read(file_in)
        # Encrypt it
        cipher = AES.new(passwords.encode("utf-8"), AES.MODE_CBC)
        self.encrypted_bytes = cipher.encrypt(file_data)
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(self.encrypted_bytes).decode('utf-8')
        self.result = json.dumps({'iv':iv, 'ciphertext':ct})
        return self.result

    # Save to file
    def SaveTo(self, file_out: str):
        FileWriter.Write(file_out, self.encrypted_bytes)
