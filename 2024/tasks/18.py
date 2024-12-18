from math import sqrt
import time
from typing import Any

from utils.vector import Vector2i

# //////////////////// PARSING & TYPES /////////////////////////

def parse_input(data: str, part: str) -> list[Vector2i]:
    bytes_fallen = []
    
    for line in data.split("\n"):
        x, y = line.split(",")
        
        bytes_fallen.append(Vector2i(int(x), int(y)))

    return bytes_fallen

# //////////////////// PARTS /////////////////////////

WIDTH = 71 #7
HEIGHT = 71 #7

BYTES_FALLEN = 1024 #12
def run_a(falling_bytes: list[Vector2i]):
    start = Vector2i(0, 0)
    end = Vector2i(WIDTH-1, HEIGHT-1)
    fallen = set(falling_bytes[:BYTES_FALLEN])
    path = find_path(start, end, fallen)
    
    # txt = ""
    # for y in range(HEIGHT):
    #     for x in range(WIDTH):
    #         cur = Vector2i(x, y)
    #         if cur in fallen:
    #             txt += "\033[94m#\033[0m"
    #         elif cur in path:
    #             txt += "\033[92mO\033[0m"
    #         elif cur == start:
    #             txt += "S"
    #         elif cur == end:
    #             txt += "E"
    #         else:
    #             txt += "."
                
    #     txt += "\n"
        
    # print(txt)
    # print()
    
    print(f"Steps: {len(path.keys())}")

def run_b(falling_bytes: list[Vector2i]):
    start = Vector2i(0, 0)
    end = Vector2i(WIDTH-1, HEIGHT-1)
    
    path = find_path(start, end, set())
    
    for i in range(BYTES_FALLEN, len(falling_bytes)):
        
        if falling_bytes[i] in path:
            fallen = set(falling_bytes[:i+1])
            path = find_path(start, end, fallen)
            
            if len(path) == 0:
                print(f"The byte that prevents a path is: {falling_bytes[i].x},{falling_bytes[i].y}")
                break
        
            
        if i % 10 == 0:
            print(f"{i+1}/{len(falling_bytes)}")


def find_path(start: Vector2i, end: Vector2i, blocked: set[Vector2i]) -> dict[Vector2i, Vector2i]:
    
    def h(pos: Vector2i, end: Vector2i) -> int:
        return abs(end.x - pos.x) + abs(end.y - pos.y)
    
    g_score: dict[Vector2i, int] = {
        start: 0
    }
    f_score: dict[Vector2i, int] = {
        start: h(start, end)
    }

    came_from: dict[Vector2i, Vector2i] = {}

    open_set: set[Vector2i] = set([start])

    while len(open_set) > 0:
        current: Vector2i = find_node_with_min_fscore(open_set, f_score)

        if current == end:
            return construct_path(current, came_from)

        open_set.remove(current)

        for dir in [Vector2i(-1, 0),Vector2i(1, 0),Vector2i(0, -1),Vector2i(0, 1),]:
            neighbor = Vector2i(current.x + dir.x, current.y + dir.y)
            
            if neighbor.x < 0 or neighbor.x >= WIDTH or neighbor.y < 0 or neighbor.y >= HEIGHT or neighbor in blocked:
                continue
            
            g_score_tentative = g_score[current]+1

            if neighbor not in g_score or g_score_tentative < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = g_score_tentative
                f_score[neighbor] = g_score_tentative + h(neighbor, end)

                if neighbor not in open_set:
                    open_set.add(neighbor)
    return []

def construct_path(end: Vector2i, came_from: dict[Vector2i, Vector2i]) -> dict[Vector2i, Vector2i]:
    path: dict[Vector2i, Vector2i] = {
        end: came_from[end]
    }
    cur = end
    while came_from[cur] in came_from:
        cur = came_from[cur]
        path[cur] = came_from[cur]
    
    return path

def find_node_with_min_fscore(nodes: list[Vector2i], f_score: dict[Vector2i, int]) -> Vector2i:
    return min(nodes, key=lambda v: f_score[v])