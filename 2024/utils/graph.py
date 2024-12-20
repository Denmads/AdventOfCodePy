
from dataclasses import dataclass
from typing import Generic, Type, TypeVar, Union


T = TypeVar("T")

@dataclass
class GraphNode(Generic[T]):
    id: str
    value: T


class Graph:

    def __init__(self):
        self.nodes: dict[str, GraphNode] = {}
        self.connections_from: dict[str, set[tuple[str, int]]] = {}

    def add_node(self, node: GraphNode):
        self.nodes[node.id] = node
        self.connections_from[node.id] = set()

    def add_connection(self, node_from: Union[GraphNode, str], node_to: Union[GraphNode, str], weight: int = 1, bi_directional: bool = False):
        id_from = node_from.id if type(node_from) == GraphNode else node_from
        id_to = node_to.id if type(node_to) == GraphNode else node_to

        self.connections_from[id_from].add((id_to, weight))
        if bi_directional:
            self.connections_from[id_to].add((id_from, weight))
    
    def get_node(self, id: str):
        return self.nodes[id]

    def get_connections_from(self, node: Union[GraphNode, str]):
        id = node.id if type(node) == GraphNode else node
        return self.connections_from[id]

    def print(self):
        for k, v in self.connections_from.items():
            print(f"'{k}' -> {v}")