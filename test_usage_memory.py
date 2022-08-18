import csv
from datetime import datetime
from lib.file_encrypter import FileEncrypter
from lib.file_decrypter import FileDecrypter

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
        file_name = str(fn+1)
        for i in range(10):
            print(f"File {fn +1} - Iterating: {i+1}")
            file_encrypt(file_name)
            file_decrypt(file_name)

def run():
    file_enc_dec()

if __name__ == "__main__":
    run()