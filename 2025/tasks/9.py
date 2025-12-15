from dataclasses import dataclass
import math
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Point:
    x: int
    y: int

def parse_input(data: str, part: str) -> list[Point]:
    points = []
    for line in data.splitlines("\n"):
        x, y = line.split(",")
        points.append(Point(int(x), int(y)))

    return points

# //////////////////// PARTS /////////////////////////

def run_a(data: list[Point]):
    largest_area = 0

    for c1_idx in range(len(data)):
        for c2_idx in range(c1_idx + 1, len(data)):
            if c1_idx == c2_idx:
                continue
                
            c1 = data[c1_idx]
            c2 = data[c2_idx]

            dx = abs(c1.x - c2.x) + 1 
            dy = abs(c1.y - c2.y) + 1

            area = dx * dy
            if area > largest_area:
                largest_area = area
                corner_1 = c1
                corner_2 = c2


    print(f"Area: {largest_area}")

def run_b(data: list[Point]):
    pass