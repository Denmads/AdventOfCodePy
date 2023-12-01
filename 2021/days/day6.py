from DailyAssignment import DailyAssignment

class LanterFish(DailyAssignment):
    def __init__(self):
        super().__init__(6)

    def run_part_a(self, input: str):
        fish_by_age = parse_fish(input)

        for _ in range(80):
            fish_by_age = next_iteration(fish_by_age)

        print(sum(fish_by_age.values()))

    def run_part_b(self, input: str):
        fish_by_age = parse_fish(input)

        for _ in range(256):
            fish_by_age = next_iteration(fish_by_age)

        print(sum(fish_by_age.values()))

def next_iteration(fish_by_age):
    new_iteration = {}
    for i in range(1, 9):
        new_iteration[str(i-1)] = fish_by_age[str(i)]
    new_iteration["8"] = fish_by_age["0"]
    new_iteration["6"] += fish_by_age["0"]
    return new_iteration

def parse_fish(input):
    fish = input.split(",")
    fish_by_age = {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0
    }
    for f in fish:
        fish_by_age[f] += 1
    return fish_by_age