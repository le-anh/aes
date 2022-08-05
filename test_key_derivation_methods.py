from datetime import datetime
from base64 import b64encode
from Crypto.Protocol.KDF import PBKDF2, scrypt, bcrypt
from Crypto.Hash import SHA512, SHA256
from Crypto.Random import get_random_bytes
from memory_profiler import profile

password = b'my super secret'
itr = 1
# ========= PBKDF2 =========
@profile
def __pbdkf2():
    aver_time = 0
    for i in range(itr):
        salt = get_random_bytes(16)
        t0 = datetime.now()
        keys = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
        key1 = keys[:16]
        key2 = keys[16:]
        t1 = datetime.now()
        aver_time += (t1-t0).total_seconds()*1000.0
    print(f"Average time (PBKDF2): {aver_time/itr:.2f}")
    print(len(key1))
    print(len(key2))


# ========= scrypt =========
@profile
def __scrypt():
    aver_time = 0
    for i in range(itr):
        salt = get_random_bytes(16)
        t0 = datetime.now()
        key = scrypt(password, salt, 16, N=2**14, r=8, p=1)
        t1 = datetime.now()
        aver_time += (t1-t0).total_seconds()*1000.0
    print(f"Average time (scrypt): {aver_time/itr:.2f}")
    print(len(key))

# ========= bcrypt =========
@profile
def __bcrypt():
    aver_time = 0
    for i in range(itr):
        t0 = datetime.now()
        b64pwd = b64encode(SHA256.new(password).digest())
        bcrypt_hash = bcrypt(b64pwd, 12)
        t1 = datetime.now()
        aver_time += (t1-t0).total_seconds()*1000.0
    print(f"Average time (bcrypt): {aver_time/itr:.2f}")
    print(len(bcrypt_hash))


if __name__ == "__main__":
    __pbdkf2()
    __scrypt()
    __bcrypt()

""" Note (result):
    PBDK2:  0.0 MiB +   630.31 ms
    scrypt: 0.2 MiB +   048.28 ms
    bcrypt: 0.7 MiB +   197.24 ms
"""