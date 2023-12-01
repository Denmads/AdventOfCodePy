from DailyAssignment import DailyAssignment

class HotCaves(DailyAssignment):
    def __init__(self):
        super().__init__(9)

    def run_part_a(self, input: str):
        height_map = parse_height_map(input)
        total = 0
        for x in range(len(height_map)):
            for y in range(len(height_map[x])):
                if is_low_spot(height_map, x, y): total += height_map[x][y] + 1
        print(total)

    def run_part_b(self, input: str):
        height_map = parse_height_map(input)
        basins = []
        for x in range(len(height_map)):
            for y in range(len(height_map[x])):
                if is_low_spot(height_map, x, y):
                    size = calc_basin_size(height_map, x, y)
                    if len(basins) < 3:
                        basins.append(size)
                        basins.sort()
                    elif size > basins[0]:
                        basins[0] = size
                        basins.sort()                    
        print(basins[0] * basins[1] * basins[2])

def calc_basin_size(height_map, x, y):
    queue = [(x, y)]
    checked = []
    while len(queue) > 0:
        current = queue.pop(0)
        checked.append(current)
        for i in range(-1, 2):
            for j in range(-1, 2):
                check_x = current[0] + i
                check_y = current[1] + j
                if check_x < 0 or check_x >= len(height_map) or check_y < 0 or check_y >= len(height_map[x]):
                    continue
                if abs(i) + abs(j) == 1:
                    item = (check_x, check_y)
                    if height_map[check_x][check_y] < 9 and item not in queue and item not in checked:
                        queue.append((check_x, check_y))
                #    if height_map[current[0]][current[1]] - height_map[check_x][check_y] == -1 and height_map[check_x][check_y] != 9:
                #        item = (check_x, check_y)
                #        if item not in queue and item not in checked:
                #            queue.append((check_x, check_y))
    return len(checked)

def is_low_spot(height_map, x, y):
    is_low = True
    for i in range(-1, 2):
        for j in range(-1, 2):
            check_x = x + i
            check_y = y + j
            if check_x < 0 or check_x >= len(height_map) or check_y < 0 or check_y >= len(height_map[x]):
                continue
            if abs(i) + abs(j) == 1:
                is_low = is_low and height_map[x][y] < height_map[check_x][check_y]
    return is_low

def parse_height_map(input):
    lines = input.split('\n')
    heights = []
    for line in lines:
        heights.append(
            list(map(int, list(line)))
        )
    return heights