from dataclasses import dataclass
from enum import Enum
from typing import Any

from utils.vector import Vector2i

# //////////////////// PARSING & TYPES /////////////////////////

class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    
@dataclass
class Box:
    left_part: Vector2i
    right_part: Vector2i
    
    def __hash__(self):
        return hash(self.left_part) + hash(self.right_part)
    
class Wall:
    pass

def parse_input(data: str, part: str) -> tuple[dict[Vector2i, str], list[Direction], Vector2i, int, int]:
    layout, moves = data.split("\n\n")
    
    warehouse, robot_pos, width, height = parse_layout(layout)
    
    return (
        warehouse,
        parse_moves(moves),
        robot_pos,
        width, height
    )
    
def parse_layout(layout: str) -> tuple[dict[Vector2i, str], Vector2i, int, int]:
    layout_dict: dict[Vector2i, str] = {}
    robot_position: Vector2i
    
    width = len(layout.split("\n")[0])
    height = len(layout.split("\n"))
    
    for y, line in enumerate(layout.split("\n")):
        for x, char in enumerate(list(line)):
            if char == "@":
                robot_position = Vector2i(x, y)
            elif char != ".":
                layout_dict[Vector2i(x, y)] = char
                
    return (layout_dict, robot_position, width, height)

def parse_moves(moves: str) -> list[Direction]:
    move_list: list[Direction] = []
    for line in moves.split("\n"):
        for char in list(line):
            move_list.append(Direction(char))
            
    return move_list


# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[dict[Vector2i, str], list[Direction], Vector2i, int, int]):
    # Execute moves
    warehouse, moves, robot_pos, width, height = data
    
    for move in moves:
        dir = get_dir_vector(move)
        
        tile_to_check = Vector2i(robot_pos.x + dir.x, robot_pos.y + dir.y)
        boxes_to_move = []
        while tile_to_check in warehouse and warehouse[tile_to_check] == "O":
            boxes_to_move.append(tile_to_check.copy())
            tile_to_check += dir
            
        if tile_to_check not in warehouse:
            # Robot can move
            robot_pos += dir
            for box in boxes_to_move:
                del warehouse[box]
            for box in boxes_to_move:
                box += dir
                warehouse[box] = "O"
                
        # for y in range(height):
        #     for x in range(width):
        #         pos = Vector2i(x, y)
                
        #         if pos == robot_pos:
        #             print("@", end="")
        #         elif pos in warehouse:
        #             print(warehouse[pos], end="")
        #         else:
        #             print(".", end="")
                    
        #     print()
            
        # print()
        # print()
    
    total = 0
    
    for key, val in warehouse.items():
        if val == "O":
            total += key.y * 100 + key.x
            
    print(f"Total GPS Score: {total}")
    

def run_b(data: tuple[dict[Vector2i, str], list[Direction], Vector2i, int, int]):
    wh, moves, rp, w, h = data
    warehouse, robot_pos, width, height = make_warehouse_wide(wh, rp, w, h)

    for move in moves:
        dir = get_dir_vector(move)
        
        tiles_to_check = [Vector2i(robot_pos.x, robot_pos.y)]
        hit_wall = False
        boxes_to_move = set()
        while len(tiles_to_check) > 0 and not hit_wall:
            new_tiles = set()
            for tile in tiles_to_check:
                new_pos = tile.copy()
                new_pos += dir
                
                if new_pos in warehouse and type(warehouse[new_pos]) is Wall:
                    hit_wall = True
                    continue
                elif new_pos in warehouse and type(warehouse[new_pos]) is Box:
                    box = warehouse[new_pos]
                    boxes_to_move.add(box)
                    
                    if move == Direction.UP or move == Direction.DOWN:
                        new_tiles.add(box.left_part)
                        new_tiles.add(box.right_part)
                    else:
                        new_tiles.add(new_pos)
                    
            tiles_to_check = list(new_tiles)
        
        if not hit_wall:
            # can move
            robot_pos += dir
            
            for box in boxes_to_move:
                del warehouse[box.left_part]
                del warehouse[box.right_part]
                
            for box in boxes_to_move:
                box.left_part += dir
                warehouse[box.left_part] = box
                box.right_part += dir
                warehouse[box.right_part] = box
                
        # print(f"Move: {move.value}")  
        # for y in range(height):
        #     for x in range(width):
        #         pos = Vector2i(x, y)
                
        #         if pos == robot_pos:
        #             print("@", end="")
        #         elif pos in warehouse:
        #             if type(warehouse[pos]) is Wall:
        #                 print("#", end="")
        #             elif type(warehouse[pos]) is Box:
        #                 box: Box = warehouse[pos]
        #                 if pos == box.left_part:
        #                     print("[", end="")
        #                 elif pos == box.right_part:
        #                     print("]", end="")
        #         else:
        #             print(".", end="")
                    
        #     print()
            
        # print()
        # print()
        
        
    total = 0
    
    for val in set(warehouse.values()):
        if type(val) is Box:
            total += val.left_part.y * 100 + val.left_part.x
            
    print(f"Total GPS Score: {total}")
            

def get_dir_vector(dir: Direction) -> Vector2i:
    match dir:
        case Direction.UP:
            return Vector2i(0, -1)
        case Direction.DOWN:
            return Vector2i(0, 1)
        case Direction.LEFT:
            return Vector2i(-1, 0)
        case Direction.RIGHT:
            return Vector2i(1, 0)
        
def make_warehouse_wide(layout: dict[Vector2i, str], robot: Vector2i, w: int, h: int) -> tuple[dict[Vector2i, object], Vector2i, int, int]:
    new_layout = {}
    
    for key, val in layout.items():
        if val == "#":
            new_layout[Vector2i(key.x * 2, key.y)] = Wall()
            new_layout[Vector2i(key.x * 2 + 1, key.y)] = Wall()
        elif val == "O":
            box = Box(
                Vector2i(key.x * 2, key.y),
                Vector2i(key.x * 2 + 1, key.y)
            )
            
            new_layout[box.left_part] = box
            new_layout[box.right_part] = box
            
    return (
        new_layout,
        Vector2i(robot.x * 2, robot.y),
        w * 2,
        h
    )