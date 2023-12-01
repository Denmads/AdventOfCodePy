from typing import Tuple
from DailyAssignment import DailyAssignment
from dataclasses import dataclass

padding = 0

next_id = 1
def gen_next_id():
    global next_id
    id = str(next_id)
    next_id += 1
    return id

@dataclass
class Source:
    id: str
    point: Tuple[int, int]

@dataclass
class Cell:
    source_id: str = None
    dist_to_source: int = 999999999999999
    is_source: bool = False

class IndeterminateCoordinates(DailyAssignment):
    def __init__(self):
        super().__init__(6)

    #Use padding 0 for part a
    def run_part_a(self, input: str):
        sources = parse_sources(input)
        grid = create_grid(sources)
        place_sources(grid, sources)
        print("Counting")
        largest = 0
        for source in sources:
            count = count_cells(grid, source.id)
            if count > largest:
                largest = count
        print(f"Largest area '{largest}'")

    def run_part_b(self, input: str):
        sources = parse_sources(input)
        grid = create_grid(sources)
        place_sources_region(grid, sources)
        print("Counting")
        count = count_region(grid)
        print(f"Size of the region '{count}'")

def parse_sources(input):
    coords = list(map(lambda x: (int(x[0])+padding, int(x[1])+padding), map(lambda x: x.split(", "), input.split("\n"))))
    return list(map(lambda p: Source(gen_next_id(), p), coords))

def top_left_coord(sources):
    min_x = min(sources, key=lambda x: x.point[0])
    min_y = min(sources, key=lambda x: x.point[1])
    return (min_x.point[0], min_y.point[1])

def bottom_right_coord(sources):
    max_x = max(sources, key=lambda x: x.point[0])
    max_y = max(sources, key=lambda x: x.point[1])
    return (max_x.point[0], max_y.point[1])

def create_grid(sources):
    bottom_right = bottom_right_coord(sources)
    width = bottom_right[0] + 1
    height = bottom_right[1] + 1
    grid = []
    for x in range(width + 2 * padding):
        grid.append([])
        for _ in range(height + 2 * padding):
            grid[x].append(Cell())

    return grid

def place_sources(grid, sources):
    for source in sources:
        try:
            grid[source.point[0]][source.point[1]].is_source = True
            grid[source.point[0]][source.point[1]].source_id = source.id
            grid[source.point[0]][source.point[1]].dist_to_source = 0
        except:
            print(source)
            exit()

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            cell = grid[x][y]
            if not cell.is_source:
                for source in sources:
                    dist = abs(source.point[0] - x) + abs(source.point[1] - y)
                    if dist < cell.dist_to_source:
                        cell.dist_to_source = dist
                        cell.source_id = source.id
                    elif dist == cell.dist_to_source:
                        cell.source_id = "multiple"

def place_sources_region(grid, sources):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            cell = grid[x][y]
            cell.dist_to_source = 0
            for source in sources:
                dist = abs(source.point[0] - x) + abs(source.point[1] - y)
                cell.dist_to_source += dist

def count_cells(grid, id):
    count = 0
    ret_now = False
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            cell = grid[x][y]
            if cell.source_id == id:
                count += 1
                if x == 0 or x == len(grid)-1 or y == 0 or y == len(grid[x]):
                    count = 0
                    ret_now = True
                    break

        if ret_now:
            break
    return count

def count_region(grid):
    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            cell = grid[x][y]
            if cell.dist_to_source < 10000:
                count += 1
    return count