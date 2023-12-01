from DailyAssignment import DailyAssignment

class CrabsInSubmarines(DailyAssignment):
    def __init__(self):
        super().__init__(7)

    def run_part_a(self, input: str):
        positions = count_positions(input)
        minp, maxp = min_and_max_pos(positions)
        min_fuel = 9999999999999999
        for pos in range(minp, maxp+1):
            fuel = get_summed_dist(positions, pos)
            if fuel < min_fuel: min_fuel = fuel
        print(min_fuel)

    def run_part_b(self, input: str):
        positions = count_positions(input)
        minp, maxp = min_and_max_pos(positions)
        min_fuel = 9999999999999999
        for pos in range(minp, maxp+1):
            print(f"Doing {pos} out of {maxp}")
            fuel = get_summed_dist_expensive(positions, pos)
            if fuel < min_fuel: min_fuel = fuel
        print(min_fuel)

def count_positions(input):
    counts = {}
    for pos in input.split(","):
        if pos not in counts:
            counts[pos] = 0
        counts[pos] += 1
    return counts

def min_and_max_pos(counts):
    minp = 99999999999
    maxp = -99999999999
    for pos in counts.keys():
        pi = int(pos)
        if pi < minp: minp = pi
        if pi > maxp: maxp = pi
    return (minp, maxp)

def get_summed_dist(positions, pos):
    total = 0
    for key_pos in positions.keys():
        kpi = int(key_pos)
        dist = abs(kpi - pos)
        total += dist * positions[key_pos]
    return total

def get_summed_dist_expensive(positions, pos):
    total = 0
    precalc = {}
    for key_pos in positions.keys():
        kpi = int(key_pos)
        if key_pos in precalc:
            dist = precalc[key_pos]
        else:
            dist = sum(range(1, abs(kpi - pos)+1))
            precalc[key_pos] = dist
        total += dist * positions[key_pos]
    return total