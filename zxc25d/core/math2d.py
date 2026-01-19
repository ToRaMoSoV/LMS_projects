import math


class Vec2:
    __slots__ = ("x", "y")

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def copy(self):
        return Vec2(self.x, self.y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, value: float):
        return Vec2(self.x * value, self.y * value)

    def __rmul__(self, value: float):
        return self.__mul__(value)

    def __truediv__(self, value: float):
        return Vec2(self.x / value, self.y / value)

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def length_sq(self) -> float:
        return self.x * self.x + self.y * self.y

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vec2(0.0, 0.0)
        return Vec2(self.x / l, self.y / l)

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other) -> float:
        return self.x * other.y - self.y * other.x

    def rotate(self, angle: float):
        c = math.cos(angle)
        s = math.sin(angle)
        return Vec2(
            self.x * c - self.y * s,
            self.x * s + self.y * c
        )

    def distance_to(self, other) -> float:
        return (self - other).length()

    def tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Vec2({self.x:.3f}, {self.y:.3f})"
    
