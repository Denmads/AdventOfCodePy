import time
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

def parse_input(data: str, part: str) -> list[int]:
    return list(map(int, data.split(" ")))


# //////////////////// PARTS /////////////////////////

def run_a(data: list[int]):
    stones = data
    for _ in range(25):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                stone_str = str(stone)
                stone_left = int(stone_str[:len(stone_str)//2])
                stone_right = int(stone_str[len(stone_str)//2:])
                new_stones.append(stone_left)
                new_stones.append(stone_right)
            else:
                new_stones.append(stone * 2024)
                
        stones = new_stones
        
    print(f"Number of stones: {len(stones)}")
                
    

def run_b(data: list[int]):
    stone_lookup: dict[tuple[int, int], int] = {}
    
    total = 0
    for stone in data:
        total += get_stones(stone, 75, stone_lookup)
        
    print(f"Number of stones: {total}")
    
def get_stones(stone: int, n: int, lookup: dict[tuple[int, int], int]) -> int:
    if n == 0:
        return 1
    
    if (stone, n) in lookup:
        return lookup[(stone, n)]
    
    count = 1
    if stone == 0:
        count = get_stones(1, n-1, lookup)
    elif len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        stone_left = int(stone_str[:len(stone_str)//2])
        stone_right = int(stone_str[len(stone_str)//2:])
        count = get_stones(stone_left, n-1, lookup) + get_stones(stone_right, n-1, lookup)
    else:
        count = get_stones(stone * 2024, n-1, lookup)
        
    lookup[(stone, n)] = count
    return count