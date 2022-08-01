import csv
from datetime import datetime
from .lib.file_encrypter import FileEncrypter
from .lib.file_encrypter import FileDecrypter

password = "Security Lab."

def export_to_csv(data_row = ''):
    data_row = [datetime.now()] + data_row
    with open('result/result.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)

def file_encrypt(file_name):
    file_encrypter = FileEncrypter()
    t0 = datetime.now()
    file_encrypter.Encrypt("original/" + file_name + ".txt", password)
    t1 = datetime.now()
    file_encrypter.SaveTo("result/enc_" + file_name)
    enc_time = (t1-t0).total_seconds()*1000.0
    print(f"Encrypt success (file {file_name}: {enc_time} ms)!")
    return enc_time

def file_decrypt(file_name):
    file_decrypter = FileDecrypter()
    t0 = datetime.now()
    file_decrypter.Decrypt("result/enc_" + file_name, password)
    t1 = datetime.now()
    file_decrypter.SaveTo("result/dec_" + file_name +".txt")
    dec_time = (t1-t0).total_seconds()*1000.0
    print(f"Decrypt success (file {file_name}: {dec_time} ms)!")
    return dec_time

def file_enc_dec():
    for fn in range(8):
        print(f"Iterating: {fn+1}")
        file_name = str(fn+1)
        for i in range(10):
            data_row = [file_name, i+1]
            data_row.append(file_encrypt(file_name))
            data_row.append(file_decrypt(file_name))
            # export_to_csv(data_row)


file_enc_dec()