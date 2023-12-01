
from dataclasses import dataclass


@dataclass
class Range:
    min: int
    max: int
    
    def contains(self, other: 'Range') -> bool:
        return self.min <= other.min and other.max <= self.max
    
    def overlaps(self, other: 'Range') -> bool:
        return (self.min <= other.min and other.min <= self.max) or \
                (other.min <= self.min and self.min <= other.max)

RangePair = tuple[Range, Range]

def parse_range(data: str) -> Range:
    bounds = list(map(
        lambda b: int(b), data.split('-')
    ))
    return Range(min=bounds[0], max=bounds[1])

def parse_input(data: str) -> list[RangePair]:
    return list(map(
        lambda l: tuple(map(
            lambda r: parse_range(r),
            l.split(',')
        )), 
        data.split("\n")
    ))
    

def run_a(data: list[RangePair]):
    total = 0
    for r1, r2 in data:
        if r1.contains(r2) or r2.contains(r1): total += 1
    print(f"Total pairs with one assignment fully contained: {total}")

def run_b(data: list[RangePair]):
    total = 0
    for r1, r2 in data:
        if r1.overlaps(r2): total += 1
    print(f"Total pairs with overlap: {total}")