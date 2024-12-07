from dataclasses import dataclass
from enum import Enum
from typing import Any

from utils.parse_util import parse_lines

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Calibration:
    result: int
    values: list[int]
    
class Operator(Enum):
    ADD = 1
    MULT = 2
    CONCAT = 3

def parse_input(data: str, part: str) -> list[Calibration]:
    calibrations = []
    
    def parse_calibration(line: str):
        [result_str, value_str] = line.split(": ")
        values = value_str.split(" ")
        
        calibrations.append(Calibration(
            int(result_str),
            list(map(int, values))
        ))
    
    parse_lines(data, parse_calibration)
    
    return calibrations


# //////////////////// PARTS /////////////////////////

def run_a(data: list[Calibration]):
    valid = []
    for calibration in data:
        if is_valid_calibration(calibration):
            valid.append(calibration)
            
    total = sum(map(lambda c: c.result, valid))
    print(f"Total is: {total}")

def run_b(data: list[Calibration]):
    valid = []
    progress = 0
    for calibration in data:
            if is_valid_calibration(calibration, include_concat=True):
                valid.append(calibration)
                
            progress += 1
            print(f"Checked {progress}/{len(data)}")
    
    total = sum(map(lambda c: c.result, valid))
    print(f"Total is: {total}")



def get_possible_operator_sequences(n: int, include_concat: bool = False) -> list[list[Operator]]:
    if n == 1:
        single_options = [[Operator.ADD], [Operator.MULT]]
        if include_concat:
            single_options.append([Operator.CONCAT])
        return single_options
    
    one_less = get_possible_operator_sequences(n-1, include_concat)
    
    possible = []
    for sequence in one_less:
        for operator in Operator:
            if not include_concat and operator == Operator.CONCAT:
                continue
            
            new_seq = sequence.copy()
            new_seq.insert(0, operator)
        
            possible.append(new_seq)
            
    return possible


def is_valid_calibration(calibration: Calibration, include_concat: bool = False) -> bool:
    
    if len(calibration.values) == 1:
        return calibration.values[0] == calibration.result
    
    operator_mutations = get_possible_operator_sequences(len(calibration.values)-1, include_concat)
    
    for mutation in operator_mutations:
        total = calibration.values[0]
        
        for i in range(0, len(mutation)):
            if mutation[i] == Operator.ADD:
                total += calibration.values[i+1]
            elif mutation[i] == Operator.MULT:
                total *= calibration.values[i+1]
            elif mutation[i] == Operator.CONCAT:
                total = int(str(total) + str(calibration.values[i+1]))
             
        if total == calibration.result:
            return True
        
    return False