from dataclasses import dataclass, field
from typing import Any
import re

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class SpringRecord:
    states: list[str]
    groups: list[int]
    
    unknown_indicies: list[int] = field(default_factory=list)
    
    def __post_init__(self):
        for i, c in enumerate(self.states):
            if c == '?':
                self.unknown_indicies.append(i)
    
    def _to_complete(self, unknown_states: list[str]) -> str:
        copy = [*self.states]
        for i, idc in enumerate(self.unknown_indicies):
            copy[idc] = unknown_states[i]
            
        return ''.join(copy)
    
    def is_valid(self, solution: list[str]) -> bool:
        complete = self._to_complete(solution)
        
        groups = re.split('\\.+', complete)
        groups = list(map(len, filter(lambda g: g != '' , groups)))
        
        return groups == self.groups
    

def parse_input(data: str, part: str) -> list[SpringRecord]:
    lines = data.split('\n')
    
    records = []
    for line in lines:
        (states, groups) = line.split(' ')
        records.append(SpringRecord(
            list(states),
            list(map(int, groups.split(',')))
        ))

    return records

# //////////////////// PARTS /////////////////////////

def generate_all_possibilities(n: int) -> dict[int, list[list[str]]]:   
    if n == 1:
        return { 1: [['.'], ['#']]}
    
    possible = generate_all_possibilities(n-1)
    mutations = []
    for small in possible[n-1]:
        mutations.append([*small, '.'])
        mutations.append([*small, '#'])
    
    possible[n] = mutations
    return possible


def run_a(records: list[SpringRecord]):
    
    max_cnt = 0
    for record in records:
        if len(record.unknown_indicies) > max_cnt:
            max_cnt = len(record.unknown_indicies)

    
    solutions = generate_all_possibilities(max_cnt)
    
    cnt = 0
    n = len(records)
    for i, record in enumerate(records):
        print(f'{i}/{n}')
        for solution in solutions[len(record.unknown_indicies)]:
            if record.is_valid(solution):
                cnt += 1
                
    print(cnt)
            

def run_b(data: Any):
    pass