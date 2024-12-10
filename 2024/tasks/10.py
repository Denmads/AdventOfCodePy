from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

type TopographicMap = dict[int, dict[int, int]]

def parse_input(data: str, part: str) -> TopographicMap:
    map = {}
    
    for y, line in enumerate(data.split("\n")):
        for x, digit in enumerate(list(line)):
            if x not in map:
                map[x] = {}
                
            map[x][y] = int(digit)
            
    return map


# //////////////////// PARTS /////////////////////////

def run_a(map: TopographicMap):
    total = 0
    
    for y in range(len(map[0])):
        for x in range(len(map)):
            if map[x][y] == 0:
                total += count_trailhead_ends(map, x, y)

    print(f"Total score is {total}")


def run_b(map: TopographicMap):
    total = 0
    
    for y in range(len(map[0])):
        for x in range(len(map)):
            if map[x][y] == 0:
                total += count_trailhead_rating(map, x, y)

    print(f"Total score is {total}")


def count_trailhead_ends(map: TopographicMap, x: int, y: int) -> int:
    tiles_to_check = [(x, y)]
    nines = set()
    
    width = len(map)
    height = len(map[0])
    
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]
    
    while len(tiles_to_check) > 0:
        
        (check_x, check_y) = tiles_to_check.pop(0)
        
        if map[check_x][check_y] == 9:
            nines.add((check_x, check_y))
            continue
        
        for dir_x, dir_y in directions:
            new_x = check_x + dir_x
            new_y = check_y + dir_y
            
            if new_x >= 0 and new_x < width and new_y >= 0 and new_y < height:
                # inside map
                
                height_diff = map[new_x][new_y] - map[check_x][check_y]
                if height_diff == 1:
                    tiles_to_check.append((new_x, new_y))
                    
    return len(nines)
            
            
def count_trailhead_rating(topo_map: TopographicMap, x: int, y: int) -> int:
    tiles_to_check = [(x, y, 1)]
    nines = []
    
    width = len(topo_map)
    height = len(topo_map[0])
    
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]
    
    while len(tiles_to_check) > 0:
        
        (check_x, check_y, trail_id) = tiles_to_check.pop(0)
        
        if topo_map[check_x][check_y] == 9:
            nines.append((check_x, check_y, trail_id))
            continue
        
        offset = 0
        for dir_x, dir_y in directions:
            new_x = check_x + dir_x
            new_y = check_y + dir_y
            
            if new_x >= 0 and new_x < width and new_y >= 0 and new_y < height:
                # inside map
                
                height_diff = topo_map[new_x][new_y] - topo_map[check_x][check_y]
                if height_diff == 1:
                    tiles_to_check.append((new_x, new_y, trail_id + offset))
                    offset += 1
    
    return len(nines)
    
    