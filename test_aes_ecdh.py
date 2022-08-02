import csv
from datetime import datetime
from lib.file_encrypter import FileEncrypter
from lib.file_decrypter import FileDecrypter
from lib.ecc import Point
from lib.ecdh import ECDH

key_priv_A = 99
key_priv_B = 109
key_pub_A = Point(0xe607de1ddba0768d63f41fb018ea203a9079cc1713eabd1865c4d89799be0a32, 0x784a0a40580c75923b8591562d5aec0ddd33b2596490d310c90d33d9147f6162)
key_pub_B = Point(0xa0b429e5d208fc92792874a326993ee60b65883e4d95cf0ac05c7e7da9798e47, 0x92d8149fcdf395ed4f41a665f384c4db218cfb085727c67fe77ee2ebe1d088a7)

def export_to_csv(data_row = ''):
    data_row = [datetime.now()] + data_row
    with open('result/result.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)

def file_encrypt(file_name):
    key_secret_encrypt = ECDH().get_key_secret(key_priv_A, key_pub_B)
    file_encrypter = FileEncrypter()
    file_encrypter.Encrypt("original/" + file_name + ".txt", key_secret_encrypt)
    file_encrypter.SaveTo("result/enc_" + file_name)
    enc_time = file_encrypter.GetEncryptedTime()
    print(f"Encrypt success (file {file_name}: {enc_time} ms)!")
    return enc_time

def file_decrypt(file_name):
    key_secret_decrypt = ECDH().get_key_secret(key_priv_B, key_pub_A)
    file_decrypter = FileDecrypter()
    file_decrypter.Decrypt("result/enc_" + file_name, key_secret_decrypt)
    file_decrypter.SaveTo("result/dec_" + file_name +".txt")
    dec_time = file_decrypter.GeDecryptedTime()
    print(f"Decrypt success (file {file_name}: {dec_time} ms)!")
    return dec_time

def file_enc_dec():
    for fn in range(8):
        for i in range(10):
            print(f"Iterating: {i+1}")
            data_row = [fn+1, i+1]
            file_name = str(fn+1)
            data_row.append(file_encrypt(file_name))
            data_row.append(file_decrypt(file_name))
            export_to_csv(data_row)

def run():
    file_enc_dec()

if __name__ == "__main__":
    run()