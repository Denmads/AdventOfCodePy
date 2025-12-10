from dataclasses import dataclass
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class PaperRoll:
    pass

def parse_input(data: str, part: str) -> list[list[PaperRoll | None]]:
    grid = []
    
    for line in data.split("\n"):
        row = []
        for cell in line:
            row.append(PaperRoll() if cell == "@" else None)

        grid.append(row)

    return grid


# //////////////////// PARTS /////////////////////////

def run_a(data: list[list[PaperRoll | None]]):
    count = 0

    for y in range(len(data)):
        for x in range(len(data[y])):

            if data[y][x] is None:
                continue

            neighbors = 0
            for i in range(-1, 2):
                for j in range(-1,2):
                    if i == 0 and j == 0:
                        continue

                    x_neigh = x+i
                    y_neigh = y+j
                    if x_neigh < 0 or x_neigh >= len(data[y]) or y_neigh < 0 or y_neigh >= len(data):
                        continue
                    
                    if data[y+j][x+i] is not None:
                        neighbors += 1
 
            if neighbors < 4:
                count += 1

    print(count)

    # for y in range(len(data)):
    #     for x in range(len(data[y])):
    #         print("@" if data[y][x] is not None else ".", end="")
    #     print()

def run_b(data: list[list[PaperRoll | None]]):
    removed = 0
    to_remove = find_removable_rolls(data)

    while len(to_remove) > 0:
        removed += len(to_remove)
        for x, y in to_remove:
            data[y][x] = None

        to_remove = find_removable_rolls(data)

    print(removed)

def find_removable_rolls(data: list[list[PaperRoll | None]]) -> list[tuple[int, int]]:
    to_remove = []

    for y in range(len(data)):
        for x in range(len(data[y])):

            if data[y][x] is None:
                continue

            neighbors = 0
            for i in range(-1, 2):
                for j in range(-1,2):
                    if i == 0 and j == 0:
                        continue

                    x_neigh = x+i
                    y_neigh = y+j
                    if x_neigh < 0 or x_neigh >= len(data[y]) or y_neigh < 0 or y_neigh >= len(data):
                        continue
                    
                    if data[y+j][x+i] is not None:
                        neighbors += 1
 
            if neighbors < 4:
                to_remove.append((x, y))

    return to_remove