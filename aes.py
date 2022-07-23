import math

BLOCK_SIZE = 16 # 16 bytes <==> 128 bits
ROUND_BY_KEY_SIZE = {16: 10, 24: 12, 32: 14}

s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

r_c = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)

def g_function(last_row_key, round):
    last_word = list(last_row_key[-1])
    last_word.append(last_word.pop(0))
    last_word = [s_box[int(b)] for b in last_word]  # S-Box
    last_word[0] ^= r_c[round]  # Adds a round coefficient RC
    last_row_key[0] = bytes(i^j for i, j, in zip(last_word,  last_row_key[0]))
    return last_row_key

def h_function(w):
    return [s_box[b] for b in w]

def key_schedule(key):
    assert len(key) in ROUND_BY_KEY_SIZE
    columns_key = len(key)//4
    num_words = (ROUND_BY_KEY_SIZE[len(key)] + 1) * 4
    round_key = math.ceil(num_words / columns_key)
    key_matrices = [key[i:i+columns_key] for i in range(0, len(key), 4)]    # round key 0
    for r in range(1, round_key):
        last_row_key = key_matrices[len(key_matrices) - columns_key:] # a last row key
        last_row_key = g_function(last_row_key, r)  # g function
        key_matrices.append(last_row_key[0])
        for w in range(1, columns_key):
            if r*columns_key + w < num_words:
                if w % 8 == 4 and len(key) == 256:
                    w_s_box = h_function(last_row_key[w-1]) # h function
                    last_row_key[w] = bytes(i^j for i, j, in zip(w_s_box,  last_row_key[w]))
                else:
                    last_row_key[w] = bytes(i^j for i, j, in zip(last_row_key[w-1],  last_row_key[w]))
                key_matrices.append(last_row_key[w])
            else:
                break
    return key_matrices

def byte_substitution(block):
    return [s_box[b] for b in block]

def inv_byte_substitution(block):
    return [inv_s_box[b] for b in block]

def shift_rows(block):
    block[1], block[5], block[9], block[13] = block[5], block[9], block[13], block[1]
    block[2], block[6], block[10], block[14] = block[10], block[14], block[2], block[6]
    block[3], block[7], block[11], block[15] = block[15], block[3], block[7], block[11]
    return block

def inv_shift_rows(block):
    block[1], block[5], block[9], block[13] = block[13], block[1], block[5], block[9]
    block[2], block[6], block[10], block[14] = block[10], block[14], block[2], block[6]
    block[3], block[7], block[11], block[15] = block[7], block[11], block[15], block[3]
    return block

xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_column(b):
    t0 = b[0] ^ b[1] ^ b[2] ^ b[3]
    b0 = b[0]
    b[0] ^= t0 ^ xtime(b[0] ^ b[1])
    b[1] ^= t0 ^ xtime(b[1] ^ b[2])
    b[2] ^= t0 ^ xtime(b[2] ^ b[3])
    b[3] ^= t0 ^ xtime(b[3] ^ b0)

    t1 = b[4] ^ b[5] ^ b[6] ^ b[7]
    b1 = b[4]
    b[4] ^= t1 ^ xtime(b[4] ^ b[5])
    b[5] ^= t1 ^ xtime(b[5] ^ b[6])
    b[6] ^= t1 ^ xtime(b[6] ^ b[7])
    b[7] ^= t1 ^ xtime(b[7] ^ b1)

    t2 = b[8] ^ b[9] ^ b[10] ^ b[11]
    b2 = b[8]
    b[8] ^= t2 ^ xtime(b[8] ^ b[9])
    b[9] ^= t2 ^ xtime(b[9] ^ b[10])
    b[10] ^= t2 ^ xtime(b[10] ^ b[11])
    b[11] ^= t2 ^ xtime(b[11] ^ b2)

    t3 = b[12] ^ b[13] ^ b[14] ^ b[15]
    b3 = b[12]
    b[12] ^= t3 ^ xtime(b[12] ^ b[13])
    b[13] ^= t3 ^ xtime(b[13] ^ b[14])
    b[14] ^= t3 ^ xtime(b[14] ^ b[15])
    b[15] ^= t3 ^ xtime(b[15] ^ b3)
    return b

def inv_mix_column(b):
    u0 = xtime(xtime(b[0] ^ b[2]))
    v0 = xtime(xtime(b[1] ^ b[3]))
    b[0] ^= u0
    b[1] ^= v0
    b[2] ^= u0
    b[3] ^= v0

    u1 = xtime(xtime(b[4] ^ b[6]))
    v1 = xtime(xtime(b[5] ^ b[7]))
    b[4] ^= u1
    b[5] ^= v1
    b[6] ^= u1
    b[7] ^= v1

    u2 = xtime(xtime(b[8] ^ b[10]))
    v2 = xtime(xtime(b[9] ^ b[11]))
    b[8] ^= u2
    b[9] ^= v2
    b[10] ^= u2
    b[11] ^= v2

    u3 = xtime(xtime(b[12] ^ b[14]))
    v3 = xtime(xtime(b[13] ^ b[15]))
    b[12] ^= u3
    b[13] ^= v3
    b[14] ^= u3
    b[15] ^= v3

    b = mix_column(b)
    return b

def add_key(block, key_matrices, round_count):
    for i in range(0, 16):
        block[i] ^= key_matrices[(i//4) + (round_count*4)][i%4]
    return block

def pad(plaintext):
    padding_len = 16 - (len(plaintext) % 16)
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding

def unpad(plaintext):
    padding_len = plaintext[-1]
    assert padding_len > 0
    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    assert all(p == padding_len for p in padding)
    return message

def split_block(byte_arr):
    return [byte_arr[i:i+BLOCK_SIZE] for i in range(0, len(byte_arr), BLOCK_SIZE)]

def valid_plaintext_original_key(plaintext, original_key):
    if isinstance(plaintext, str):
        plaintext = pad(bytes(plaintext.encode('utf-8')))
    if isinstance(plaintext, bytes):
        plaintext = pad(bytes(plaintext))
    if isinstance(plaintext, bytearray):
        plaintext = pad(bytes(plaintext))
    plaintext = [byte for byte in plaintext]
    if isinstance(original_key, str):
        original_key = [byte for byte in bytes(original_key, "utf-8")]
    return plaintext, original_key

def encrypt_block(block, key_matrices, NUM_ROUND):
    block = add_key(block, key_matrices, 0) # Add key
    for r in range(1, NUM_ROUND):
        block = byte_substitution(block)    # Byte Substitution
        block = shift_rows(block)   # Shift Rows
        block = mix_column(block)   # Mix Column
        block = add_key(block, key_matrices, r) # Add key
    # Last round
    block = byte_substitution(block)    # Byte Substitution
    block = shift_rows(block)   # Shift Rows
    block = add_key(block, key_matrices, NUM_ROUND) # Add key
    return block

def encrypt(plaintext, original_key):
    plaintext, original_key = valid_plaintext_original_key(plaintext, original_key)
    key_matrices = key_schedule(original_key)
    NUM_ROUND = ROUND_BY_KEY_SIZE[len(original_key)]
    cipher_text=[]
    for block in split_block(plaintext):
        block = encrypt_block(block, key_matrices, NUM_ROUND)
        cipher_text.append(block)
    cipher_text = [byte for block in cipher_text for byte in block]
    return cipher_text

def xor_bytes(block1, block2):
    return [b1^b2 for b1, b2 in zip(block1, block2)]

def valid_ciphertext_original_key(ciphertext, original_key):
    if isinstance(ciphertext, str):
        ciphertext = [byte for byte in bytes(ciphertext, "utf-8")]
    if isinstance(ciphertext, bytes):
        ciphertext = [byte for byte in ciphertext]
    if isinstance(original_key, str):
        original_key = [byte for byte in bytes(original_key, "utf-8")]
    return ciphertext, original_key

def decrypt_block(block, key_matrices, NUM_ROUND):
    # Inverse of last round:
    block = add_key(block, key_matrices, NUM_ROUND) # Add key
    block = inv_shift_rows(block)   # Inverse Shift Rows
    block = inv_byte_substitution(block)     # Inverse Byte Substitution
    for r in range(NUM_ROUND-1, 0, -1):
        block = add_key(block, key_matrices, r) # Add key
        block = inv_mix_column(block)   # Inverse Mix Column
        block = inv_shift_rows(block)   # Inverse Shift Rows
        block = inv_byte_substitution(block)    # Inverse Byte Substitution
    block = add_key(block, key_matrices, 0)
    return block

def decrypt(ciphertext, original_key):
    ciphertext, original_key = valid_ciphertext_original_key(ciphertext, original_key)
    key_matrices = key_schedule(original_key)
    NUM_ROUND = ROUND_BY_KEY_SIZE[len(original_key)]
    plain_text = []
    for block in split_block(ciphertext):
        block = decrypt_block(block, key_matrices, NUM_ROUND)
        plain_text.append(block)
    plain_text = unpad([byte for block in plain_text for byte in block])
    return plain_text