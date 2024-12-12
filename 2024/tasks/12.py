from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

@dataclass
class Plot:
    x: int
    y: int
    neighbors: list[Direction] = field(default_factory=list)

@dataclass
class Region:
    plant_type: str
    plots: list[Plot] = field(default_factory=list)

def parse_input(data: str, part: str) -> list[Region]:
    in_region = set()
    regions: list[Region] = []

    garden_map = parse_garden(data)

    for y in range(len(garden_map)):
        for x in range(len(garden_map[y])):
            if (x, y) not in in_region:
                region = flood_fill_region(garden_map, x, y)
                regions.append(region)
                
                for plot in region.plots:
                    in_region.add((plot.x, plot.y))

    return regions

def parse_garden(data: str) -> list[list[str]]:
    garden = [[] for _ in range(len(data.split("\n")[0]))]
    
    for y, line in enumerate(data.split("\n")):
        for x, plant in enumerate(list(line)):
            garden[x].append(plant)
            
    return garden

def flood_fill_region(garden: list[list[str]], x: int, y: int):
    plot_type = garden[x][y]
    plots: list[Plot] = []
    
    width = len(garden[0])
    height = len(garden)
    
    checked = set()
    to_check = set()
    to_check.add((x, y))
    while len(to_check) > 0:
        (x, y) = to_check.pop()
        plot = Plot(x, y)
        plots.append(plot)
        
        if x - 1 >= 0 and garden[x-1][y] == plot_type:
            if (x-1, y) not in to_check and (x-1, y) not in checked:
                to_check.add((x-1, y))
            plot.neighbors.append(Direction.LEFT)
        if x + 1 < width and garden[x+1][y] == plot_type:
            if (x+1, y) not in to_check and (x+1, y) not in checked:
                to_check.add((x+1, y))
            plot.neighbors.append(Direction.RIGHT)
        if y - 1 >= 0 and garden[x][y-1] == plot_type:
            if (x, y-1) not in to_check and (x, y-1) not in checked:
                to_check.add((x, y-1))
            plot.neighbors.append(Direction.UP)
        if y + 1 < height and garden[x][y+1] == plot_type:
            if (x, y+1) not in to_check and (x, y+1) not in checked:
                to_check.add((x, y+1))
            plot.neighbors.append(Direction.DOWN)
                
        checked.add((x, y))
            
    return Region(plot_type, plots)

# //////////////////// PARTS /////////////////////////

def run_a(data: list[Region]):
    
    total = 0
    for reg in data:
        perimeter = sum(map(lambda p: 4 - len(p.neighbors), reg.plots))
        total += perimeter * len(reg.plots)
        
    print(f"Price is {total}")

def run_b(data: list[Region]):
    total = 0
    for reg in data:
        
        sides: dict[tuple[int, str, str], list[int]] = {}
        
        for plot in reg.plots:
            for dir in Direction:
                if dir not in plot.neighbors:
                    orientation = "H" if dir == Direction.UP or dir == Direction.DOWN else "V"
                    index = plot.y if dir == Direction.UP or dir == Direction.DOWN else plot.x
                    alt_index = plot.x if dir == Direction.UP or dir == Direction.DOWN else plot.y
                    
                    if (index, orientation, dir.name) not in sides:
                        sides[(index, orientation, dir.name)] = []
                    
                    sides[(index, orientation, dir.name)].append(alt_index)
        
        num_sides = 0
        for positions in sides.values():
            pos_list = positions.copy()
            pos_list.sort()
            
            count = 1
            for i in range(0, len(pos_list)-1):
                if pos_list[i+1] - pos_list[i] != 1:
                    count += 1
                    
            num_sides += count
        
        total += num_sides * len(reg.plots)
        
    print(f"Price is {total}")