from DailyAssignment import DailyAssignment

class FrequencyChanges(DailyAssignment):
    def __init__(self):
        super().__init__(1)

    def run_part_a(self, input: str):
        changes = list(map(lambda x: int(x), input.split("\n")))
        result = sum(changes)
        print(f"Resulting frequency after changes is '{result}'!")

    def run_part_b(self, input: str):
        changes = list(map(lambda x: int(x), input.split("\n")))
        result = 0
        seen = []
        index = 0
        while result not in seen:
            seen.append(result)
            result += changes[index]
            index += 1
            if index == len(changes):
                index = 0
                print(len(seen))

        print(f"Frequency already seen '{result}'")
