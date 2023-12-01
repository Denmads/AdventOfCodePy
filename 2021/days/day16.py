from typing import List, Type
from DailyAssignment import DailyAssignment
from bitstring import ConstBitStream
from dataclasses import dataclass, field

@dataclass
class Node:
    version: int
    operator_type: int
    bit_length: int = 0

    #return bits parsed
    def parse(self, stream: ConstBitStream):
        ...

    def get_result(self) -> int:
        ...

# 3 bit version
# 3 bit type id (always 4)
# sets of 5 bits 
#   1 bit - tells if it is the last set (is 0 if it is the last)
#   bit 2-5 - concatenated from all sets make up the value
@dataclass
class ValueNode(Node):
    value: int = 0

    def parse(self, stream: ConstBitStream):
        next_set = stream.read("bin:5")
        bit_count = 11 # 6 for header + 5 for first set
        val_str = ""
        while next_set[0] != "0":
            val_str += next_set[1:]
            next_set = stream.read("bin:5")
            bit_count += 5
        val_str += next_set[1:]
        self.value = int(val_str, 2)
        self.bit_length = bit_count
    
    def get_result(self) -> int:
        return self.value

# 3 bit version
# 3 bit type id
# 1 bit length type - 0 = 15 bits (total length in bits) / 1 = 11 bits (number of subpakcets)
# subpackets according to length type
@dataclass
class OperatorNode(Node):
    sub_nodes: List[Type["OperatorNode"]] = field(default_factory=list)

    def parse(self, stream: ConstBitStream):
        length_type = stream.read("bin:1")
        bit_count = 7 # header + length type
        if length_type == "0":
            num_bits = int(stream.read("bin:15"), 2)
            bit_count += 15
            parsed_bits = 0
            while parsed_bits < num_bits:
                node = parse_next_node(stream)
                self.sub_nodes.append(node)
                parsed_bits += node.bit_length
                bit_count += node.bit_length
        else:
            num_packets = int(stream.read("bin:11"), 2)
            bit_count += 11
            for i in range(num_packets):
                node = parse_next_node(stream)
                self.sub_nodes.append(node)
                bit_count += node.bit_length
        self.bit_length = bit_count
    
    def get_result(self) -> int:
        if self.operator_type == 0: # sum
            return sum(list(map(lambda x: x.get_result(), self.sub_nodes)))
        elif self.operator_type == 1: # product
            results = list(map(lambda x: x.get_result(), self.sub_nodes))
            total = 1
            for res in results:
                total *= res
            return total
        elif self.operator_type == 2: # minimum
            return min(list(map(lambda x: x.get_result(), self.sub_nodes)))
        elif self.operator_type == 3: # maximum
            return max(list(map(lambda x: x.get_result(), self.sub_nodes)))
        elif self.operator_type == 5: # greater than - [0] > [1] = 1 else 0
            return 1 if self.sub_nodes[0].get_result() > self.sub_nodes[1].get_result() else 0
        elif self.operator_type == 6: # less than - [0] < [1] = 1 else 0
            return 1 if self.sub_nodes[0].get_result() < self.sub_nodes[1].get_result() else 0
        elif self.operator_type == 7: # equal to - [0] == [1] = 1 else 0
            return 1 if self.sub_nodes[0].get_result() == self.sub_nodes[1].get_result() else 0

class BitsTransmission(DailyAssignment):
    def __init__(self):
        super().__init__(16)

    def run_part_a(self, input: str):
        root = parse_bits_tree(input)
        total = sum_version(root)
        print(total)

    def run_part_b(self, input: str):
        root = parse_bits_tree(input)
        print(root.get_result())

def sum_version(node: Node):
    if isinstance(node, ValueNode):
        return node.version
    else:
        total = node.version
        for n in node.sub_nodes:
            total += sum_version(n)
        return total

# first packet has 0 padding at the end, should be ignored
def parse_bits_tree(input):
    stream = ConstBitStream(hex="0x" + input)
    return parse_next_node(stream)
    
    
def parse_next_node(stream):
    version = int(stream.read("bin:3"), 2)
    operator = int(stream.read("bin:3"), 2)
    if operator == 4:
        node = ValueNode(version, operator)
        node.parse(stream)
    else:
        
        node = OperatorNode(version, operator)
        node.parse(stream)
    return node