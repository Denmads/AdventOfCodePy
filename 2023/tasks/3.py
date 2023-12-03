from dataclasses import dataclass, field
from typing import Any, Union

# //////////////////// PARSING & TYPES /////////////////////////
@dataclass
class Number:
    string: str
    pos: tuple[int, int]
    char_positions: list[tuple[int, int]] = field(default_factory=list)

    def __post_init__(self):
        for i in range(len(self.string)):
            self.char_positions.append((self.pos[0] + i, self.pos[1]))

    def value(self) -> int:
        return int(self.string)
    
@dataclass
class Symbol:
    char: str
    pos: tuple[int, int]
    
@dataclass
class Container:
    numbers: list[Number] 
    symbols: list[Symbol]
    num_lines: int
    
    def get_numbers_on_line(self, y: int) -> list[Number]:
        return list(filter(lambda number: number.pos[1] == y, self.numbers))


def parse_input(data: str) -> Container:
    numbers = []
    symbols = []
    
    for y, line in enumerate(data.split('\n')):
        number = ""
        pos: tuple[int, int] = None
        for x, char in enumerate(line):
            if char.isnumeric():
                number += char
                
                if pos is None:
                    pos = (x, y)
            elif not char.isnumeric() and len(number) > 0:
                numbers.append(Number(number, pos))
                number = ""
                pos = None
            
            if char != '.' and not char.isnumeric():
                symbols.append(Symbol(char, (x, y)))
        
        if len(number) > 0:
            numbers.append(Number(number, pos))
            number = ""
            pos = None
    
    return Container(numbers, symbols, len(data.split('\n')))


# //////////////////// PARTS /////////////////////////

def run_a(data: Container):
    adjacent_numbers: list[Number] = []
    
    for symbol in data.symbols:
        for possible_number in get_numbers_on_adjacent_lines(symbol, data):
            if is_adjacent(symbol, possible_number):
                
                if not any(map(lambda num: num.pos == possible_number.pos, adjacent_numbers)):
                    adjacent_numbers.append(possible_number)
                    
    print(sum(map(lambda num: num.value(), adjacent_numbers)))
 
def get_numbers_on_adjacent_lines(symbol: Symbol, container: Container) -> list[Number]: 
    numbers = container.get_numbers_on_line(symbol.pos[1])
       
    if symbol.pos[1] > 0:
        for number in container.get_numbers_on_line(symbol.pos[1]-1):
            numbers.append(number)

    if symbol.pos[1] < container.num_lines-1:
        for number in container.get_numbers_on_line(symbol.pos[1]+1):
            numbers.append(number)
    
    return numbers
       
def is_adjacent(symbol: Symbol, number: Number) -> bool:
    for num_pos in number.char_positions:
        if abs(num_pos[0] - symbol.pos[0]) <= 1 and abs(num_pos[1] - symbol.pos[1]) <= 1:
            return True
        
    return False


def run_b(data: Container):
    gear_ratios: list[int] = []
    
    for symbol in data.symbols:
        if symbol.char != '*':
            continue
        
        adjacent_nums = []
        for possible_number in get_numbers_on_adjacent_lines(symbol, data):
            if is_adjacent(symbol, possible_number):
                adjacent_nums.append(possible_number)
        
        if len(adjacent_nums) == 2:
            gear_ratios.append(adjacent_nums[0].value() * adjacent_nums[1].value())

    print(sum(gear_ratios))