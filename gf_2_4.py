def add(x, y):
    return x^y

def sub(x, y):
    return x^y

def mpy(x, y):
    p = 0b11111         # module P(x) = x^4 + x^3 + x^2 + x + 1
    m = 0               # m will be product
    for i in range(4):
        m <<=  1
        if m & 0b10000:
            m ^= p
        if y & 0b01000:
            m ^= x
        y <<= 1
    return m

def div(x, y):
    return mpy(x, inv(y))

def inv(x):         # x^14 = 1/x
    p = mpy(x, x)   # p = x^2
    x = mpy(p, p)   # x = x^4
    p = mpy(p, x)   # p = x^(2+4)
    x = mpy(x, x)   # x = x^8
    p = mpy(p, x)   # p = x^(2+4+8)
    return p
def muitiplicationF_2_4_2(x):

# a = 0b1101
# b = 0b0110

# print(bin(inv(a)))
# print(bin(inv(b)))