from lib.file_encrypter import FileEncrypter
from lib.file_decrypter import FileDecrypter
from lib.ecdh import ECDH

priv_key = 0x156ff3c7d9685bed1ad0988052cc0273acd8e0050f8a0fb6c228e9cb532ba4fe
pub_key = ECDH().get_public_key(priv_key)

def file_encrypt(file_name: str) -> None:
    file_encrypter = FileEncrypter(pub_key)
    file_encrypter.encrypt(file_name + ".txt")
    file_encrypter.save_to(file_name + ".bin")

def file_decrypt(file_name: str) -> None:
    file_decrypter = FileDecrypter(priv_key, file_name)
    file_decrypter.decrypt(file_name + ".bin")
    file_decrypter.save_to(file_name + ".txt")

def run():
    print(f'Public key: {ECDH().point_to_bytes_key(pub_key)}')
    file_encrypt("text")
    print(120*'=')
    file_decrypt("text")

if __name__ == "__main__":
    run()