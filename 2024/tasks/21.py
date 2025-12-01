from typing import Any

from utils.vector import Vector2i

# //////////////////// PARSING & TYPES /////////////////////////

type KeypadDict = dict[str, Vector2i]
type MoveDict = dict[tuple[str, str], int]

def create_keypad(keypad_lines: list[str]) -> KeypadDict:
    keypad: KeypadDict = {}
    
    for y, line in enumerate(keypad_lines):
        for x, char in enumerate(list(line)):
            if char != " ":
                keypad[char] = Vector2i(x, y)
        
    return keypad

def parse_input(data: str, part: str) -> list[str]:
    return data.split("\n")

NUMERIC_KEYPAD = create_keypad(["789", "456", "123", " 0A"])
DIRECTIONAL_KEYPAD = create_keypad([" ^A", "<v>"])

DIRECTIONAL_KEYPAD_PATHS = {
            ('A', 'A'): '',
            ('A', '^'): '<',
            ('A', '>'): 'v',
            ('A', 'v'): 'v<',
            ('A', '<'): 'v<<',
            
            ('^', 'A'): '>',
            ('^', '^'): '',
            ('^', '>'): 'v>',
            ('^', 'v'): 'v',
            ('^', '<'): 'v<',
            
            ('>', 'A'): '^',
            ('>', '^'): '<^',
            ('>', '>'): '',
            ('>', 'v'): '<',
            ('>', '<'): '<<',
            
            ('v', 'A'): '^>',
            ('v', '^'): '^',
            ('v', '>'): '>',
            ('v', 'v'): '',
            ('v', '<'): '<',
            
            ('<', 'A'): '>>^',
            ('<', '^'): '>^',
            ('<', '>'): '>>',
            ('<', 'v'): '>',
            ('<', '<'): '',
        }

# //////////////////// PARTS /////////////////////////

def run_a(codes: list[str]):
    keypad_moves = get_moves([NUMERIC_KEYPAD, DIRECTIONAL_KEYPAD, DIRECTIONAL_KEYPAD])

def run_b(codes: list[str]):
    pass

def get_moves(num_levels: 3) -> MoveDict:
    if num_levels == 0:
        return 
    
    next_moves = get_moves(num_levels-1)
    move_map: MoveDict = {}