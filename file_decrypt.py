from Crypto.Cipher import AES
from base64 import b64decode
import json
from file_reader import FileReader
from file_writer import FileWriter

# File decrypter class
class FileDecrypter:

    decrypyted_bytes: bytes

    # Constructor
    def __init__(self):
        self.decrypyted_bytes = b''

    # Decrypt
    def Decrypt(self, file_in: str, password: str):
        # Read file
        file_data = FileReader.Read(file_in)
        # print((file_data))
        b64 = json.loads(file_data)
        print(b64['iv'])
        # iv = b64decode(b64['iv'])
        # ct = b64decode(b64['ciphertext'])
        # print(iv)
        # Decrypt it
        # decrypter = AES.new(password, AES.MODE_CBC, iv)
        # self.decrypyted_bytes = decrypter.decrypt(ct)

    # Save to file
    def SaveTo(self,
               file_out: str) -> None:
        FileWriter.Write(file_out, self.decrypyted_bytes())
