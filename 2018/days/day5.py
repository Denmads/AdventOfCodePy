from DailyAssignment import DailyAssignment
from dataclasses import dataclass

class PolymerReactions(DailyAssignment):
    def __init__(self):
        super().__init__(5)

    def run_part_a(self, input: str):
        units = full_react(input)
        print(f"No more reactions, remaning units '{len(units)}'")

    def run_part_b(self, input: str):
        shortest = 999999999999999999
        for ascii in range(65, 91):
            print(chr(ascii))
            reduced_polymer = remove_units(input, ascii)
            reacted_polymer = full_react(reduced_polymer)
            if len(reacted_polymer) < shortest:
                shortest = len(reacted_polymer)
        print(f"Shortest solution '{shortest}'")

def remove_units(polymer, upper_unit_ascii):
    upper_char = chr(upper_unit_ascii)
    lower_char = chr(upper_unit_ascii + 32)
    polymer = polymer.replace(upper_char, '')
    polymer = polymer.replace(lower_char, '')
    return polymer

def full_react(polymer):
    units = polymer
    reactions = scan_for_reactions(units)
    while reactions is None or len(reactions) != 0:
        units = resolve_reactions(units, reactions)
        reactions = scan_for_reactions(units)
    return units

def scan_for_reactions(units):
    reactions = []
    for i in range(len(units)-1):
        unit1 = units[i]
        unit2 = units[i+1]

        if abs(ord(unit1) - ord(unit2)) == 32 and i-1 not in reactions:
            reactions.append(i)
    return reactions

def resolve_reactions(units, reactions):
    for i in range(len(reactions)-1, -1, -1):
        units = units[:reactions[i]] + units[reactions[i]+2:]
    return units