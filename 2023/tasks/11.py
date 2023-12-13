from dataclasses import dataclass
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Galaxy:
    x: int
    y: int


def parse_input(data: str, part: str) -> list[Galaxy]:
    space = list(map(lambda l: list(l), data.split('\n')))
    empty_row_spacing = 2 if part == 'a' else 1000000
    
    empty_row_indicies = []
    for y in range(len(space)):
        is_empty = True
        for x in range(len(space[y])):
            if space[y][x] != '.':
                is_empty = False
                break
            
        if is_empty:
            empty_row_indicies.append(y)
    
    empty_column_indicies = []     
    for x in range(len(space[0])):
        is_empty = True
        for y in range(len(space)):
            if space[y][x] != '.':
                is_empty = False
                break
            
        if is_empty:
            empty_column_indicies.append(x)
            
    galaxies: list[Galaxy] = []
    x_pos = 0
    y_pos = 0
    for y in range(len(space)):
        for x in range(len(space[y])):    
            if space[y][x] == '#':
                galaxies.append(Galaxy(x_pos, y_pos))
                
            x_pos += empty_row_spacing if x in empty_column_indicies else 1
            
        y_pos += empty_row_spacing if y in empty_row_indicies else 1
        x_pos = 0
     
    return galaxies


# //////////////////// PARTS /////////////////////////

def run_a(galaxies: list[Galaxy]):
    sum = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            sum += abs(galaxies[i].x - galaxies[j].x) + abs(galaxies[i].y - galaxies[j].y)

    print(sum)

def run_b(galaxies: list[Galaxy]):
    sum = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            sum += abs(galaxies[i].x - galaxies[j].x) + abs(galaxies[i].y - galaxies[j].y)

    print(sum)