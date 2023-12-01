from typing import Callable
from utils.graph import Graph, GraphNode



# ////////////////////// ASTAR ////////////////////////////
class AStarNodeInfo:
    def __init__(self, node):
        self.g_score = 999999999999
        self.f_score = 999999999999
        self.previous_node = None
        self.node = node

    def __str__(self):
        return f"Dist: {self.distance_from_source}, Prev: {self.previous_node.node.id if self.previous_node else 'NONE'}"

def astar(graph: Graph, start: GraphNode, end: GraphNode, heuristic: Callable[[GraphNode, GraphNode], float]) -> list[GraphNode]:
    node_info: dict[str, AStarNodeInfo] = {k: AStarNodeInfo(n) for k, n in graph.nodes.items()}

    open_set: dict[str: AStarNodeInfo] = {}
    open_set[start.id] = node_info[start.id]

    node_info[start.id].g_score = 0
    node_info[start.id].f_score = node_info[start.id].g_score + heuristic(start, end)

    while len(open_set.keys()) > 0:
        current = find_node_with_min_fscore(open_set)
        # print(current.node.value["val"], current.node.id)

        if current.node == end:
            return construct_path(current)

        del open_set[current.node.id]

        connections = graph.get_connections_from(current.node)
        for conn in connections:
            neigh_info = node_info[conn]
            g_score = current.g_score+1

            if g_score < neigh_info.g_score:
                neigh_info.previous_node = current
                neigh_info.g_score = g_score
                neigh_info.f_score = g_score + heuristic(neigh_info.node, end)

                if neigh_info.node.id not in open_set:
                    open_set[neigh_info.node.id] = neigh_info
    return []

def construct_path(end: AStarNodeInfo) -> list[GraphNode]:
    path: list[GraphNode] = []
    cur = end
    while cur is not None:
        path.append(cur.node)
        cur = cur.previous_node
    
    path.reverse()
    return path

def find_node_with_min_fscore(node_info: dict[str, AStarNodeInfo]) -> AStarNodeInfo:
    nodes = sorted(node_info.values(), key=lambda nf: nf.f_score)
    return nodes[0]




# ////////////////////// DJIKSTRA /////////////////////////
class NodeInfo:
    def __init__(self, node):
        self.distance_from_source = 9999999999999
        self.previous_node = None
        self.node = node

    def __str__(self):
        return f"Dist: {self.distance_from_source}, Prev: {self.previous_node.node.id if self.previous_node else 'NONE'}"

def djikstra(graph: Graph, start: GraphNode, end: GraphNode) -> list[GraphNode]:
    node_info: dict[str, NodeInfo] = {k: NodeInfo(n) for k, n in graph.nodes.items()}
    nodes_done: list[NodeInfo] = []

    node_info[start.id].distance_from_source = 0

    while len(nodes_done) != len(graph.nodes):
        node = find_node_with_min_dist(node_info, nodes_done)
        nodes_done.append(node)

        connections = graph.get_connections_from(node.node)
        for conn in connections:
            neigh_info = node_info[conn]
            if neigh_info.distance_from_source > node.distance_from_source+1:
                neigh_info.distance_from_source = node.distance_from_source+1
                neigh_info.previous_node = node
    
    # for k, v in node_info.items():
    #     print(f"{k} - {v}")


    path: list[GraphNode] = []
    cur = node_info[end.id]
    while cur is not None:
        path.append(cur.node)
        cur = cur.previous_node
    
    path.reverse()
    return path

def find_node_with_min_dist(node_info: dict[str, NodeInfo], node_done: list[NodeInfo]):
    nodes = sorted(node_info.values(), key=lambda nf: nf.distance_from_source)

    for n in nodes:
        if n.node.id not in map(lambda nf: nf.node.id, node_done):
            return n