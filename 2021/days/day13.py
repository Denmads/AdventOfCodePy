from typing import Dict, List, Tuple
from DailyAssignment import DailyAssignment
from dataclasses import dataclass, field

@dataclass
class FoldAction:
    fold_axis: str
    fold_index: int

@dataclass
class Paper:
    points: Dict[Tuple[int, int], int] = field(default_factory=dict)

    def add_point(self, x, y):
        self.points[(x, y)] = 1
    
    def do_fold(self, action: FoldAction):
        new_points = {}

        for p in self.points.keys():
            if (action.fold_axis == "x" and p[0] < action.fold_index) or (action.fold_axis == "y" and p[1] < action.fold_index):
                new_points[p] = 1
            else:
                diff_x =  p[0] - action.fold_index if action.fold_axis == "x" else 0
                diff_y =  p[1] - action.fold_index if action.fold_axis == "y" else 0
                new_p = (
                    p[0] - (diff_x * 2),
                    p[1] - (diff_y * 2)
                )
                new_points[new_p] = 1
        
        self.points = new_points
    
    def boundary(self):
        min_x = min(self.points.keys(), key=lambda x: x[0])
        min_y = min(self.points.keys(), key=lambda x: x[1])
        max_x = max(self.points.keys(), key=lambda x: x[0])
        max_y = max(self.points.keys(), key=lambda x: x[1])

        return ((min_x[0], min_y[1]), (max_x[0], max_y[1]))

    def print(self):
        min_coord, max_coord = self.boundary()
        print("-" * (max_coord[0] - min_coord[0]))
        for y in range(min_coord[1], max_coord[1]+1):
            line = ""
            for x in range(min_coord[0], max_coord[0]+1):
                line += "#" if (x, y) in self.points else " "
            print(line)
        print("-" * (max_coord[0] - min_coord[0]))

class FoldingPaper(DailyAssignment):
    def __init__(self):
        super().__init__(13)

    def run_part_a(self, input: str):
        paper, folds = parse_paper_and_folds(input)
        paper.do_fold(folds[0])

        print(len(paper.points.keys()))

    def run_part_b(self, input: str):
        paper, folds = parse_paper_and_folds(input)
        for fold in folds:
            paper.do_fold(fold)
        paper.print()

def parse_paper_and_folds(input):
    paper = Paper()
    folds = []

    sections = input.split("\n\n")
    for line in sections[0].split("\n"):
        point = line.split(",")
        paper.add_point(int(point[0]), int(point[1]))
    
    for line in sections[1].split("\n"):
        info = line.split(" ")[2]
        parts = info.split("=")
        folds.append(FoldAction(parts[0], int(parts[1])))

    return (paper, folds)