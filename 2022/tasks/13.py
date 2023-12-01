# //////////////////// PARSING /////////////////////////

from dataclasses import dataclass, field
from enum import Enum
from typing import Union

class NodeType(Enum):
    INT = 0
    LIST_BEGIN = 1
    LIST_END = 2

@dataclass
class LinkedNode:
    type: NodeType
    value: Union[int, None] = field(default=None)
    next: Union['LinkedNode', None] = field(default=None)

def parse_input(data: str) -> list[LinkedNode]:
    pairs = data.split("\n\n")

    result = []
    for pair in pairs:
        packets = pair.split("\n")
        result.append(parse_packet(packets[0]))
        result.append(parse_packet(packets[1]))

    return result

def parse_packet(data: str) -> LinkedNode:
    head = LinkedNode(NodeType.LIST_BEGIN)
    cur_node = head

    cur_token = ""
    for ch in data[1:]:
        if ch == "[":
            node = LinkedNode(NodeType.LIST_BEGIN)
            cur_node.next = node
            cur_node = node
        elif ch == "]":
            if cur_token != "":
                int_node = LinkedNode(NodeType.INT, int(cur_token))
                cur_token = ""
                cur_node.next = int_node
                cur_node = int_node
            node = LinkedNode(NodeType.LIST_END)
            cur_node.next = node
            cur_node = node
        elif ch == ",":
            if cur_token != "":
                node = LinkedNode(NodeType.INT, int(cur_token))
                cur_node.next = node
                cur_node = node
                cur_token = ""
        else:
            cur_token += ch
    
    return head

# //////////////////// PARTS /////////////////////////

def is_in_right_order(left: LinkedNode, right: LinkedNode) -> bool:
    # print(left, right)
    # print()
    if left.type == NodeType.INT and right.type == NodeType.INT:
        if left.value < right.value: return True
        elif left.value > right.value: return False
        else: return is_in_right_order(left.next, right.next)
    elif left.type == NodeType.LIST_BEGIN and right.type == NodeType.LIST_BEGIN:
        return is_in_right_order(left.next, right.next)
    elif left.type == NodeType.LIST_END and right.type == NodeType.LIST_END:
        if left.next is None: return True
        elif right.next is None: return False
        else: return is_in_right_order(left.next, right.next)
    else:
        if left.type == NodeType.LIST_END:
            return True
        elif right.type == NodeType.LIST_END:
            return False
        elif left.type == NodeType.LIST_BEGIN:
            ls_node = LinkedNode(NodeType.LIST_BEGIN)
            le_node = LinkedNode(NodeType.LIST_END)
            ls_node.next = right
            le_node.next = right.next
            right.next = le_node
            return is_in_right_order(left, ls_node)
        elif right.type == NodeType.LIST_BEGIN:
            ls_node = LinkedNode(NodeType.LIST_BEGIN)
            le_node = LinkedNode(NodeType.LIST_END)
            ls_node.next = left
            le_node.next = left.next
            left.next = le_node
            return is_in_right_order(ls_node, right)


    

def run_a(data: list[LinkedNode]):
    total = 0
    index = 1

    for i in range(0, len(data), 2):
        if is_in_right_order(data[i], data[i+1]):
            total += index
        index += 1
    
    print(f"Sum of correct indices: {total}")


def create_divider_packet(value: int) -> LinkedNode:
    data = f"[[{value}]]"
    return parse_packet(data)


def run_b(data: list[LinkedNode]):
    divider1 = create_divider_packet(2)
    divider2 = create_divider_packet(6)
    data.append(divider1)
    data.append(divider2)

    for _ in range(len(data)):
        changed = False
        for i in range(len(data)-1):
            if not is_in_right_order(data[i], data[i+1]):
                changed = True
                data[i], data[i+1] = data[i+1], data[i]
    
        if not changed:
            break
    
    index1 = data.index(divider1)+1
    index2 = data.index(divider2)+1

    print(f"Product of indices: {index1 * index2}")