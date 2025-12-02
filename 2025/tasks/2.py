from dataclasses import dataclass
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Range:
    start: int
    length: int

def parse_input(data: str, part: str) -> list[Range]:
    ranges_str = data.split(",")
    
    ranges = []
    for range_str in ranges_str:
        parts = range_str.split("-")
        start = int(parts[0])
        end = int(parts[1])
        
        ranges.append(Range(start, end - start))
        
    return ranges


# //////////////////// PARTS /////////////////////////

def run_a(data: list[Range]):
    sum = 0
    
    for rng in data:
        for i in range(rng.start, rng.start + rng.length + 1):
            i_str = str(i)
            if len(i_str) % 2 == 0:
                middle = len(i_str) // 2
                
                if i_str[:middle] == i_str[middle:]:
                    sum += i
                    
    print(f"Total Sum: {sum}")
        

def run_b(data: list[Range]):
    sum = 0
    
    for rng in data:
        for i in range(rng.start, rng.start + rng.length + 1):
            i_str = str(i)
            middle = len(i_str) // 2
            
            for pl in range(1, middle+1):
                if len(i_str) % pl == 0:
                    pattern = i_str[:pl]
                    
                    only_patterns = True
                    for offset in range(1, len(i_str) // pl):
                        if pattern != i_str[offset*pl:offset*pl+pl]:
                            only_patterns = False
                            break
                        
                    if not only_patterns:
                        continue
                    
                    sum += i
                    break
                    
    print(f"Total Sum: {sum}")