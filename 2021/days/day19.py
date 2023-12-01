from typing import List, Tuple
from DailyAssignment import DailyAssignment
from dataclasses import dataclass, field

@dataclass
class Scanner:
    points: List[Tuple[int, int, int]] = field(default_factory=list)

    def add_point(self, point):
        self.points.append(point)

    def find_overlapping_points(self, other):
        diffs = {}
        for mp in self.points:
            for op in other.points:
                diff = (
                    abs(abs(mp[0]) - abs(op[0])),
                    abs(abs(mp[1]) - abs(op[1])),
                    abs(abs(mp[2]) - abs(op[2]))
                )

                if diff not in diffs:
                    diffs[diff] = []
                diffs[diff].append([
                    mp, op
                ])
        
        for k, v in diffs.items():
            if k[0] == 68:
                print(k)
            if len(v) >= 12:
                return (k, v)
        return None

class ScannersAndBeacons(DailyAssignment):
    def __init__(self):
        super().__init__(19)

    def run_part_a(self, input: str):
        scanners = parse_scanners(input)
        print(scanners[0].find_overlapping_points(scanners[1]))

    def run_part_b(self, input: str):
        ...

def parse_scanners(input):
    sections = input.split('\n\n')

    scanners = []
    for section in sections:
        scanner = Scanner()
        for point in section.split("\n")[1:]:
            vals = tuple(map(int, point.split(",")))
            scanner.add_point(vals)
        scanners.append(scanner)
    return scanners
