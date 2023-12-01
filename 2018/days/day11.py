from DailyAssignment import DailyAssignment

class PowerLevels(DailyAssignment):
    def __init__(self):
        super().__init__(11)

    def run_part_a(self, input: str):
        serial = int(input)
        grid = [[0] * 300 for _ in range(300)]
        
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                grid[x][y] = calc_power_level(x, y, serial)
        
        largest_power = 0
        coord = ""

        for x in range(1, len(grid)-1):
            for y in range(1, len(grid[x])-1):
                sum = 0
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        sum += grid[x + x_off][y + y_off]
                if sum > largest_power:
                    largest_power = sum
                    coord = str(x-1) + "," + str(y-1)
        
        print(coord)

    def run_part_b(self, input: str):
        serial = int(input)
        grid = [[0] * 300 for _ in range(300)]
        
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                grid[x][y] = calc_power_level(x, y, serial)
        

        largest_power = 0
        coord = ""

        prev_calcs = [[0] * 300 for _ in range(300)]
        for size in range(1, 301):
            one_less_size = size - 1
            print(size)

            calcs = [[0] * (300-size+1) for _ in range(300-size+1)]

            for x in range(0, len(calcs)):
                for y in range(0, len(calcs[x])):
                    sum = prev_calcs[x][y]
                    for i in range(one_less_size):
                        sum += grid[x+i][y+one_less_size] + grid[x+one_less_size][y+i]
                    sum += grid[x+one_less_size][y+one_less_size]
                    calcs[x][y] = sum
                    if sum > largest_power:
                        largest_power = sum
                        coord = str(x) + "," + str(y) + "," + str(size)
            prev_calcs = calcs

        print(coord)


def calc_power_level(x, y, serial):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    power_level = int(str(power_level)[-3]) if power_level > 99 else 0
    return power_level - 5
