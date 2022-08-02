class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class EccConst:
    P = 115792089237316195423570985008687907853269984665640564039457584007908834671663  # P = 2^256 - 2^32 - 977
    A = 1
    B = int
    G = Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

class ECC:
    P = 115792089237316195423570985008687907853269984665640564039457584007908834671663  # P = 2^256 - 2^32 - 977
    A = 1
    B = int
    G = Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

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
    
    # def get_key_public(self, key_priv: int)->Point:
    #     key_public = self.__Point_Multiplication(key_priv, self.G)
    #     return key_public
    
    # def get_key_secret(self, key_priv:int, key_pub: Point)->Point:
    #     key_secret = self.__Point_Multiplication(key_priv, key_pub)
    #     return key_secret