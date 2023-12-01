from typing import Type
from DailyAssignment import DailyAssignment
from dataclasses import dataclass


class PolymerExpansion(DailyAssignment):
    def __init__(self):
        super().__init__(14)

    def run_part_a(self, input: str):
        polymer, rules = parse_polymer_and_rules(input)
        counts = do_expansion(polymer, rules, 10)
        
        min_cnt = min(counts.values())
        max_cnt = max(counts.values())
        print(max_cnt - min_cnt)

    def run_part_b(self, input: str):
        polymer, rules = parse_polymer_and_rules(input)
        counts = do_expansion(polymer, rules, 40)
        
        min_cnt = min(counts.values())
        max_cnt = max(counts.values())
        print(max_cnt - min_cnt)

def do_expansion(polymer, rules, num_iterations):
    polymer = list(polymer)
    result = {}
    seen = {}
    for i in range(len(polymer)-1):
        counts = expand_and_count(polymer[i], polymer[i+1], rules, num_iterations, seen)
        for key, val in counts.items():
            if key not in result:
                result[key] = val
            else:
                result[key] += val
    for ch in polymer:
        if ch not in result:
            result[ch] = 1
        else:
            result[ch] += 1
    return result

def expand_and_count(item1, item2, rules, iterations, seen):
    if iterations == 0:
        return {} 

    counts = {}
    if (item1+item2, iterations) in seen:
        counts = seen[(item1+item2, iterations)]
    else:
        middle = rules[(item1, item2)]
        counts[middle] = 1
        left_counts = expand_and_count(item1, middle, rules, iterations-1, seen)
        for key, val in left_counts.items():
            if key not in counts:
                counts[key] = val
            else:
                counts[key] += val
        right_counts = expand_and_count(middle, item2, rules, iterations-1, seen)
        for key, val in right_counts.items():
            if key not in counts:
                counts[key] = val
            else:
                counts[key] += val
        seen[(item1+item2, iterations)] = counts
    return counts

def parse_polymer_and_rules(input):
    sections = input.split("\n\n")
    
    rules = {}
    for line in sections[1].split("\n"):
        parts = line.split(" -> ")
        rules[tuple(parts[0])] = parts[1]
    
    return (sections[0], rules)