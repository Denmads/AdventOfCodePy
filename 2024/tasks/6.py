from dataclasses import dataclass
from enum import Enum
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

class Direction(Enum):
    UP = "^",
    DOWN = "v",
    LEFT = "<",
    RIGHT = ">"

@dataclass
class Vector2:
    x: int
    y: int
    
    def __hash__(self):
        return hash(self.x) + hash(self.y)
    
@dataclass
class Guard:
    x: int
    y: int
    dir: Direction
    
    def copy(self) -> "Guard":
        return Guard(self.x, self.y, self.dir)
    
@dataclass
class Map:
    width: int
    height: int
    
    def is_inside(self, x: int, y: int):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

def parse_input(data: str, part: str) -> tuple[Guard, set[Vector2], Map]:
    obstacles: set[Vector2] = set()
    guard: Guard = None
    room_map: Map = Map(len(data.split("\n")[0]), len(data.split("\n")))
    
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(list(line)):
            if char == "#":
                obstacles.add(Vector2(x, y))
            elif char == "^":
                guard = Guard(x, y, Direction.UP)
                
    return (guard, obstacles, room_map)




# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[Guard, list[Vector2], Map]):
    
    (guard, obstacles, room) = data
    
    path = follow_path(guard, obstacles, room)
    
    visited = list(map(lambda x: (x[0], x[1]), path))
        
    print(f"Path length: {len(visited)}")
    print(f"Visitied: {len(set(visited))}")


def run_b(data: tuple[Guard, set[Vector2], Map]):
    (guard, obstacles, room) = data
    
    # guard_start_x = guard.x
    # guard_start_y = guard.y
    
    path = follow_path(guard.copy(), obstacles, room)
    path_set = set(map(lambda c: (c[0], c[1]), path))
    
    valid_positions = set()
    progress = 0
    path_length = len(path_set)
    for x, y in path_set:
         
        # if progress > 100:
        #      break
            
        new_obstacle = Vector2(x, y)
        if new_obstacle in obstacles or (x == guard.x and y == guard.y):
            continue
        
        new_obstacles = obstacles.copy()
        new_obstacles.add(new_obstacle)
        
        if ends_in_loop(guard.copy(), new_obstacles, room):
            # print(f"Path: {x}, {y}")
            # print_path(guard.copy(), new_obstacles, room)
            valid_positions.add((x, y))
                
        progress += 1
        if (progress % 100 == 0 or progress == path_length):
            print(f"Done {progress}/{path_length}")
        
        
        # 3, 6
        # 6, 7
        # 7, 7
        # 1, 8
        # 3, 8
        # 7, 9
                
                
    print(f"Number of valid positions: {len(valid_positions)}")
            

def print_path(guard: Guard, obstacles: set[Vector2], room: Map):
    path = follow_path(guard.copy(), obstacles, room)
    path_dict = {}
    
    for x, y, dir in path:
        path_dict[(x, y)] = dir
    
    for y in range(room.height):
        for x in range(room.width):
            if (x, y) in path_dict:
                print(path_dict[(x, y)].value[0], end="")
            elif Vector2(x, y) in obstacles:
                print("#", end="")
            else:
                print(".", end="")
                
        print("")
               


def get_dir_vector(dir: Direction) -> Vector2:
    match dir:
        case Direction.UP:
            return Vector2(0, -1)
        case Direction.DOWN:
            return Vector2(0, 1)
        case Direction.LEFT:
            return Vector2(-1, 0)
        case Direction.RIGHT:
            return Vector2(1, 0)
        
def get_next_dir(dir: Direction) -> Direction:
    match dir:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP

def follow_path(guard: Guard, obstacles: set[Vector2], room: Map) -> list[tuple[int, int, Direction]]:
    path = []
    
    while (room.is_inside(guard.x, guard.y)):
        dir = get_dir_vector(guard.dir)
        
        in_front_pos = Vector2(guard.x + dir.x, guard.y + dir.y)
        if in_front_pos in obstacles:
            guard.dir = get_next_dir(guard.dir)
            
        dir = get_dir_vector(guard.dir)
        
        position = (guard.x, guard.y, guard.dir)
        if (position in path):
            return path
        
        path.append(position)
            
        guard.x += dir.x
        guard.y += dir.y
        
    return path
        
def ends_in_loop(guard: Guard, obstacles: set[Vector2], room: Map) -> bool:
    visited: set = set()
    
    while (room.is_inside(guard.x, guard.y)):
        dir = get_dir_vector(guard.dir)
        
        in_front_pos = Vector2(guard.x + dir.x, guard.y + dir.y)
        if in_front_pos in obstacles:
            guard.dir = get_next_dir(guard.dir)
            
        dir = get_dir_vector(guard.dir)
        
        position = (guard.x, guard.y, guard.dir)
        if (position in visited):
            return True
        
        visited.add(position)
            
        guard.x += dir.x
        guard.y += dir.y
        
    return False