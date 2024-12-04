from typing import Any

from utils.parse_util import parse_lines

# //////////////////// PARSING & TYPES /////////////////////////

type WordSearchGrid = list[list[str]]

def parse_input(data: str, part: str) -> WordSearchGrid:
    
    grid = []
    
    for line in data.splitlines():
        grid.append(list(line))
    
    return grid


# //////////////////// PARTS /////////////////////////

def run_a(data: WordSearchGrid):
    xmas_count = 0
    
    for y in range(len(data)):
        for x in range(len(data[y])):
            
            if data[y][x] == "X":
                xmas_count += count_xmas_matches(data, x, y)
                
    print(f"Xmas was found {xmas_count} times")

def run_b(data: WordSearchGrid):
    xmas_count = 0
    
    for y in range(1, len(data)-1):
        for x in range(1, len(data[y])-1):
            
            if data[y][x] == "A" and is_x_mas_match(data, x, y):
                xmas_count += 1
                
    print(f"X-Mas was found {xmas_count} times")



def count_xmas_matches(data: WordSearchGrid, x: int, y: int) -> int:
    to_match = "MAS"
    
    matches = 0
    for j in range(-1, 2):
        for i in range(-1, 2):
            if i == 0 and j == 0:
                continue
            
            end_x = x + i * len(to_match)
            end_y = y + j * len(to_match)
            if end_x < 0 or end_x > len(data[y])-1 or end_y < 0 or end_y > len(data)-1:
                continue
            
            full_match = True
            for offset, char in enumerate(to_match):
                x_pos = x + i * (offset + 1)
                y_pos = y + j * (offset + 1)
                
                if data[y_pos][x_pos] != char:
                    full_match = False
                    break
                
            if full_match:
                matches += 1
                
    
    return matches


def is_x_mas_match(data: WordSearchGrid, x: int, y: int) -> bool:
    diagonal1 = [
        data[y-1][x-1], data[y+1][x+1]
    ]
    
    diagonal2 = [
        data[y-1][x+1], data[y+1][x-1]
    ]
    
    return diagonal1.count("M") == 1 and diagonal1.count("S") == 1 and diagonal2.count("M") == 1 and diagonal2.count("S") == 1