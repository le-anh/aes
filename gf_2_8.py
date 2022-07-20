def add(x, y):
    return x^y

def sub(x, y):
    return x^y

def mpy(x, y):
    p = 0b100011011     # module P(x) = x^8 + x^4 + x^3 + x + 1
    m = 0               # m will be product
    for i in range(8):
        m <<=  1
        if m & 0b100000000:
            m ^= p
        if y & 0b010000000:
            m ^= x
        y <<= 1
    return m

def div(x, y):
    return mpy(x, inv(y))

def inv(x):         # x^254 = 1/x
    p = mpy(x, x)   # p = x^2
    x = mpy(p, p)   # x = x^4
    p = mpy(p, x)   # p = x^(2+4)
    x = mpy(x, x)   # x = x^8
    p = mpy(p, x)   # p = x^(2+4+8)
    x = mpy(x, x)   # x = x^16
    p = mpy(p, x)   # p = x^(2+4+8+16)
    x = mpy(x, x)   # x = x^32
    p = mpy(p, x)   # p = x^(2+4+8+16+32)
    x = mpy(x, x)   # x = x^64
    p = mpy(p, x)   # p = x^(2+4+8+16+32+64)
    x = mpy(x, x)   # x = x^128
    p = mpy(p, x)   # p = x^(2+4+8+16+32+64+128)
    return p

# a = 0b11010110

# print(bin(inv(a)))