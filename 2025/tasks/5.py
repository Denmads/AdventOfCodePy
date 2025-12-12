from dataclasses import dataclass
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class IdRange:
    start: int
    end: int

def parse_input(data: str, part: str) -> tuple[list[IdRange], list[int]]:
    range_lines, food_ids = data.split("\n\n")

    ranges = []
    for line in range_lines.split("\n"):
        start, end = map(int, line.split("-"))
        ranges.append(IdRange(start, end))

    food_ids_list = list(map(int, food_ids.split("\n")))

    return ranges, food_ids_list

# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[list[IdRange], list[int]]):
    fresh = 0
    for food_id in data[1]:
        if any([r.start <= food_id and r.end >= food_id for r in data[0]]):
            fresh += 1

    print(fresh)

def run_b(data: tuple[list[IdRange], list[int]]):
    ranges = []

    new_ranges = data[0]
    while len(new_ranges) != len(ranges):
        # print(f"{len(ranges)} - {len(new_ranges)}")

        ranges = new_ranges
        new_ranges = []
        merged_ids = set()
    
        for i in range(len(ranges)):
            for j in range(i + 1, len(ranges)):
                if i in merged_ids or j in merged_ids:
                    continue

                r1 = ranges[i]
                r2 = ranges[j]

                if r1.end >= r2.start and r2.end >= r1.start:
                    new_start = min(r1.start, r2.start)
                    new_end = max(r1.end, r2.end)
                    new_ranges.append(IdRange(new_start, new_end))
                    merged_ids.add(i)
                    merged_ids.add(j)
                    break

        new_ranges += [ranges[i] for i in range(len(ranges)) if i not in merged_ids]

    sum = 0
    for r in new_ranges:
        # print(r)
        sum += r.end - r.start + 1

    print(sum)

    