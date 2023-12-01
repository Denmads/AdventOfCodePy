from typing import Dict, List, Tuple, Type
from DailyAssignment import DailyAssignment
from dataclasses import dataclass, field

@dataclass
class Algorithm:
    transformations: Dict[List[str], str] = field(default_factory=dict)

    def init(self, input):
        for i in range(len(input)):
            res = input[i]
            binary = bin(i)[2:]
            binary = "0" * (9 - len(binary)) + binary
            pixels = binary.replace("1", "#").replace("0", ".")
            self.transformations[tuple(pixels)] = res
        
    def transform(self, input: List[str]):
        return self.transformations[tuple(input)]

class Image:
    #minx miny | maxx maxy

    def __init__(self, get_unbounded_point, prev_infinity=None):
        self.boundary = [0, 0, 0, 0]
        self.points = {}
        
        self.prev_infinity = "." if prev_infinity is None else get_unbounded_point(prev_infinity)
        self.get_unbounded_point = get_unbounded_point

    def add_point(self, x, y):
        if x < self.boundary[0]:
            self.boundary[0] = x
        elif x > self.boundary[2]:
            self.boundary[2] = x
        
        if y < self.boundary[1]:
            self.boundary[1] = y
        elif y > self.boundary[3]:
            self.boundary[3] = y

        self.points[(x, y)] = ""

    def get_point(self, x, y):
        if x < self.boundary[0] or x > self.boundary[2] or y < self.boundary[1] or y > self.boundary[3]:
            return self.prev_infinity
        return "#" if (x, y) in self.points else "."

    def apply_algorithm(self, algo: Algorithm) -> Type["Image"]:
        img = Image(self.get_unbounded_point, self.prev_infinity)
        for y in range(self.boundary[1]-1, self.boundary[3]+2):
            for x in range(self.boundary[0]-1, self.boundary[2]+2):
                pixels = [
                    self.get_point(x-1, y-1),
                    self.get_point(x, y-1),
                    self.get_point(x+1, y-1),
                    self.get_point(x-1, y),
                    self.get_point(x, y),
                    self.get_point(x+1, y),
                    self.get_point(x-1, y+1),
                    self.get_point(x, y+1),
                    self.get_point(x+1, y+1)
                ]
                res = algo.transform(pixels)
                if res == "#":
                    img.add_point(x, y)
        return img

    def print(self):
        for y in range(self.boundary[1], self.boundary[3]+1):
            line = ""
            for x in range(self.boundary[0], self.boundary[2]+1):
                line += "#" if (x, y) in self.points else "."
            print(line)
        print("----------------------------------------")

class ImageAlgorithm(DailyAssignment):
    def __init__(self):
        super().__init__(20)

    def run_part_a(self, input: str):
        algo, img = parse_algo_and_image(input)
        for i in range(2):
            img.print()
            img = img.apply_algorithm(algo)
        img.print()
        print(len(img.points.keys()))

    def run_part_b(self, input: str):
        algo, img = parse_algo_and_image(input)
        for i in range(50):
            img = img.apply_algorithm(algo)
        print(len(img.points.keys()))

def parse_algo_and_image(input):
    parts = input.split("\n\n")
    algo = Algorithm()
    algo.init(parts[0])

    def unbounded_point(prev):
        if parts[0][0] == ".":
            return "."
        elif parts[0][0] == "#" and parts[0][-1] == "#":
            return "#"
        else:
            return "." if prev == "#" else "#"

    img = Image(unbounded_point)
    lines = parts[1].split("\n")
    for j in range(len(lines)):
        for i in range(len(lines[j])):
            if lines[j][i] == "#":
                img.add_point(i, j)
    return (algo, img)