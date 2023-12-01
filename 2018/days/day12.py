from typing import Dict, List, Type
from DailyAssignment import DailyAssignment
from dataclasses import dataclass, field

@dataclass
class PotLine:
    pots: List[bool]
    rules: Dict[str, bool] = field(default_factory=dict)
    padding_size: int = 5
    zero_index: int = 0

    def add_rule(self, rule_num, result):
        self.rules[str(rule_num)] = result

    def check_padding(self):
        #left
        cnt = 0
        for i in range(len(self.pots)):
            if not self.pots[i]:
                cnt += 1
            if cnt == self.padding_size or self.pots[i]:
                break
        missing = self.padding_size - cnt
        self.zero_index += missing
        [self.pots.insert(0, False) for _ in range(missing)]

        #right
        cnt = 0
        for i in range(len(self.pots)-1, 0, -1):
            if not self.pots[i]:
                cnt += 1
            if cnt == self.padding_size or self.pots[i]:
                break
        missing = self.padding_size - cnt
        [self.pots.append(False) for _ in range(missing)]

    def next_generation(self):
        new_gen = []
        for i in range(len(self.pots)):
            bits = ""
            for j in range(i-2, i+3):
                if j >= 0 and j < len(self.pots):
                    bits += str(int(self.pots[j]))
                else:
                    bits += "0"
            rule_num = str(int(bits, 2))
            if rule_num in self.rules:
                new_gen.append(self.rules[rule_num])
            else:
                new_gen.append(False)
        self.pots = new_gen

    def count_plant_pots(self):
        total = 0
        for i in range(len(self.pots)):
            total += i-self.zero_index if self.pots[i] else 0
        return total


class FrequencyChanges(DailyAssignment):
    def __init__(self):
        super().__init__(12)

    def run_part_a(self, input: str):
        pot_line = parse_pots_and_rules(input)
        print("".join(list(map(lambda x: "#" if x else ".", pot_line.pots))))
        for _ in range(20):
            pot_line.check_padding()
            pot_line.next_generation()
            print("".join(list(map(lambda x: "#" if x else ".", pot_line.pots))))        
        print(pot_line.count_plant_pots())

    def run_part_b(self, input: str):
        pot_line = parse_pots_and_rules(input)
        print("".join(list(map(lambda x: "#" if x else ".", pot_line.pots))))
        prev_score = 0
        for i in range(500):
            pot_line.check_padding()
            pot_line.next_generation()
            #print("".join(list(map(lambda x: "#" if x else ".", pot_line.pots))))     
            score = pot_line.count_plant_pots()
            #print(f"Gen {i}: ", score-prev_score)
            prev_score = score

        final = prev_score + (50000000000 - 500) * 78
        print(final)

def parse_pots_and_rules(input):
    sections = input.split("\n\n")
    initial_pots = list(map(lambda x: x == "#", sections[0].split(" ")[2]))
    line = PotLine(initial_pots)
    rule_lines = sections[1].split("\n")
    for rule in rule_lines:
        tokens = rule.split(" ")
        result = tokens[2] == "#"
        num = int(tokens[0].replace(".", "0").replace("#", "1"), 2)
        line.add_rule(str(num), result)
    return line