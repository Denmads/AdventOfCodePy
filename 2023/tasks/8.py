from dataclasses import dataclass
import dataclasses
import json
import math
import os
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Node:
    node: str
    num_steps: int # number of steps from previous to reach this

NodeDict = dict[str, tuple[str, str]]

def parse_input(data: str, part: str) -> tuple[list[str], NodeDict]:
    (dirs, nodes_lines) = data.split('\n\n')

    directions = list(dirs)

    nodes = {}
    for node_str in nodes_lines.split('\n'):
        [node, conn_str] = node_str[:-1].split(' = (')

        connections = conn_str.split(', ')

        nodes[node] = (connections[0], connections[1])

    return (directions, nodes)


# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[list[str], NodeDict]):
    (directions, nodes) = data

    current_node = 'AAA'
    dir_index = 0

    steps = 0

    while current_node != 'ZZZ':
        dir = 0 if directions[dir_index] == 'L' else 1
        current_node = nodes[current_node][dir]
        steps += 1

        dir_index = (dir_index + 1) % len(directions)

    print(steps)


# Key - dir_index
StepDict = dict[int, Node]

def run_b(data: tuple[list[str], NodeDict]):
    (directions, nodes) = data
    
    start_nodes = list(filter(lambda n: n[-1] == 'A', nodes.keys()))
    steps_count = list(map(lambda s: get_steps_to_end_node(s, nodes, directions), start_nodes))
    
    ans = 1
    for i in steps_count: 
        ans = int((ans * i)/math.gcd(ans, i))         
    print(ans)
    

def get_steps_to_end_node(node: str, nodes: NodeDict, directions: list[str]) -> int:
    current_node = node
    dir_index = 0
    steps = 0
    
    while current_node[-1] != 'Z':
            dir = 0 if directions[dir_index] == 'L' else 1
            current_node = nodes[current_node][dir]
            steps += 1

            dir_index = (dir_index + 1) % len(directions)
            
    return steps