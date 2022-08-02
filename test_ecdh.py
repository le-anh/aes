
from datetime import datetime
from lib.ecdh import ECDH

key_priv_A = 99
key_priv_B = 109
ecdh = ECDH()
key_pub_A = ecdh.get_key_public(key_priv_A)
key_pub_B = ecdh.get_key_public(key_priv_B)
t0 = datetime.now()
key_secret_A = ecdh.get_key_secret(key_priv_A, key_pub_B)
key_secret_B = ecdh.get_key_secret(key_priv_B, key_pub_A)
t1 = datetime.now()

print(f"Create key time: {(t1-t0).total_seconds()}")
print(f"key_pub_A: [{hex(key_pub_A.x)}, {hex(key_pub_A.y)}]")
print(f"key_pub_B: [{hex(key_pub_B.x)}, {hex(key_pub_B.y)}]")
print("=============================================================================================================================================================================")
print(f"key_secret_A: {key_secret_A}")
print(f"key_secret_B: {key_secret_B}")

