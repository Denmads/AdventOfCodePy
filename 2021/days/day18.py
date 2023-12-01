from typing import Type
from DailyAssignment import DailyAssignment
from dataclasses import dataclass
import math

@dataclass
class Node:
    parent: Type["PairNode"]
    child_side: str

    def magnitude(self) -> int:
        ...

@dataclass
class ValueNode(Node):
    value: int

    def magnitude(self) -> int:
        return self.value

    def __repr__(self):
        return str(self.value)

@dataclass
class PairNode(Node):
    left: Node = None
    right: Node = None

    def copy(self, parent=None):
        node = PairNode(parent, self.child_side)
        node.left = ValueNode(node, "left", self.left.value) if isinstance(self.left, ValueNode) else self.left.copy(node)
        node.right = ValueNode(node, "right", self.right.value) if isinstance(self.right, ValueNode) else self.right.copy(node)
        return node

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def add(self, other) -> Type["PairNode"]:
        node = PairNode(None, None)
        node.left = self
        node.right = other

        self.parent = node
        self.child_side = "left"
        
        other.parent = node
        other.child_side = "right"
        
        node.reduce()
        return node

    def reduce(self):
        reduction_not_done = True
        while reduction_not_done:
            if self.do_explodes():
                continue
            if self.do_splits():
                continue
            reduction_not_done = False

    def get_depth(self):
        if self.parent is None:
            return 1
        return self.parent.get_depth() + 1

    def get_prev_leaf_node(self):
        if self.parent is None:
            return None
        return self.parent.get_prev_go_up(self.child_side)

    def get_prev_go_up(self, came_from):
        if came_from == "left":
            if self.parent is None:
                return None
            return self.parent.get_prev_go_up(self.child_side)
        else:
            if isinstance(self.left, ValueNode):
                return self.left
            return self.left.get_prev_go_down()
    
    def get_prev_go_down(self):
        if isinstance(self.right, ValueNode):
            return self.right
        else:
            return self.right.get_prev_go_down()

    def get_next_leaf_node(self):
        if self.parent is None:
            return None
        return self.parent.get_next_go_up(self.child_side)

    def get_next_go_up(self, came_from):
        if came_from == "right":
            if self.parent is None:
                return None
            return self.parent.get_next_go_up(self.child_side)
        else:
            if isinstance(self.right, ValueNode):
                return self.right
            return self.right.get_next_go_down()
    
    def get_next_go_down(self):
        if isinstance(self.left, ValueNode):
            return self.left
        else:
            return self.left.get_next_go_down()

    #True if a explosion happened
    def do_explodes(self) -> bool:
        if self.get_depth() == 5:
            prev_node = self.get_prev_leaf_node()
            next_node = self.get_next_leaf_node()

            if prev_node is not None:
                prev_node.value += self.left.value

            if next_node is not None:
                next_node.value += self.right.value

            new_node = ValueNode(self.parent, self.child_side, 0)
            if self.child_side == "left":
                self.parent.left = new_node
            if self.child_side == "right":
                self.parent.right = new_node
            return True

        if isinstance(self.left, PairNode):
            exploded = self.left.do_explodes()
            if exploded:
                return True

        if isinstance(self.right, PairNode):
            exploded = self.right.do_explodes()
            if exploded:
                return True
        return False

    #True if a split happened
    def do_splits(self) -> bool:
        if isinstance(self.left, ValueNode):
            if self.left.value >= 10:
                node = PairNode(self, "left")
                node.left = ValueNode(node, "left", math.floor(self.left.value / 2))
                node.right = ValueNode(node, "right", math.ceil(self.left.value / 2))
                self.left = node
                return True
        else:
            did_splits = self.left.do_splits()
            if did_splits:
                return True

        if isinstance(self.right, ValueNode):
            if self.right.value >= 10:
                node = PairNode(self, "right")
                node.left = ValueNode(node, "left", math.floor(self.right.value / 2))
                node.right = ValueNode(node, "right", math.ceil(self.right.value / 2))
                self.right = node
                return True
        else:
            did_splits = self.right.do_splits()
            if did_splits:
                return True
        return False
        
    def __repr__(self):
        return f"[{str(self.left)},{str(self.right)}]"


class SnailNumbers(DailyAssignment):
    def __init__(self):
        super().__init__(18)

    def run_part_a(self, input: str):
        numbers = parse_all_snail_numbers(input)
        result = numbers[0].copy()
        for number in numbers[1:]:
            result = result.add(number)
        print(result.magnitude())

    def run_part_b(self, input: str):
        numbers = parse_all_snail_numbers(input)
        max = 0
        for i in range(len(numbers)-1):
            for j in range(i+1, len(numbers)):
                res1 = numbers[i].copy().add(numbers[j].copy()).magnitude()
                if res1 > max:
                    max = res1
                res1 = numbers[j].copy().add(numbers[i].copy()).magnitude()
                if res1 > max:
                    max = res1
        print(max)

def parse_all_snail_numbers(input):
    lines = input.split("\n")
    numbers = [parse_node(l) for l in lines]
    return numbers

def find_split_index(input):
    stack = 0
    index = 0
    for ch in input:
        if ch == "," and stack == 0:
            return index+1
        elif ch == "[":
            stack += 1
        elif ch == "]":
            stack -= 1
        index += 1
    return -1

def parse_node(input, parent=None, side=None):
    node = PairNode(parent, side)
    split_point = find_split_index(input[1:-1])
    left = input[1:split_point]
    right = input[split_point+1:-1]
    node.left = ValueNode(parent, "left", int(left)) if "," not in left else parse_node(left, node, "left")
    node.right = ValueNode(parent, "right",int(right)) if "," not in right else parse_node(right, node, "right")
    return node
