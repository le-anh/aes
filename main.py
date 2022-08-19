from lib.file_encrypter import FileEncrypter
from lib.file_decrypter import FileDecrypter
from lib.ecdh import ECDH

priv_key = 0x156ff3c7d9685bed1ad0988052cc0273acd8e0050f8a0fb6c228e9cb532ba4fe
pub_key = ECDH().get_public_key(priv_key)

def file_encrypt(file_name: str)->None:
    file_encrypter = FileEncrypter(pub_key)
    file_encrypter.Encrypt("original/" + file_name + ".txt")
    file_encrypter.SaveTo("result/enc_" + file_name)

def file_decrypt(file_name: str)->None:
    file_decrypter = FileDecrypter(priv_key, "result/enc_" + file_name + ".key")
    file_decrypter.Decrypt("result/enc_" + file_name)
    file_decrypter.SaveTo("result/dec_" + file_name +".txt")

def run():
    print(f'Public key: {ECDH().point_to_bytes_key(pub_key)}')
    file_encrypt("text")
    print('==============================================================================================')
    file_decrypt("text")

if __name__ == "__main__":
    run()