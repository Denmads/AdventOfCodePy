from utils.listutils import subgroup_list

class Rugsack:
    def __init__(self, content_data: str):
        self.size = int(len(content_data) / 2)
        self.left_compartment = list(content_data[:self.size])
        self.right_compartment = list(content_data[self.size:])

        self.left_compartment_types = set(self.left_compartment)
        self.right_compartment_types = set(self.right_compartment)

        self.all_types = self.left_compartment_types | self.right_compartment_types

def priority_score(symbol: str) -> int:
    if symbol.isupper(): return ord(symbol) - 38
    else: return ord(symbol) - 96 

def parse_input(data: str) -> list[Rugsack]:
    lines = data.split("\n")
    return list(map(lambda d: Rugsack(d), lines))

def run_a(data: list[Rugsack]):
    total = 0
    for rugsack in data:
        error = list(rugsack.left_compartment_types & rugsack.right_compartment_types)[0]
        total += priority_score(error)
    print(f"The total sum of priorities are: {total}")


def run_b(data: list[Rugsack]):
    total = 0
    for group in subgroup_list(data, 3, None):
        common_item = list(group[0].all_types & group[1].all_types & group[2].all_types)[0]
        total += priority_score(common_item)
    print(f"The total sum of priorities are: {total}")
