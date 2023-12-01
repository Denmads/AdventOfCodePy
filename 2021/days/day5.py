from typing import Tuple
from DailyAssignment import DailyAssignment
from dataclasses import dataclass

@dataclass
class Line:
    start: Tuple[int, int]
    end: Tuple[int, int]

    def get_all_coords(self):
        dir_x = 0 if self.end[0] == self.start[0] else 1 if self.end[0] - self.start[0] > 0 else -1
        dir_y = 0 if self.end[1] == self.start[1] else 1 if self.end[1] - self.start[1] > 0 else -1

        points = []
        point = self.start
        while point != self.end:
            points.append(point)
            point = (point[0]+dir_x, point[1]+dir_y)
        points.append(point)
        return points

class HydrothermalVents(DailyAssignment):
    def __init__(self):
        super().__init__(5)

    def run_part_a(self, input: str):
        lines = parse_lines(input)
        lines = list(filter(lambda x: x.start[0] == x.end[0] or x.start[1] == x.end[1], lines))

        max = find_max(lines)
        grid = [[0] * (max[1]+1) for _ in range(max[0]+1)]

        for line in lines:
            for p in line.get_all_coords():
                grid[p[0]][p[1]] += 1


        cnt = 0
        for y in range(len(grid[0])):
            for x in range(len(grid)):
                if grid[x][y] > 1:
                    cnt += 1
        print(cnt) 
                

    def run_part_b(self, input: str):
        lines = parse_lines(input)

        max = find_max(lines)
        grid = [[0] * (max[1]+1) for _ in range(max[0]+1)]

        for line in lines:
            for p in line.get_all_coords():
                grid[p[0]][p[1]] += 1


        cnt = 0
        for y in range(len(grid[0])):
            for x in range(len(grid)):
                if grid[x][y] > 1:
                    cnt += 1
        print(cnt) 

def find_max(lines):
    xs = []
    ys = []
    for line in lines:
        xs.extend([line.start[0], line.end[0]])
        ys.extend([line.start[1], line.end[1]])
    return (
        max(xs),
        max(ys)
    )

def parse_lines(input):
    lines = []
    for l in input.split("\n"):
        parts = l.split(" -> ")
        start = tuple(map(lambda x: int(x), parts[0].split(",")))
        end = tuple(map(lambda x: int(x), parts[1].split(",")))
        lines.append(Line(start, end))
    return lines