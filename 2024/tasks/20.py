from enum import Enum
from typing import Any

from utils.vector import Vector2i

# //////////////////// PARSING & TYPES /////////////////////////

class TileType(Enum):
    OPEN = 1,
    WALL = 2

class Direction(Enum):
    NORTH = "^"
    SOUTH = "v"
    WEST = "<"
    EAST = ">"

def parse_input(data: str, part: str) -> tuple[dict[Vector2i, TileType], Vector2i, Vector2i, int, int]:
    maze: dict[Vector2i, TileType] = {}
    start_pos: Vector2i
    end_pos: Vector2i
    
    width = len(data.split("\n")[0])
    height = len(data.split("\n"))
    
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(list(line)):
            if char == "S":
                start_pos = Vector2i(x, y)
                maze[start_pos] = TileType.OPEN
            elif char == "E":
                end_pos = Vector2i(x, y)
                maze[end_pos] = TileType.OPEN
            elif char == "#":
                maze[Vector2i(x, y)] = TileType.WALL
            else:
                maze[Vector2i(x, y)] = TileType.OPEN
                
    return (maze, start_pos, end_pos, width, height)


# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[dict[Vector2i, TileType], Vector2i, Vector2i, int, int]):
    track, start, end, width, height = data
    
    path_numbers = find_path_numbers(track, start, end)
    min_save = 100
    num_shortcuts = find_shortcuts(track, path_numbers, 2, min_save)
    
    print(f"Num cheats >= {min_save}: {num_shortcuts}")
    

def run_b(data: tuple[dict[Vector2i, TileType], Vector2i, Vector2i, int, int]):
    track, start, end, width, height = data
    
    path_numbers = find_path_numbers(track, start, end)
    min_save = 100
    num_shortcuts = find_shortcuts(track, path_numbers, 20, min_save)
    
    print(f"Num cheats >= {min_save}: {num_shortcuts}")


def find_path_numbers(track: dict[Vector2i, TileType], start: Vector2i, end: Vector2i) -> dict[Vector2i, int]:
    numbers: dict[Vector2i, int] = {
        start: 0
    }
    
    previous = None
    current = start
    while current != end:
        for dir in [Vector2i(-1, 0),Vector2i(1, 0),Vector2i(0, -1),Vector2i(0, 1)]:
            new_pos = current + dir
            
            if track[new_pos] == TileType.OPEN and new_pos != previous:
                previous = current
                current = new_pos
                numbers[current] = numbers[previous] + 1
                break
            
    return numbers

def find_shortcuts(track: dict[Vector2i, TileType], numbers: dict[Vector2i, int], cheat_length: int, saves_at_least: int) -> int:
    shortcuts: set[tuple[int, int]] = set()
    reachable: set[Vector2i] = set()
    
    for y in range(-cheat_length, cheat_length+1):
        for x in range(-cheat_length, cheat_length+1):
            manhatten_dist = abs(x) + abs(y)
            if manhatten_dist <= cheat_length:
                reachable.add(Vector2i(x, y))
    
    
    for i, path_tile in enumerate(numbers.keys()):
        for dir in reachable:
            new_pos = path_tile + dir
            
            if new_pos in track and track[new_pos] == TileType.OPEN:
                from_number = numbers[path_tile]
                to_number = numbers[new_pos]
                
                manhatten_dist = abs(path_tile.x - new_pos.x) + abs(path_tile.y - new_pos.y)
                
                if (to_number - from_number - manhatten_dist) >= saves_at_least:         # -2 for shortcut execution time
                    shortcut = (min(from_number, to_number), max(from_number, to_number))
                    if shortcut not in shortcuts:
                        shortcuts.add(shortcut)

        if i % 100 == 0:
            print(f"Progress: {i}/{len(numbers)}")
            
    return len(shortcuts)