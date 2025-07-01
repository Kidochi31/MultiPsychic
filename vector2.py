from math import sqrt

class Fraction:
    def __init__(self, numerator: int, denominator: int):
        self.numerator = numerator
        self.denominator = denominator
    
    def __repr__(self) -> str:
        return f"Fraction({self.numerator}, {self.denominator})"

    def __str__(self) -> str:
        return f"({self.numerator}/{self.denominator})"
    
    def __mul__(self, other: int) -> int:
        return other * self.numerator // self.denominator
    


class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __mul__(self, other: int) -> 'Vector2':
        return Vector2(self.x * other, self.y * other)
    
    def __floordiv__(self, other: int) -> 'Vector2':
        return Vector2(self.x // other, self.y // other)

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __neg__(self) -> 'Vector2':
        return Vector2(-self.x, -self.y)
    
    def __pos__(self) -> 'Vector2':
        return Vector2(self.x, self.y)
    
    def magnitude(self) -> int:
        return int_sqrt(self.x * self.x + self.y * self.y)
    
    def sqr_magnitude(self) -> int:
        return self.x * self.x + self.y * self.y
    
    def distance_between(self, other: 'Vector2') -> int:
        return (self - other).magnitude()
    
    def sqr_distance_between(self, other: 'Vector2') -> int:
        return (self - other).sqr_magnitude() 
    
    def __iter__(self):
        yield self.x
        yield self.y

    def dot_product(self, other: 'Vector2') -> int:
        return self.x * other.x + self.y * other.y
    
    def in_direction_of(self, other: 'Vector2') -> 'Vector2':
        # v in direction of o is (v . o) / |o| * (o / |o|) = o . (v . o) / |o|^2
        return other * self.dot_product(other) // other.sqr_magnitude()
    
    def tan_times(self, other: int) -> int:
        # tan = o / a = y / x
        return other * self.y // self.x
    
    def cot_times(self, other: int) -> int:
        # cot = a / o = x / y
        return other * self.x // self.y

    def sin_times(self, other: int) -> int:
        # sin = o / h = y / sqrt(x^2 + y^2)
        return other * self.y // self.magnitude()
    
    def cos_times(self, other: int) -> int:
        # cos = a / h = x / sqrt(x^2 + y^2)
        return other * self.x // self.magnitude()

    def times_normal(self, other: int) -> 'Vector2':
        return (self * other) // self.magnitude()
    
    def rotate_counterclockwise(self) -> 'Vector2':
        return Vector2(-self.y, self.x)

    def rotate_clockwise(self) -> 'Vector2':
        return Vector2(self.y, -self.x)

def int_sqrt(a: int) -> int:
    if a < 0:
        raise Exception("cannot find square root of a negative number")
    if a == 0:
        return 0
    if a == 1:
        return 1
    
    estimate = a // 2
    prev_estimate = estimate
    while True:
        estimate = (estimate * estimate + a) // 2 // estimate
        if prev_estimate == estimate:
            break
        prev_estimate = estimate
    return estimate