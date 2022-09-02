from lib.file_encrypter import FileEncrypter
from lib.file_decrypter import FileDecrypter
from lib.ecdh import ECDH

send_priv_key = 0x156ff3c7d9685bed1ad0988052cc0273acd8e0050f8a0fb6c228e9cb532ba4fe
send_pub_key = ECDH().get_public_key(send_priv_key)

receive_priv_key = 0x156ff3c9d9685bed1ad0988052cc0273acd8e0050f8a0fb6c228e9cb532ba4fe
receive_pub_key = ECDH().get_public_key(receive_priv_key)

def file_encrypt(file_name: str) -> None:
    file_encrypter = FileEncrypter(receive_pub_key)
    file_encrypter.encrypt(file_name + ".txt")
    file_encrypter.save_to(file_name + ".bin", send_priv_key, receive_pub_key)

def file_decrypt(file_name: str) -> None:
    file_decrypter = FileDecrypter(receive_priv_key, file_name)
    file_decrypter.decrypt(file_name + ".bin", receive_priv_key, send_pub_key)
    file_decrypter.save_to(file_name + ".txt")

def run():
    file_encrypt("text")
    print(120*'=')
    file_decrypt("text")

if __name__ == "__main__":
    run()