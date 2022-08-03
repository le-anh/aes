import csv
from datetime import datetime
from lib.file_encrypter import FileEncrypter
from lib.file_decrypter import FileDecrypter
from lib.ecc import Point

key_priv_A = 0x156ff3c7d9685bed1ad0988052cc0273acd8e0050f8a0fb6c228e9cb532ba4fe
key_pub_A = Point(0x93dc12bd0ae2db5790795852eeeefeb6bcea2f38d3013314c17d72b1d7257f6d, 0xf9125b136ff2b3b85d96ab6ea42f59d2ba7b7a6805d538b49eae1520b32d04f)

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
    print(f"Encrypt success (file {file_name}): {enc_time} ms!")
    return enc_time

def file_decrypt(file_name):
    file_decrypter = FileDecrypter(key_priv_A)
    t0 = datetime.now()
    file_decrypter.Decrypt("result/enc_" + file_name)
    t1 = datetime.now()
    file_decrypter.SaveTo("result/dec_" + file_name +".txt")
    dec_time = (t1-t0).total_seconds()*1000.0
    print(f"Decrypt success (file {file_name}) {dec_time} ms!")
    return dec_time

def file_enc_dec():
    for fn in range(1):
        for i in range(1):
            data_row = [fn+1, i+1]
            file_name = str(fn+1)
            print(f"File: {file_name} - Iterating: {i+1}")
            data_row.append(file_encrypt(file_name))
            data_row.append(file_decrypt(file_name))
            # export_to_csv(data_row)

def run():
    file_encrypt("text")
    file_decrypt("text")

if __name__ == "__main__":
    run()