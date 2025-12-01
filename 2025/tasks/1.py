from dataclasses import dataclass
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Instruction:
    dir: str
    distance: int

def parse_input(data: str, part: str) -> list[Instruction]:
    return list(map(lambda x: Instruction(x[0], int(x[1:])), data.split("\n")))


# //////////////////// PARTS /////////////////////////

def run_a(data: list[Instruction]):
    current = 50
    zero_count = 0
    
    for inst in data:
        if inst.dir == "L":
            current -= inst.distance
        elif inst.dir == "R":
            current += inst.distance
            
        current = (current + 100) % 100
        
        if current == 0:
            zero_count += 1
            
    print(f"Zero Count: {zero_count}")

def run_b(data: list[Instruction]):
    current = 50
    zero_count = 0
    
    for inst in data:
        for i in range(inst.distance):
            if inst.dir == "L":
                current -= 1
            elif inst.dir == "R":
                current += 1
            
            current = (current + 100) % 100
        
            if current == 0:
                zero_count += 1
            
    print(f"Zero Count: {zero_count}")