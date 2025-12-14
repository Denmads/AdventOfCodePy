from dataclasses import dataclass, field
import math
import sys
import time
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class JunctionBox:
    x: int
    y: int
    z: int

    circuit: set[int]

    def sqr_dist(self, other: "JunctionBox"):
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2

def parse_input(data: str, part: str) -> list[JunctionBox]:
    lines = data.split("\n")

    boxes = []
    for i, line in enumerate(lines):
        x, y, z = line.split(",")
        boxes.append(JunctionBox(int(x), int(y), int(z), set([i])))

    return boxes

# //////////////////// PARTS /////////////////////////

def run_a(data: list[JunctionBox]):
    dists = []

    for idx_a in range(len(data)):
        for idx_b in range(idx_a+1, len(data)):

            box_a = data[idx_a]
            box_b = data[idx_b]

            dist = box_a.sqr_dist(box_b)
            dists.append((dist, (idx_a, idx_b)))

    dists.sort(key= lambda x: x[0])

    for i in range(1000):
        dist, pair = dists[i]

        box_a: JunctionBox = data[pair[0]]
        box_b: JunctionBox = data[pair[1]]

        if box_a.circuit != box_b.circuit:
            box_a.circuit.update(box_b.circuit)
            for idx in box_b.circuit:
                data[idx].circuit = box_a.circuit

    all_circuits = list(set([tuple(box.circuit) for box in data]))
    all_circuits.sort(key=lambda c: len(c))

    print()
    print(math.prod(map(lambda c: len(c), all_circuits[-3:])))
    
                

def run_b(data: list[JunctionBox]):
    dists = []

    for idx_a in range(len(data)):
        for idx_b in range(idx_a+1, len(data)):

            box_a = data[idx_a]
            box_b = data[idx_b]

            dist = box_a.sqr_dist(box_b)
            dists.append((dist, (idx_a, idx_b)))


    dists.sort(key= lambda x: x[0])

    num_circuits = 1000
    conn_idx = -1
    while num_circuits > 1:
        conn_idx += 1
        dist, pair = dists[conn_idx]

        box_a: JunctionBox = data[pair[0]]
        box_b: JunctionBox = data[pair[1]]

        if box_a.circuit != box_b.circuit:
            # print(f"{dist} | {box_a.x},{box_a.y},{box_a.z} ({pair[0]}) | {box_b.x},{box_b.y},{box_b.z} ({pair[1]})")
            box_a.circuit.update(box_b.circuit)
            for idx in box_b.circuit:
                data[idx].circuit = box_a.circuit

        new_num_circuits = len(set([tuple(box.circuit) for box in data]))
        if new_num_circuits != num_circuits:
            print(f"Num Circuits: {new_num_circuits}")
            
            # if new_num_circuits < 5:
            all_circuits = list(set([tuple(box.circuit) for box in data]))
            all_circuits.sort(key=lambda c: len(c))

            # print("Circuits")
            # for c in all_circuits:
            #     print(f"{len(c)} - {c}")
        num_circuits = new_num_circuits

    dist, pair = dists[conn_idx]

    box_a: JunctionBox = data[pair[0]]
    box_b: JunctionBox = data[pair[1]]

    print(f"{box_a.x},{box_a.y},{box_a.z} | {box_b.x},{box_b.y},{box_b.z}")

    print(f"X-Mul: {box_a.x * box_b.x}")