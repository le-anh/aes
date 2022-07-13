from unittest import result


P = 17
A = 2
B = 2

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
def Invert(n):
    return pow(n, -1, P)

def Point_Double(Q):
    if Q.y:
        s = ((3*Q.x*Q.x + A) * Invert(2*Q.y)) % P
        x = (s*s - Q.x -Q.x) % P
        y = (s*(Q.x - x) - Q.y) % P
        return Point(x, y)
    return Point(0, 0)

def Point_Add(Q1, Q2):
    if Q2.x - Q1.x:
        s = ((Q2.y - Q1.y) * Invert(Q2.x - Q1.x)) % P
        x = (s*s - Q1.x - Q2.x) % P
        y = (s*(Q1.x - x) - Q1.y) % P
        return Point(x, y)
    return Point(0, 0)

def Point_Multiplication(d, Q):
    T = Q
    # while d:
    for i in bin(d)[2:]:
        T = Point_Double(T)
        print("Double: ", T.x, T.y)
        if(int(i)):
            T = Point_Add(T, Q)
            print("Add: ", T.x, T.y)
        d >>=1
    return T

p = Point(5, 1)
Q = Point(10, 6)

# result = Point_Multiplication(4, p)
result = Point_Double(Q)
print(result.x, result.y)

print(Invert(12))