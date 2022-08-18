import csv
from datetime import datetime
from lib.file_encrypter import FileEncrypter
from lib.file_decrypter import FileDecrypter
from lib.ecdh import ECDH

key_priv_A = 0x156ff3c7d9685bed1ad0988052cc0273acd8e0050f8a0fb6c228e9cb532ba4fe
key_pub_A = ECDH().get_key_public(key_priv_A)

def export_to_csv(data_row = ''):
    data_row = [datetime.now()] + data_row
    with open('result/result.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)

def file_encrypt(file_name):
    file_encrypter = FileEncrypter(key_pub_A)
    t0 = datetime.now()
    file_encrypter.Encrypt("original/" + file_name + ".txt")
    t1 = datetime.now()
    file_encrypter.SaveTo("result/enc_" + file_name)
    enc_time = (t1-t0).total_seconds()*1000.0
    return enc_time

def file_decrypt(file_name):
    file_decrypter = FileDecrypter(key_priv_A, "result/enc_" + file_name + ".key")
    t0 = datetime.now()
    file_decrypter.Decrypt("result/enc_" + file_name)
    t1 = datetime.now()
    file_decrypter.SaveTo("result/dec_" + file_name +".txt")
    dec_time = (t1-t0).total_seconds()*1000.0
    return dec_time

def file_enc_dec():
    for fn in range(20):
        file_name = str(fn+1)
        for i in range(10):
            print(f"File: {file_name} - Iterating: {i+1}")
            data_row = [fn+1, i+1]
            data_row.append(file_encrypt(file_name))
            data_row.append(file_decrypt(file_name))
            export_to_csv(data_row)

def run():
    print(f'Public key: {ECDH().point_to_bytes_key(key_pub_A)}')
    file_encrypt("text")
    print('==============================================================================================')
    file_decrypt("text")

if __name__ == "__main__":
    run()