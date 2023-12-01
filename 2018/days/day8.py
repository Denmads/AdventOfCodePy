from typing import List, Type
from DailyAssignment import DailyAssignment
from dataclasses import dataclass, field

@dataclass
class Node:
    metadata: List[int] = field(default_factory=list)
    children: List[Type["Node"]] = field(default_factory=list)

class NavigatingToThePole(DailyAssignment):
    def __init__(self):
        super().__init__(8)

    def run_part_a(self, input: str):
        tree_root = parse_tree(input)
        total = sum_metadata(tree_root)
        print(f"The sum of all metadata is '{total}'")

    def run_part_b(self, input: str):
        tree_root = parse_tree(input)
        total = advanced_sum(tree_root)
        print(f"The advanced sum is '{total}'")

def advanced_sum(node):
    total = 0
    if len(node.children) == 0:
        total = sum(node.metadata)
    else:
        for data in node.metadata:
            index = data-1
            if index < len(node.children):
                total += advanced_sum(node.children[index])
    return total

def sum_metadata(node):
    total = sum(node.metadata)
    for child in node.children:
        total += sum_metadata(child)
    return total

def parse_tree(input):
    numbers = list(map(lambda x: int(x), input.split(" ")))
    root, _ = parse_node(numbers)
    return root

def parse_node(numbers):
    node = Node()
    num_children = numbers[0]
    num_metadata = numbers[1]
    remaining_nums = numbers[2:]
    for _ in range(num_children):
        child, remaining = parse_node(remaining_nums)
        node.children.append(child)
        remaining_nums = remaining
    node.metadata = remaining_nums[:num_metadata]
    remaining_nums = remaining_nums[num_metadata:]

    return (node, remaining_nums)