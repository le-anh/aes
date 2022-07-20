import io
import PIL.Image as Image
import dhke as DHKE
import ecc as ECC
import aes as AES
import gf_2_8 as GF_2_8

def test_gf_2_8():
    x = 0b01010101
    y = 0b10101010
    y = 0b10101010
    print("x: ", bin(x))
    print("y: ", bin(y))
    print("x + y: ", bin(GF_2_8.add(x, y)))
    print("x - y: ", bin(GF_2_8.sub(x, y)))
    print("x * y: ", bin(GF_2_8.mpy(x, y)))
    print("x / y: ", bin(GF_2_8.div(x, y)))
    print("x^(-1): ", bin(GF_2_8.inv(x)))

def test_dhke():
    priv_key_A = 9
    priv_key_B = 8
    public_key_A = DHKE.get_public_key(priv_key_A)
    public_key_B = DHKE.get_public_key(priv_key_B)
    secret_key_A = DHKE.get_secret_key(public_key_B, priv_key_A)
    secret_key_B = DHKE.get_secret_key(public_key_A, priv_key_B)

    print("secret_key_A: ", secret_key_A)
    print("secret_key_B: ", secret_key_B)

def test_aes_dhke():
    plaintext = "Nogami Lab.  Okayama University."
    priv_key_A = 9
    priv_key_B = 8
    public_key_A = DHKE.get_public_key(priv_key_A)
    public_key_B = DHKE.get_public_key(priv_key_B)

    secret_key_A = DHKE.get_secret_key(public_key_B, priv_key_A)
    result_encypt = AES.encrypt(plaintext, secret_key_A)

    secret_key_B = DHKE.get_secret_key(public_key_A, priv_key_B)
    result_decypt = AES.decrypt(result_encypt, secret_key_B)

    print('Plain text: ', plaintext)
    print('Key: ', secret_key_A)
    print("-----------------------------------------------------\n")
    print('Encrypt: ', bytes(result_encypt))

    print("Decrypt: ", ''.join([chr(byte) for byte in result_decypt]))

# def test_aes_ecc_ke():
#     plaintext = "Nogami Lab.  Okayama University."
#     # key_priv_a = 1023
#     key_priv_b = 9081
#     # key_pub_a = ECC.get_public_key(key_priv_a)
#     key_pub_b = ECC.get_public_key(key_priv_b)
#     # key_secret_a = ECC.get_secret_key(key_priv_a, key_pub_b)
#     # result_encypt = AES.encrypt(plaintext, key_secret_a)
#     # key_secret_b = ECC.get_secret_key(key_priv_b, key_pub_a)
#     # result_decypt = AES.decrypt(result_encypt, key_secret_b)
    
#     # Encrypt by A
#     encrypt_ecc_key, ciphertext_pub_key = ECC.encryption_key(key_pub_b)
#     result_encypt = AES.encrypt(plaintext, encrypt_ecc_key)

#     # Decrypt by B
#     decrypt_ecc_key = ECC.decryption_key(key_priv_b, ciphertext_pub_key)
#     result_decypt = AES.decrypt(result_encypt, decrypt_ecc_key)
    
#     print("")
#     print('Plain text: ', plaintext)
#     print("-----------------------------------------------------")
#     print('Encrypt key: ', encrypt_ecc_key)
#     print('Encrypted: ', bytes(result_encypt))
#     print('Decrypt key: ', decrypt_ecc_key)
#     print("Decrypted: ", ''.join([chr(byte) for byte in result_decypt]))
#     print("")

def test_aes_ecc_ke():
    plaintext = "Nogami Lab.  Okayama University."
    key_priv_b = 9081
    key_pub_b = ECC.get_public_key(key_priv_b)
    
    # Encrypt by A
    encrypt_ecc_key, ciphertext_pub_key = ECC.encryption_key(key_pub_b)
    result_encypt = AES.encrypt(plaintext, encrypt_ecc_key)

    # Decrypt by B
    decrypt_ecc_key = ECC.decryption_key(key_priv_b, ciphertext_pub_key)
    result_decypt = AES.decrypt(result_encypt, decrypt_ecc_key)
    
    # Show results
    print("")
    print('Plain text: ', plaintext)
    print("-----------------------------------------------------")
    print('Encrypt key: ', encrypt_ecc_key)
    print('Encrypted: ', bytes(result_encypt))
    print('Decrypt key: ', decrypt_ecc_key)
    print("Decrypted: ", ''.join([chr(byte) for byte in result_decypt]))
    print("")

def test_file_text():
    original_key = "Nogami Lab. 0123"
    
    file = open("./test/text.txt","rb")
    plaintext = file.read()
    file.close()

    result_encrypt = AES.encrypt(plaintext, original_key)
    
    file = open("./result/text_encrypt_result.txt","wb")
    file.write(bytes(result_encrypt))
    file.close()

    file = open("./result/text_encrypt_result.txt","rb")
    ciphertext = file.read()
    file.close()

    result_decrypt = AES.decrypt(ciphertext, original_key)
    

    file = open("./result/text_decrypt_result.txt","w")
    file.write(''.join([chr(byte) for byte in result_decrypt]))
    file.close()

    print("Success.")

def readimage(path):
    with open(path, "rb") as f:
        return bytearray(f.read())

def test_file_image():
    original_key = "Nogami Lab. 0123"
    path = "./test/japan.jpg"
    plaintext = readimage(path)


    result_encrypt = AES.encrypt(plaintext, original_key)

    file = open("./result/image_encrypt_result.bin","wb")
    file.write(bytearray(result_encrypt))
    file.close()

    file = open("./result/image_encrypt_result.bin","rb")
    ciphertext = file.read()
    file.close()

    result_decrypt = AES.decrypt(ciphertext, original_key)
    
   
    dataBytesIO = io.BytesIO(bytearray(result_decrypt))
    image = Image.open(dataBytesIO)
    image.save("./result/image_decrypt_result.jpg")

    print("Success.")

def run():
    # test_gf_2_8()
    # test_dhke()
    # print("")
    # test_string()
    # print("")
    # test_file_image()
    # test_file_text()
    # test_aes_dhke()
    test_aes_ecc_ke()

if __name__ == "__main__":
    run()