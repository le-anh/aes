from os import stat
from attr import has
from numpy import block, byte

BLOCK_SIZE = 16     # 16 bytes ~= 128 bits
MAXTRIC_SIZE = 4    # 4x4 matrix
KEY_SIZE = 128
WORD_SIZE = 32
_key_matrices = []
_n_rounds = 10      # example 10 rounds for key lenght size 128 bits
rounds_by_key_size = {16: 10, 24: 12, 32: 14}

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

r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)

def expand_key(key):
    assert len(key) in rounds_by_key_size
    _n_rounds = rounds_by_key_size[len(key)]
    key_columns = bytes_to_matrix(key)
    iteration_size = len(key) // 4

    i = 1
    while len(key_columns) < (_n_rounds + 1) * 4:
        word = list(key_columns[-1])
        if len(key_columns) % iteration_size == 0:
            word.append(word.pop(0))
            word = [s_box[b] for b in word]
            word[0] ^= r_con[i]
            i += 1
        elif len(key) == 32 and len(key_columns) % iteration_size == 4:
            word = [s_box[b] for b in word]

        word = xor_bytes(word, key_columns[-iteration_size])
        key_columns.append(word)

    return [key_columns[4*i:4*(i+1)] for i in range(len(key_columns) // 4)]

def split_blocks(message, block_size=16, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+16] for i in range(0, len(message), block_size)]

def bytes_to_matrix(text):
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]  # Convert a 16 bytes array to a 4x4 matrix.

def xor_bytes(a, b):
    print(a)
    print(b)
    return bytes(i^j for i, j, in zip(a, b))

def add_round_key(state, key):
    for i in range(MAXTRIC_SIZE):
        for j in range(MAXTRIC_SIZE):
            state[i][j] ^= key[i][j]

def sub_bytes(state):
    for i in range(MAXTRIC_SIZE):
        for j in range(MAXTRIC_SIZE):
            state[i][j] = s_box[state[i][j]]

def shift_rows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]

# learned from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_single_column(column):
    col_t = column[0] ^ column[1] ^ column[2] ^ column[3]
    col_0 = column[0]
    column[0] ^= col_t ^ xtime(column[0] ^ column[1])
    column[1] ^= col_t ^ xtime(column[1] ^ column[2])
    column[2] ^= col_t ^ xtime(column[2] ^ column[3])
    column[3] ^= col_t ^ xtime(column[3] ^ col_0)

def mix_column(state):
    for i in range(MAXTRIC_SIZE):
        mix_single_column(state[i])

def encrypt_block(plaintext):
    assert len(plaintext) == BLOCK_SIZE
    plain_state = bytes_to_matrix(plaintext)
    add_round_key(plain_state, _key_matrices[0])

    for i in range(1, _n_rounds):
        sub_bytes(plain_state)
        shift_rows(plain_state)
        mix_column(plain_state)
        add_round_key(plain_state, _key_matrices[i])

    # last round
    sub_bytes(plain_state)
    shift_rows(plain_state)
    add_round_key(plain_state, _key_matrices[-1])

def encrypt(plaintext, key):

    blocks = []
    expand_key(key)
    for plaintext_block in split_blocks(plaintext):
        block = encrypt_block(plaintext_block)
        blocks.append(block)

    return blocks



def decrypt(ciphertext, key):

    plaintext = ''
    return plaintext

import random
hash = random.getrandbits(128)

k = b'a3fa6d97f4807e145b37451fc344e58c'
c = bytes(16)
# a = int(k, 16)

# key_expand = expand_key(k)
# print(key_expand)

for r in range(10, 0, -1):
    print(r)