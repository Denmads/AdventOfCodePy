from typing import Any

from utils.vector import Vector2i

# //////////////////// PARSING & TYPES /////////////////////////

def parse_input(data: str, part: str) -> tuple[dict[str, list[Vector2i]], int, int]:
    antenneas: dict[str, list[Vector2i]] = {}
    
    width = len(data.split("\n")[0])
    height = len(data.split("\n"))
    
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(list(line)):
            if char != ".":
                if char not in antenneas:
                    antenneas[char] = []
                    
                antenneas[char].append(Vector2i(x, y))
                
    return (antenneas, width, height)


# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[dict[str, list[Vector2i]], int, int]):
    (antennas, width, height) = data
    anti_nodes: set[Vector2i] = set()
    
    def inside(point: Vector2i) -> bool:
        return point.x >= 0 and point.x < width and point.y >= 0 and point.y < height
    
    for char, points in antennas.items():
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                x_diff = points[i].x - points[j].x
                y_diff = points[i].y - points[j].y
                
                nodes = [
                    Vector2i(points[i].x + x_diff, points[i].y + y_diff),
                    Vector2i(points[i].x - x_diff, points[i].y - y_diff),
                    
                    Vector2i(points[j].x + x_diff, points[j].y + y_diff),
                    Vector2i(points[j].x - x_diff, points[j].y - y_diff),
                ]
                
                anti = list(filter(lambda p: p not in [points[i], points[j]], nodes))
                anti = list(filter(inside, anti))
                [anti_nodes.add(p) for p in anti]

    print(f"Unique anti nodes: {len(anti_nodes)}")

def run_b(data: tuple[dict[str, list[Vector2i]], int, int]):
    (antennas, width, height) = data
    anti_nodes: set[Vector2i] = set()
    
    def inside(point: Vector2i) -> bool:
        return point.x >= 0 and point.x < width and point.y >= 0 and point.y < height
    
    for char, points in antennas.items():
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                x_diff = points[i].x - points[j].x
                y_diff = points[i].y - points[j].y
                
                anti = set()
                
                for antenna, dir_vec in [(points[i], Vector2i(x_diff, y_diff)), (points[j], Vector2i(-x_diff, -y_diff))]:
                    pos = Vector2i(antenna.x, antenna.y)
                    
                    while inside(pos):
                        anti.add(pos.copy())
                        pos += dir_vec
                    
                [anti_nodes.add(p) for p in anti]

    print(f"Unique anti nodes: {len(anti_nodes)}")