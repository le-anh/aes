from datetime import datetime
from tinyec import registry
import secrets

curve = registry.get_curve('brainpoolP256r1')

def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]

def ecc_calc_encryption_keys(pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    sharedECCKey = pubKey * ciphertextPrivKey
    return (sharedECCKey, ciphertextPubKey)

def ecc_calc_decryption_key(privKey, ciphertextPubKey):
    sharedECCKey = ciphertextPubKey * privKey
    return sharedECCKey

for i in range(10):
    t0 = datetime.now()
    # privKey = secrets.randbelow(curve.field.n)
    privKey = 0x156ff3c7d9685bed1ad0988052cc0273acd8e0050f8a0fb6c228e9cb532ba4fe
    pubKey = privKey * curve.g


    (encryptKey, ciphertextPubKey) = ecc_calc_encryption_keys(pubKey)
    decryptKey = ecc_calc_decryption_key(privKey, ciphertextPubKey)
    t1 = datetime.now()
    print((t1-t0).total_seconds()*1000.0)
# print(f"Create keys time: {(t1-t0).total_seconds()*1000.0}")
# print("private key:", hex(privKey))
# print("public key:", compress_point(pubKey))

# print("ciphertext pubKey:", compress_point(ciphertextPubKey))
# print("encryption key:", compress_point(encryptKey))


# print("decryption key:", compress_point(decryptKey))