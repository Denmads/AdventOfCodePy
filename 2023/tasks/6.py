import re
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

def parse_input(data: str) -> tuple[list[int], list[int]]:
    (time_str, dist_str) = data.split('\n')

    return (
        list(map(int, re.sub(' +', ' ', time_str[9:]).strip().split(' '))),
        list(map(int, re.sub(' +', ' ', dist_str[9:]).strip().split(' '))),
    )


# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[list[int], list[int]]):
    (times, dists) = data

    product = 1

    for ri in range(len(times)):
        ways_to_win = 0
        for j in range(times[ri]+1):
            remain = times[ri] - j
            dist = j * remain
            if dist > dists[ri]:
                ways_to_win += 1
        
        product *= ways_to_win

    print(product)

def run_b(data: Any):
    (times, dists) = data

    time = int(''.join(map(str, times)))
    dist = int(''.join(map(str, dists)))

    ways_to_win = 0
    for j in range(time+1):
        remain = time - j
        my_dist = j * remain
        if my_dist > dist:
            ways_to_win += 1

    print(ways_to_win)
