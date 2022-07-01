from os import stat
from numpy import block

BLOCK_SIZE = 16     # 16 bytes ~= 128 bits
MAXTRIC_SIZE = 4    # 4x4 matrix
KEY_SIZE = 128
WORD_SIZE = 32
_key_matrices = []
_n_rounds = 10      # example 10 rounds for key lenght size 128 bits


def expand_key(key):
    [_key_matrices[i:i+32] for i in range(0, KEY_SIZE, WORD_SIZE)]

def split_blocks(message, block_size=16, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+16] for i in range(0, len(message), block_size)]

def bytes_to_matrix(text):
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]  # Convert a 16 bytes array to a 4x4 matrix.

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
        add_round_key(plain_state), _key_matrices[i]

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