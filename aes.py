import re
from numpy import block

BLOCK_SIZE = 16     # 16 bytes ~= 128 bits
MAXTRIC_SIZE = 4    # 4x4 matrix
_key_matrices = []
_n_rounds = 10      # example 10 rounds for key lenght size 128 bits

def split_blocks(message, block_size=16, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+16] for i in range(0, len(message), block_size)]

def bytes_to_matrix(text):
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]  # Convert a 16 bytes array to a 4x4 matrix.

def add_round_key(state, key):
    for i in range(MAXTRIC_SIZE):
        for j in range(MAXTRIC_SIZE):
            state[i][j] ^= key[i][j]

def sub_bytes(plain_state):
    

def encrypt_block(plaintext):
    assert len(plaintext) == BLOCK_SIZE
    plain_state = bytes_to_matrix(plaintext)
    add_round_key(plain_state, _key_matrices[0])

    for i in range(1, _n_rounds):
        sub_bytes(plain_state)
        shift_rows(plain_state)
        mix_column(plain_state)
        add_round_key(plain_state), _key_matrices[i]

    # last round
    sub_bytes(plain_state)
    shift_rows(plain_state)
    add_round_key(plain_state, _key_matrices[-1])

def encrypt(plaintext, key):

    blocks = []
    for plaintext_block in split_blocks(plaintext):
        block = encrypt_block(plaintext_block, key)
        blocks.append(block)

    return blocks



def decrypt(ciphertext, key):

    plaintext = ''
    return plaintext