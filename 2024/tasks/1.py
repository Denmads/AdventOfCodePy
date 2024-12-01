from typing import Any

from utils.parse_util import parse_lines

type ParseResult = tuple[list[int], list[int]]

# //////////////////// PARSING & TYPES /////////////////////////

def parse_input(data: str, part: str) -> ParseResult:
    list1 = []
    list2 = []

    def line_func(line: str):
        values = line.split("   ")
        list1.append(int(values[0]))
        list2.append(int(values[1]))

    parse_lines(data, line_func)

    return (list1, list2)

# //////////////////// PARTS /////////////////////////

def run_a(data: ParseResult):
    (left_list, right_list) = data
    
    left_list.sort()
    right_list.sort()
    
    diffs = [abs(left_list[i] - right_list[i]) for i in range(len(left_list))]

    print(f"Total id distance: {sum(diffs)}")
        

def run_b(data: ParseResult):
    (left_list, right_list) = data
    
    counts: dict[int, int] = {}
    
    for num in left_list:
        counts[num] = 0
        
    for num in right_list:
        if (num in counts):
            counts[num] += 1
        
    scores = [num * counts.get(num, 0) for num in left_list]
    
    print(f"Similarity score: {sum(scores)}")