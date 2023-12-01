from dataclasses import dataclass, field
from typing import Union


@dataclass
class Instruction:
    operation: str
    arg: Union[int, None] = field(default=None)

    def number_of_cycles(self) -> int:
        if self.operation == "noop": return 1
        elif self.operation == "addx": return 2
    
    def execute(self, x: int) -> int:
        if self.operation == "noop": return x
        elif self.operation == "addx": return x + self.arg

    @staticmethod
    def parse(data: str) -> 'Instruction':
        tokens = data.split()
        if len(tokens) == 1:
            return Instruction(tokens[0])
        else:
            return Instruction(tokens[0], int(tokens[1]))

# //////////////////// PARSING /////////////////////////

def parse_input(data: str) -> list[Instruction]:
    return list(map(lambda l: Instruction.parse(l), data.split("\n")))


# //////////////////// PARTS /////////////////////////

def is_significant_cycle(n: int) -> bool:
    return (n-20) % 40 == 0

def run_a(data: list[Instruction]):
    cycle_counter = 0
    instruction_counter = 0
    x = 1
    instruction_end_time = data[instruction_counter].number_of_cycles()

    total = 0    

    while True:
        cycle_counter += 1

        if is_significant_cycle(cycle_counter):
            print(f"Adding {cycle_counter * x} = cycle({cycle_counter}) * x({x})")
            total += cycle_counter * x

        if cycle_counter == instruction_end_time:
            x = data[instruction_counter].execute(x)
            instruction_counter += 1
            if instruction_counter >= len(data): break
            instruction_end_time = cycle_counter + data[instruction_counter].number_of_cycles()

    print(f"Total of significant cycles: {total}")



def is_sprite_on_pixel(sprite_pos: int, pixel_pos: int) -> bool:
    return sprite_pos -1 <= pixel_pos and pixel_pos <= sprite_pos + 1

def run_b(data: list[Instruction]):
    cycle_counter = 0
    instruction_counter = 0
    x = 1
    instruction_end_time = data[instruction_counter].number_of_cycles() 

    crt_row = ""

    while True:
        cycle_counter += 1

        crt_row += "#" if is_sprite_on_pixel(x, (cycle_counter-1) % 40) else "."

        if cycle_counter != 0 and cycle_counter % 40 == 0:
            print(crt_row)
            crt_row = ""

        if cycle_counter == instruction_end_time:
            x = data[instruction_counter].execute(x)
            instruction_counter += 1
            if instruction_counter >= len(data): break
            instruction_end_time = cycle_counter + data[instruction_counter].number_of_cycles()