from DailyAssignment import DailyAssignment
from utils.gridutils import print_grid

class FlashingOctopuses(DailyAssignment):
    def __init__(self):
        super().__init__(11)

    def run_part_a(self, input: str):
        grid = parse_int_grid(input)
        total = 0
        for iteration in range(100):
            increase_all(grid)
            total += do_flashes(grid)
        print(total)

    def run_part_b(self, input: str):
        grid = parse_int_grid(input)
        total_octopuses = 100
        iter = 0
        while True:
            increase_all(grid)
            flashes = do_flashes(grid)
            iter += 1
            if flashes == total_octopuses:
                break
        print(iter)

def do_flashes(grid):
    queue = []
    flashed = []
    #initial scan
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] > 9:
                queue.append((x, y))
    
    while len(queue) > 0:
        next = queue.pop(0)
        flashed.append(next)
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = next[0] + i
                y = next[1] + j
                if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[x]): continue

                grid[x][y] += 1
                item = (x, y)
                if grid[x][y] > 9 and item not in flashed and item not in queue:
                    queue.append(item)
    
        for pos in flashed:
            grid[pos[0]][pos[1]] = 0

    return len(flashed)

def increase_all(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            grid[x][y] += 1

def parse_int_grid(input):
    return [list(map(int, list(line))) for line in input.split("\n")]