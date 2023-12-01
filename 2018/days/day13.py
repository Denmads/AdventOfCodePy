from typing import List
from DailyAssignment import DailyAssignment
from dataclasses import dataclass

@dataclass
class Minecart():
    position: List[int]
    dir: str
    intersection_index: int = 0
    intersection_turns = ["left", "straight", "right"]

    def update(tracks):
        ...
    
    def intersection_turns(self):
        ...

class CartsAndTracks(DailyAssignment):
    def __init__(self):
        super().__init__(13)

    def run_part_a(self, input: str):
        tracks, carts = parse_tracks_and_carts(input)
        while not is_crashed(carts):
            for c in carts:
                c.update(tracks)
            carts.sort(key=lambda x: (x.position[1], x.position[0]))

    def run_part_b(self, input: str):
        ...

def is_crashed(carts):
    ...

def parse_tracks_and_carts(input):
    tracks = list(map(lambda x: list(x) , input.split('\n')))
    carts = []

    for y in range(len(tracks[0])):
        for x in range(len(tracks)):
            tile = tracks[x][y]
            if tile == "<":
                carts.append(
                    Minecart([x, y], "left")
                )
                tracks[x][y] = "-"
            elif tile == ">":
                carts.append(
                    Minecart([x, y], "right")
                )
                tracks[x][y] = "-"
            elif tile == "v":
                carts.append(
                    Minecart([x, y], "down")
                )
                tracks[x][y] = "|"
            elif tile == "^":
                carts.append(
                    Minecart([x, y], "up")
                )
                tracks[x][y] = "|"
    return (tracks, carts)