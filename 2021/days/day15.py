from DailyAssignment import DailyAssignment

class ChitonProblems(DailyAssignment):
    def __init__(self):
        super().__init__(15)

    def run_part_a(self, input: str):
        cave = parse_risk_levels(input)
        path = lowest_cost_path(cave, (0, 0), (len(cave)-1, len(cave[0])-1))
        total = sum(list(map(lambda x: cave[x[0]][x[1]], path[1:])))
        print(total)

    def run_part_b(self, input: str):
        original_scan = parse_risk_levels(input)
        cave = create_cave_map(original_scan)
        path = lowest_cost_path(cave, (0, 0), (len(cave)-1, len(cave[0])-1))
        total = sum(list(map(lambda x: cave[x[0]][x[1]], path[1:])))
        print(total)

def create_cave_map(scan):
    width = len(scan)
    height = len(scan[0])

    cave = [[0] * (height * 5) for x in range(width * 5)]
    for x in range(width):
        for y in range(height):
            for x_tile in range(5):
                line = ""
                for y_tile in range(5):
                    dist = x_tile + y_tile
                    val = scan[x][y] + dist
                    line += str(val if val < 10 else val % 10 + 1)
                    cave[x + width*x_tile][y + height * y_tile] = val if val < 10 else val % 10 + 1
    return cave

def lowest_cost_path(cave, start, end):
    queue = [start]
    came_from = {}

    g_score = {}
    g_score[start] = 0

    f_score = {}
    f_score[start] = h_score(start, end)

    neighbor_offsets = [
        [-1, 0],
        [0, -1],
        [1, 0],
        [0, 1]
    ]

    while len(queue) > 0:
        current = queue.pop(0)
        if h_score(current, end) % 100 == 0:
            print(h_score(current, end))
        if current == end:
            return make_path(came_from, current)
        
        for offset in neighbor_offsets:
            neighbor = (current[0] + offset[0], current[1] + offset[1])
            if neighbor[0] >= 0 and neighbor[0] < len(cave) and neighbor[1] >= 0 and neighbor[1] < len(cave[0]):

                temp_g_score = (g_score[current] if current in g_score else 9999999999999999999) + cave[neighbor[0]][neighbor[1]]
                if temp_g_score < (g_score[neighbor] if neighbor in g_score else 9999999999999999999):
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h_score(neighbor, end)
                    if neighbor not in queue:
                        queue.append(neighbor)
                        queue.sort(key=lambda x: f_score[x] if x in f_score else 9999999999999999999999)

    return []

def h_score(node, end):
    return abs(end[0] - node[0]) + abs(end[1] - node[1])

def make_path(came_from, end):
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = came_from[current] if current in came_from else None
    return path

def parse_risk_levels(input):
    return [list(map(int, list(line))) for line in input.split("\n")]