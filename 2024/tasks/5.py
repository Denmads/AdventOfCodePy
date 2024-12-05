from typing import Any

from utils.parse_util import parse_lines

# //////////////////// PARSING & TYPES /////////////////////////

type Update = dict[int, int]

type PageRules = dict[int, list[int]]

def parse_input(data: str, part: str) -> tuple[PageRules, list[Update]]:
    [rules_str, updates_str] = data.split("\n\n")
    
    rules: PageRules = {}
    def parse_rule(line: str):
        [before, after] = list(map(lambda x: int(x), line.split("|")))
        
        if before not in rules:
            rules[before] = []
            
        rules[before].append(after)
    
    parse_lines(rules_str, parse_rule)  
    
    updates : list[Update] = []
    def parse_update(line: str):
        update = {}
        for i, page_str in enumerate(line.split(",")):
            update[int(page_str)] = i
            
        updates.append(update)
    
    parse_lines(updates_str, parse_update)

    return (rules, updates)

# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[PageRules, list[Update]]):
    (rules, updates) = data
    
    valid_updates: list[Update] = []
    
    for update in updates:
        if is_update_valid(rules, update):
            valid_updates.append(update)
            
    sum_of_middle = 0
    for update in valid_updates:
        middle_index = len(update) // 2
        for page, index in update.items():
            if index == middle_index:
                sum_of_middle += page
                break
            
    print(f"Sum of all valid middle pages: {sum_of_middle}")

def run_b(data: tuple[PageRules, list[Update]]):
    (rules, updates) = data
    
    invalid_updates: list[Update] = []
    
    for update in updates:
        if not is_update_valid(rules, update):
            invalid_updates.append(update)
    
    valid_updates = list(map(lambda ud: fix_update(rules, ud), invalid_updates))
    
    sum_of_middle = 0
    for update in valid_updates:
        middle_index = len(update) // 2
        for page, index in update.items():
            if index == middle_index:
                sum_of_middle += page
                break

    print(f"Sum of all valid middle pages: {sum_of_middle}")


def is_update_valid(rules: PageRules, update: Update) -> bool:
    for page in update.keys():
        if page in rules:
            for after_page in rules[page]:
                if after_page in update and update[page] > update[after_page]:
                    return False
                
    return True


def fix_update(rules: PageRules, update: Update) -> Update:
    fixed_update: Update = {}
    
    for page in update.keys():
        valid_rules = 0
        if page in rules:
            for after_page in rules[page]:
                if after_page in update:
                    valid_rules += 1
                
        fixed_update[page] = (len(update)-1) - valid_rules
        
    return fixed_update