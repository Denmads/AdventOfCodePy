from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

type MulInstructions = list[(int, int)]

def parse_input(data: str, part: str) -> MulInstructions:
    instructions = []
    
    mul_enabled = True
    
    for i in range(len(data)):
        if mul_enabled and data[i] == "m":
            instruction = try_to_parse_mul_instruction(data, i)
            if instruction is not None:
                instructions.append(instruction)
                
        elif part == "b" and data[i] == "d":
            if try_parse_token(data, i, "do()"):
                mul_enabled = True
            elif try_parse_token(data, i, "don't()"):
                mul_enabled = False
                
    return instructions

def try_to_parse_mul_instruction(data: str, index: int) -> tuple[int, int] | None:
    if not try_parse_token(data, index, "mul"):
        return None
    index += 3
    
    if not try_parse_token(data, index, "("):
        return None
    index += 1
    
    num1 = try_parse_number(data, index)
    if num1 is None:
        return None
    
    index += len(str(num1))
    
    if not try_parse_token(data, index, ","):
        return None
    index += 1
    
    num2 = try_parse_number(data, index)
    if num2 is None:
        return None
    
    index += len(str(num2))
    
    if not try_parse_token(data, index, ")"):
        return None
    index += 1
    
    return (num1, num2)

def try_parse_token(data: str, index: int, token: str) -> bool:
    for char in token:
        if data[index] != char:
            return False
        
        index += 1
        
    return True   

def try_parse_number(data: str, index: int) -> int | None:
    num_str = ""
    
    while data[index].isdigit():
        num_str += data[index]
        index += 1
        
    if len(num_str) < 1 or len(num_str) > 3:
        return None
    
    return int(num_str)

# //////////////////// PARTS /////////////////////////

def run_a(data: MulInstructions):
    sum = 0
    
    for mul in data:
        sum += mul[0] * mul[1]
        
    print(f"Total sum of mul instructions is: {sum}")

def run_b(data: MulInstructions):
    sum = 0
    
    for mul in data:
        sum += mul[0] * mul[1]
        
    print(f"Total sum of mul instructions is with conditionals: {sum}")