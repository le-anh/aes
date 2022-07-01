B0 = 0x25
B1 = 0x25
B2 = 0x25
B3 = 0x25
a = 0x25
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

# print(bin(B1))
# print(bin((B1 << 1)))
# print(bin((B1 << 1) ^ 0x1B))
t = B0 ^ B1 ^ B2 ^ B3
b = B0 ^ (t ^ xtime(B0 ^ B1))
print(bin(B0))
print(hex(b))