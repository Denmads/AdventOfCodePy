from dataclasses import dataclass, field


@dataclass
class Vector2i:
    x: int = field(default=0)
    y: int = field(default=0)

    def __mul__(self, other):
        if type(other) == int:
            return Vector2i(self.x * other + self.y * other)

    def __iadd__(self, other):
        if type(other) == tuple and len(other) == 2:
            self.x += other[0]
            self.y += other[1]
        elif type(other) == Vector2i:
            self.x += other.x
            self.y += other.y
        return self

    def __str__(self):
        return f"({self.x}, {self.y})"