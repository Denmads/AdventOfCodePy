from dataclasses import dataclass
from utils.stack import Stack

@dataclass
class Instruction:
    amount: int
    from_index: str
    to_index: str

    @staticmethod
    def parse(data: str) -> 'Instruction':
        tokens = data.split()
        return Instruction(
            int(tokens[1]), # Amount
            tokens[3], # From
            tokens[5] # To
        )

def parse_stacks(lines: list[str]) -> dict[str, Stack]:
    lines.reverse()
    num_stacks = (len(lines[0]) + 1) // 4

    stacks = {f"{i}": Stack[str]() for i in range(1, num_stacks+1)}

    for line in lines:
        for i in range(num_stacks):
            val = line[i*4 + 1]
            if val != " ":
                stacks[f"{i+1}"].push(val)

    return stacks

def parse_input(data: str) -> tuple[dict[str, Stack[str]], list[Instruction]]:
    parts = data.split("\n\n")

    stacks = parse_stacks(parts[0].split("\n")[:-1])
    instructions = list(map(lambda l: Instruction.parse(l), parts[1].split("\n")))
    return (stacks, instructions)


def run_a(data: tuple[dict[str, Stack[str]], list[Instruction]]):
    stacks, instructions = data
    for instruction in instructions:
        stacks[instruction.from_index].transfer_to(stacks[instruction.to_index], instruction.amount)

    code = "".join([f"{s.peek()}" for k, s in stacks.items()])

    print(f"Final code: {code}")

def run_b(data: tuple[dict[str, Stack[str]], list[Instruction]]):
    stacks, instructions = data
    for instruction in instructions:
        stacks[instruction.from_index].transfer_to_without_restack(stacks[instruction.to_index], instruction.amount)

    code = "".join([f"{s.peek()}" for k, s in stacks.items()])

    print(f"Final code: {code}")