from dataclasses import dataclass
from typing import Any

from utils.vector import Vector2i

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class ClawMachine:
    button_a: Vector2i
    button_b: Vector2i
    prize_location: Vector2i

def parse_input(data: str, part: str) -> list[ClawMachine]:
    
    def parse_line(line: str, final_split_char: str) -> Vector2i:
        _, pos = line.split(": ")
        x_str, y_str = pos.split(", ")
        
        x_val = int(x_str.split(final_split_char)[1])
        y_val = int(y_str.split(final_split_char)[1])
        
        return Vector2i(x_val, y_val)
    
    
    machines: list[ClawMachine] = []
    for machine_str in data.split("\n\n"):
        lines = machine_str.split("\n")
        btn_a = parse_line(lines[0], "+")
        btn_b = parse_line(lines[1], "+")
        prize = parse_line(lines[2], "=")
        
        if part == "b":
            prize.x += 10000000000000
            prize.y += 10000000000000
        
        machines.append(ClawMachine(btn_a, btn_b, prize))
        
    return machines

# //////////////////// PARTS /////////////////////////

def run_a(data: list[ClawMachine]):
    total_tokens = 0
    
    for machine in data:
        
        AX, AY = machine.button_a.x, machine.button_a.y
        BX, BY = machine.button_b.x, machine.button_b.y
        PX, PY = machine.prize_location.x, machine.prize_location.y
        
        b_presses = (AY * PX - AX * PY) / (AY * BX - AX * BY)
        a_presses = (PY - BY * b_presses) / AY
        
        if float.is_integer(a_presses) and float.is_integer(b_presses):
            total_tokens += int(3 * a_presses + b_presses)
            
    print(f"Tokens: {total_tokens}")

def run_b(data: list[ClawMachine]):
    total_tokens = 0
    
    for machine in data:
        
        AX, AY = machine.button_a.x, machine.button_a.y
        BX, BY = machine.button_b.x, machine.button_b.y
        PX, PY = machine.prize_location.x, machine.prize_location.y
        
        b_presses = (AY * PX - AX * PY) / (AY * BX - AX * BY)
        a_presses = (PY - BY * b_presses) / AY
        
        if float.is_integer(a_presses) and float.is_integer(b_presses):
            total_tokens += int(3 * a_presses + b_presses)
            
    print(f"Tokens: {total_tokens}")