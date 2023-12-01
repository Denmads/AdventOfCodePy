from DailyAssignment import DailyAssignment
from dataclasses import dataclass

class FabricSquares(DailyAssignment):
    def __init__(self):
        super().__init__(3)

    def run_part_a(self, input: str):
        claims = parse_input(input)
        fabric = Fabric(1000)
        [fabric.mark_rect(rect.x, rect.y, rect.w, rect.h) for rect in claims]

        overlapping_squares = fabric.count_square_greater_than(1)
        print(f"Number of squares with overlap '{overlapping_squares}'")

    def run_part_b(self, input: str):
        claims = parse_input(input)
        for i in range(len(claims)):
            free = True
            for j in range(len(claims)):
                if i == j: continue
                if claims[i].intersects(claims[j]):
                    free = False
                    break
            if free:
                print(f"ID of non overlapping rect is '{claims[i].id}'")
                return
        print("No non overlapping rects")

def parse_input(input):
    claims = map(lambda x: x.split(" "), input.split("\n"))
    rects = []
    for claim in claims:
        id = claim[0][1:]
        x = int(claim[2].split(",")[0])
        y = int(claim[2].split(",")[1][:-1])
        w = int(claim[3].split("x")[0])
        h = int(claim[3].split("x")[1])
        rects.append(Rect(id, x, y, w, h))
    return rects

@dataclass
class Rect:
    id: str
    x: int
    y: int
    w: int
    h: int

    def left(self):
        return self.x

    def right(self):
        return self.x + self.w

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.h

    def intersects(self, other):
        return not (other.left() > self.right()-1 or other.top() > self.bottom()-1 or other.right()-1 < self.left() or other.bottom()-1 < self.top())

class Fabric:
    def __init__(self, size):
        self.size = size
        self.rect = [[0] * size for _ in range(size)]

    def mark_rect(self, x, y, w, h):

        for x_pos in range(x, x+w):
            for y_pos in range(y, y+h):
                self.rect[x_pos][y_pos] += 1
    
    def count_square_greater_than(self, n):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.rect[i][j] > n:
                    count += 1
        return count