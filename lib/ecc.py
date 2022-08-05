class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
# https://www.ietf.org/rfc/rfc5639.txt ==> 3.4.  Domain Parameters for 256-Bit Curves
class EccConst:
    P = 0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377
    A = 0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9
    B = 0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6
    G = Point(0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262, 0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997)
    N = 0xA9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7

#Secp256k1
# class EccConst:
#     P = 115792089237316195423570985008687907853269984665640564039457584007908834671663  # P = 2^256 - 2^32 - 977
#     A = 1
#     B = 7
#     G = Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
#     N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

class ECC:
    P = EccConst.P
    A = EccConst.A
    B = EccConst.B
    G = EccConst.G
    N = EccConst.N

    def __init__(self) -> None:
        self.P = EccConst.P
        self.A = EccConst.A
        self.B = EccConst.B
        self.G = EccConst.G
        self.N = EccConst.N

    def gcd(a, b):
        while b > 0:
            r = a % b
            a = b
            b = r
        return a

    def __invert(self, n, P):
        if n < 0: n = P + n
        a1, a2, a3 = 1, 0, P
        b1, b2, b3 = 0, 1, n
        while True:
            if b3 == 0:
                return "no inverse"
            if b3 == 1:
                return b2 if b2 >= 0 else P+b2
            q = a3//b3
            t1, t2, t3 = a1 - q * b1, a2 - q * b2, a3 - q * b3
            a1, a2, a3 = b1, b2, b3
            b1, b2, b3 = t1, t2, t3

    def __Point_Double(self, Q):
        if Q.y:
            s = ((3*Q.x*Q.x + self.A) * self.__invert(2*Q.y, self.P)) % self.P
            x = (s*s - Q.x -Q.x) % self.P
            y = (s*(Q.x - x) - Q.y) % self.P
            return Point(x, y)
        return Point(0, 0)

    def __Point_Add(self, Q1, Q2):
        if Q2.x - Q1.x:
            s = ((Q2.y - Q1.y) * self.__invert(Q2.x - Q1.x, self.P)) % self.P
            x = (s*s - Q1.x - Q2.x) % self.P
            y = (s*(Q1.x - x) - Q1.y) % self.P
            return Point(x, y)
        return Point(0, 0)

    def Point_Multiplication(self, d, Q=None):
        if not Q: Q = self.G
        T = Point(Q.x, Q.y)
        for i in bin(d)[3:]:
            T = self.__Point_Double(T)
            if(int(i)):
                T = self.__Point_Add(T, Q)
        return T