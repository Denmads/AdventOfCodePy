from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

def parse_input(data: str, part: str) -> tuple[dict[str, list[str]], list[str]]:
    patterns_str, designs_str = data.split("\n\n")
    patterns = patterns_str.split(", ")
    
    pattern_dict: dict[str, list[str]] = {}
    for pattern in patterns:
        if pattern[0] not in pattern_dict:
            pattern_dict[pattern[0]] = []
            
        pattern_dict[pattern[0]].insert(0, pattern)
    
    designs = designs_str.split("\n")
    
    return (pattern_dict, designs)


# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[dict[str, list[str]], list[str]]):
    patterns, designs = data
    
    count = 0
    checked_designs: dict[str, bool] = {}
    for i, design in enumerate(designs):
        if is_possible(patterns, checked_designs, design):
            count += 1
            
        print(i)
            
    print(f"Possible designs: {count}")

def run_b(data: tuple[dict[str, list[str]], list[str]]):
    patterns, designs = data
    
    count = 0
    checked_designs: dict[str, bool] = {}
    num_ways: dict[str, int] = {}
    for i, design in enumerate(designs):
        if is_possible(patterns, checked_designs, design):
            count += possible_ways_of_creations(patterns, num_ways, design)
            
        print(i)
            
    # print(num_ways)
            
    print(f"Possible designs: {count}")


def is_possible(patterns: dict[str, list[str]], checked_designs: dict[str, bool], design: str) -> bool:
    
    if design in checked_designs:
        return checked_designs[design]
    
    if design[0] not in patterns:
        return False
    
    for pattern in patterns[design[0]]:
        new_design = design[len(pattern):]
        
        if pattern != design[:len(pattern)]:
            continue
        
        if len(new_design) == 0:
            return True
        
        if is_possible(patterns, checked_designs, new_design):
            if design not in checked_designs:
                checked_designs[design] = True
            return True
        
    if design not in checked_designs:
        checked_designs[design] = False
    return False


def possible_ways_of_creations(patterns: dict[str, list[str]], num_ways: dict[str, int], design: str, level: int = 0) -> int:
    if len(design) == 0:
        return 1
    
    if design in num_ways:
        return num_ways[design]
    
    count = 0
    for pattern in patterns[design[0]]:
        new_design = design[len(pattern):]
        
        if pattern != design[:len(pattern)]:
            continue
        
        # print(("  " * level) + pattern)
        count +=  possible_ways_of_creations(patterns, num_ways, new_design, level+1)
        
    if design not in num_ways:
        num_ways[design] = count
    return count