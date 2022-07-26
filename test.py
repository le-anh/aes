from datetime import datetime
import csv
from tarfile import LENGTH_NAME
import aes as AES

SOURCE_PATH = "./source_test/"
DESTINATION_PATH = "./result/"
KEY = "Nogami Lab. 0123"

def create_file_example():
    file_size = 1024 * 1024
    for i in range(1, 6):
        # with open("./source_test/hoanganh.txt", "w") as out:
            # out.truncate(i*128 * 1024 * 1024)
        with open("./source_test/"+str(i)+".txt", "w") as out:
            for j in range(file_size):
                out.writelines("Nogami Lab. Okayama University.\n")
        file_size *= 2
        
def encrypt_file(file_name):
    file = open(SOURCE_PATH + file_name,"r")
    plaintext = file.read()
    file.close()
    t0 = datetime.now()
    result_encrypt = AES.encrypt(plaintext, KEY)
    t1 = datetime.now()
    file = open(DESTINATION_PATH + "encrypt_" + file_name,"wb")
    file.write(bytes(result_encrypt))
    file.close()
    return t1 - t0

def decrypt_file(file_name):
    file = open(DESTINATION_PATH + "encrypt_" + file_name,"rb")
    ciphertext = file.read()
    file.close()
    t2 = datetime.now()
    result_decrypt = AES.decrypt(ciphertext, KEY)
    t3 = datetime.now()
    file = open(DESTINATION_PATH + "decrypt_" + file_name,"w")
    file.write(''.join([chr(byte) for byte in result_decrypt]))
    file.close()
    return t3 - t2

def export_result_experiment(interval_encrypt, interval_decrypt, file_name):
    file = open(DESTINATION_PATH + "logs.txt","a")
    file.write(str(datetime.now()) + "\n")
    file.write(file_name + "\n")
    file.write("t1-t0: " + str(interval_encrypt) + "\n")
    file.write("t3-t2: " + str(interval_decrypt) + "\n\n")
    file.close()

def test_encrypt_file():
    for j in range(1):
        # data_row = [j]
        for i in range(1, 2):
            # file_name = str(i)+".txt"
            file_name = "text.txt"
            interval_encrypt = encrypt_file(file_name)
            interval_decrypt = decrypt_file(file_name)
            # data_row.append(interval_encrypt.total_seconds() * 1000.0)
            # data_row.append(interval_decrypt.total_seconds() * 1000.0)
            # print(j, i)
            print("Encryption time: ", interval_encrypt)
            print("Decryption time: ", interval_decrypt)
        # write_csv(data_row)
        
        print("Success (iteration: " + str(j + 1) + ")")
    print("Success.")

def write_csv(data_row = ''):
    data_row = [datetime.now()] + data_row
    with open(DESTINATION_PATH + 'result.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)

def run():
    test_encrypt_file()
    # create_file_example()

if __name__ == "__main__":
    run()