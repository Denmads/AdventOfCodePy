from utils.vector import Vector2i

# //////////////////// PARSING /////////////////////////

InstructionList = list[tuple[Vector2i, int]]

def parse_instruction(data: str) -> tuple[Vector2i, int]:
    tokens = data.split()

    amount = int(tokens[1])

    if tokens[0] == "U":
        return (Vector2i(0, -1), amount)
    elif tokens[0] == "R":
        return (Vector2i(1, 0), amount)
    if tokens[0] == "D":
        return (Vector2i(0, 1), amount)
    if tokens[0] == "L":
        return (Vector2i(-1, 0), amount)

def parse_input(data: str) -> InstructionList:
    lines = data.split("\n")
    return list(map(lambda l: parse_instruction(l), lines))


# //////////////////// PARTS /////////////////////////

class Rope:
    def __init__(self, n: int):
        self.knots = [Vector2i() for _ in range(n)]
        self.length = n

    def __getattr__(self, name: str) -> Vector2i:
        if name == "head":
            return self.knots[0]
        elif name == "tail":
            return self.knots[self.length - 1]
        else:
            raise AttributeError()

    def move_head(self, x: int, y: int):
        self.head += (x, y)

        for i in range(1, self.length):
            if self.should_knot_move(i):
                self.move_knot(i)

    def should_knot_move(self, i) -> bool:
        x_diff = abs(self.knots[i-1].x - self.knots[i].x)
        y_diff = abs(self.knots[i-1].y - self.knots[i].y)

        return x_diff > 1 or y_diff > 1

    def move_knot(self, i):
        x_diff = self.knots[i-1].x - self.knots[i].x
        y_diff = self.knots[i-1].y - self.knots[i].y

        self.knots[i].x += min(1, max(-1, x_diff))
        self.knots[i].y += min(1, max(-1, y_diff))

def run_a(data: InstructionList):
    rope = Rope(2)
    visited = set()

    for inst in data:
        for i in range(inst[1]):
            # print(f"{inst[0]} - {i+1}/{inst[1]}")
            # print(f"H: {rope.head} | T: {rope.tail}")
            rope.move_head(inst[0].x, inst[0].y)
            # print(f"H: {rope.head} | T: {rope.tail}")
            # print("---")
            visited.add((rope.tail.x, rope.tail.y))

    print(f"Number of visited cells: {len(visited)}")

def run_b(data: InstructionList):
    rope = Rope(10)
    visited = set()

    for inst in data:
        for i in range(inst[1]):
            rope.move_head(inst[0].x, inst[0].y)
            visited.add((rope.tail.x, rope.tail.y))

    print(f"Number of visited cells: {len(visited)}")