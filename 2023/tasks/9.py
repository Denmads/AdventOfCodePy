from dataclasses import dataclass
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Sequence:
    values: list[int]
    
    def get_diff_sequence(self) -> 'Sequence':
        diffs = []
        for i in range(len(self.values)-1):
            diffs.append(self.values[i+1] - self.values[i])
            
        return Sequence(diffs)

def parse_input(data: str, part: str) -> list[Sequence]:
    return list(
        map(lambda l: Sequence(list(map(int, l.split(' ')))), data.split('\n'))
    )


# //////////////////// PARTS /////////////////////////

def run_a(sequences: list[Sequence]):
    print(sum(map(get_extrapolated_value, sequences)))

def get_extrapolated_value(sequence: Sequence) -> int:
    sequences = [sequence]
    
    while not all_zero(sequences[-1]):
        sequences.append(sequences[-1].get_diff_sequence())
        
    value = 0
    for seq in reversed(sequences[:-1]):
        value = seq.values[-1] + value
        
    return value
    
def all_zero(sequence: Sequence) -> bool:
    return all(map(lambda v: v == 0, sequence.values))


def run_b(sequences: list[Sequence]):
    print(sum(map(get_prev_extrapolated_value, sequences)))
    
def get_prev_extrapolated_value(sequence: Sequence) -> int:
    sequences = [sequence]
    
    while not all_zero(sequences[-1]):
        sequences.append(sequences[-1].get_diff_sequence())
        
    value = 0
    for seq in reversed(sequences[:-1]):
        value = seq.values[0] - value
        
    return value