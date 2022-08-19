from .parameter_initial import EccConst, Point

class ECC:
    def __init__(self) -> None:
        pass

    def gcd(self, a: int, b: int) -> int:
        while b > 0:
            r = a % b
            a = b
            b = r
        return a

    def __invert(self, n: int, P: int) -> int:
        if n < 0: n = P + n
        a1, a2, a3 = 1, 0, P
        b1, b2, b3 = 0, 1, n
        while True:
            if b3 == 0:
                return "no inverse"
            if b3 == 1:
                return b2 if b2 >= 0 else P + b2
            q = a3//b3
            t1, t2, t3 = a1 - q * b1, a2 - q * b2, a3 - q * b3
            a1, a2, a3 = b1, b2, b3
            b1, b2, b3 = t1, t2, t3

    def __Point_Double(self, Q: Point) -> Point:
        if Q.y:
            s = ((3*Q.x*Q.x + EccConst.A) * self.__invert(2*Q.y, EccConst.P)) % EccConst.P
            x = (s*s - Q.x -Q.x) % EccConst.P
            y = (s*(Q.x - x) - Q.y) % EccConst.P
            return Point(x, y)
        return Point(0, 0)

    def __Point_Add(self, Q1: Point, Q2: Point) -> Point:
        if Q2.x - Q1.x:
            s = ((Q2.y - Q1.y) * self.__invert(Q2.x - Q1.x, EccConst.P)) % EccConst.P
            x = (s*s - Q1.x - Q2.x) % EccConst.P
            y = (s*(Q1.x - x) - Q1.y) % EccConst.P
            return Point(x, y)
        return Point(0, 0)

    def Point_Multiplication(self, d: int, Q: Point = None) -> Point:
        if not Q: Q = EccConst.G
        T = Point(Q.x, Q.y)
        for i in bin(d)[3:]:
            T = self.__Point_Double(T)
            if(int(i)):
                T = self.__Point_Add(T, Q)
        return T