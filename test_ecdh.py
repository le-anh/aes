
from datetime import datetime
from lib.ecdh import ECDH
from lib.ecc import EccConst

key_priv_A = 0x156ff3c7d9685bed1ad0988052cc0273acd8e0050f8a0fb6c228e9cb532ba4fe
key_priv_B = 109

ecdh = ECDH()
t0 = datetime.now()
key_pub_A = ecdh.get_key_public(key_priv_A)
# key_pub_B = ecdh.get_key_public(key_priv_B)
# key_secret_A = ecdh.get_key_secret(key_priv_A, key_pub_B)
# key_secret_B = ecdh.get_key_secret(key_priv_B, key_pub_A)

key_encrypt, ciphertext_pub_key = ecdh.get_encryption_key(key_pub_A)
key_decrypt = ecdh.get_decryption_key(key_priv_A, ciphertext_pub_key)
t1 = datetime.now()

print((t1-t0).total_seconds()*1000.0)
# print(f"key_priv_A: {hex(key_priv_A)}")
# print(f"key_pub_A: ({len(hex(key_pub_A.x))}, {len(hex(key_pub_A.y))})")
print(f"ciphertext_pub_key: ({len(hex(ciphertext_pub_key.x))}, {len(hex(ciphertext_pub_key.y))})")
# print("=============================================================================================================================================================================")
# print(f"key_encryption: {ecdh.compress_point(key_encrypt)}")
# print(f"key_decryption: {ecdh.compress_point(key_decrypt)}")

