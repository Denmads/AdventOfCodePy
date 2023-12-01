from typing import List
from DailyAssignment import DailyAssignment
from dataclasses import dataclass

class SubmarinePilot(DailyAssignment):
    def __init__(self):
        super().__init__(2)

    def run_part_a(self, input: str):
        moves = parse_input(input)
        position = Position()
        [position.do_move(mv) for mv in moves]
        print(f"After all movements have been made the position is 'Hor: {position.hor} | Dep: {position.dep}'")
        print(f"The product of the position is '{position.hor * position.dep}'")

    def run_part_b(self, input: str):
        moves = parse_input(input)
        position = AdvancedPosition()
        [position.do_move(mv) for mv in moves]
        print(f"After all movements have been made the position is 'Hor: {position.hor} | Dep: {position.dep}'")
        print(f"The product of the position is '{position.hor * position.dep}'")

@dataclass
class Move:
    direction: str
    amount: int

@dataclass
class Position:
    hor: int = 0
    dep: int = 0

    def do_move(self, move: Move):
        if move.direction == "f":
            self.hor += move.amount
        elif move.direction == "d":
            self.dep += move.amount
        elif move.direction == "u":
            self.dep -= move.amount

@dataclass
class AdvancedPosition:
    hor: int = 0
    dep: int = 0
    aim: int = 0

    def do_move(self, move: Move):
        if move.direction == "f":
            self.hor += move.amount
            self.dep += self.aim * move.amount
        elif move.direction == "d":
            self.aim += move.amount
        elif move.direction == "u":
            self.aim -= move.amount


def parse_input(input: str) -> List[Move]:
    moves = [line.split(" ") for line in input.split("\n")]
    return list(map(lambda move: Move(move[0][0], int(move[1])), moves))