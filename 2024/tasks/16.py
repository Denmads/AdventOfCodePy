from dataclasses import dataclass
from enum import Enum
from math import sqrt
import time
from typing import Any, Callable

from utils.graph import Graph, GraphNode
from utils.vector import Vector2i

# //////////////////// PARSING & TYPES /////////////////////////

class TileType(Enum):
    OPEN = 1,
    WALL = 2

class Direction(Enum):
    NORTH = "^"
    SOUTH = "v"
    WEST = "<"
    EAST = ">"

def parse_input(data: str, part: str) -> tuple[dict[Vector2i, TileType], Vector2i, Vector2i, int, int]:
    maze: dict[Vector2i, TileType] = {}
    start_pos: Vector2i
    end_pos: Vector2i
    
    width = len(data.split("\n")[0])
    height = len(data.split("\n"))
    
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(list(line)):
            if char == "S":
                start_pos = Vector2i(x, y)
                maze[start_pos] = TileType.OPEN
            elif char == "E":
                end_pos = Vector2i(x, y)
                maze[end_pos] = TileType.OPEN
            elif char == "#":
                maze[Vector2i(x, y)] = TileType.WALL
            else:
                maze[Vector2i(x, y)] = TileType.OPEN
                
    return (maze, start_pos, end_pos, width, height)

# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[dict[Vector2i, TileType], Vector2i, Vector2i, int, int]):
    maze, start, end, width, height = data
                
    graph, start_node, end_node = get_maze_graph(maze, start, end)
    
    def h(a: GraphNode, b: GraphNode) -> float:
        x_diff = a.value.x - b.value.x
        y_diff = a.value.y - b.value.y
        
        return sqrt(x_diff*x_diff + y_diff*y_diff) 
    
    # path = astar(graph, start_node, end_node, h, True )
    path = djikstra(graph, start_node, end_node)
    
    revised_path = [path[0]]
    for i in range(1, len(path)-1):
        prev = path[i-1]
        curr = path[i]
        next = path[i+1]
    
        if prev.value.x == curr.value.x == next.value.x or prev.value.y == curr.value.y == next.value.y:
            continue
        
        revised_path.append(curr)
        
    revised_path.append(path[-1])
    
    # for n in revised_path:
    #     print(n.value)
    
    turns = len(revised_path[1:-1])
    if revised_path[0].value.y == revised_path[1].value.y and revised_path[1].value.x - revised_path[0].value.x > 0:
        pass
    else:
        turns += 1
    
    steps = 0
    for i in range(len(path)-1):
        curr = path[i]
        next = path[i+1]
        
        s = abs(curr.value.x - next.value.x) + abs(curr.value.y - next.value.y)
        steps += s
    
    score = turns * 1000 + steps
    print(f"Score: {score}")

def run_b(data: tuple[dict[Vector2i, TileType], Vector2i, Vector2i, int, int]):
    pass


def get_maze_graph(maze: dict[Vector2i, TileType], start: Vector2i, end: Vector2i) -> tuple[Graph, GraphNode, GraphNode]:
    graph = Graph()
    
    def find_directions(pos: Vector2i) -> list[tuple[Vector2i, Vector2i]]:
        open_dir = []
        for dir in [(-1, 0),(1, 0),(0, -1),(0, 1)]:
            neighbor = Vector2i(pos.x + dir[0], pos.y + dir[1])
            
            if neighbor in maze and maze[neighbor] == TileType.OPEN:
                open_dir.append((pos, dir))
                
        return open_dir
    
    def is_split_point(pos: Vector2i) -> bool:
        open_dir = []
        for dir in [(-1, 0),(1, 0),(0, -1),(0, 1)]:
            neighbor = Vector2i(pos.x + dir[0], pos.y + dir[1])
            
            if neighbor in maze and maze[neighbor] == TileType.OPEN:
                open_dir.append(neighbor)
                
        if len(open_dir) == 2:
            n1, n2 = open_dir
            if n1.x != n2.x and n1.y != n2.y:
                return True
        elif len(open_dir) in [1, 3, 4]:
            return True
            
        return False
    
    def get_id(pos: Vector2i) -> str:
        return f"{pos.x},{pos.y}"
    
    nodes = {
        start: GraphNode(get_id(start), start)
    }
    graph.add_node(nodes[start])
    lines = find_directions(start)
    
    while len(lines) > 0:
        pos, dir = lines.pop(0)
        new_pos = pos.copy()
        new_pos += dir
        
        steps = 1
        while not is_split_point(new_pos):
            new_pos += dir
            steps += 1
        
        node = None
        if new_pos not in nodes:
            node = GraphNode(get_id(new_pos), new_pos)
            nodes[new_pos] = node
            graph.add_node(node)
            
            new_lines = find_directions(new_pos)
            for l in new_lines:
                _, l_dir = l
                if l_dir[0] + dir[0] != 0 or l_dir[1] + dir[1] != 0:
                    lines.append(l)
        else:
            node = nodes[new_pos]
        
        graph.add_connection(nodes[pos], node, steps, False)
        
    return graph, nodes[start], nodes[end]
        
        
        
        
# ////////////////////// ASTAR ////////////////////////////
class AStarNodeInfo:
    def __init__(self, node):
        self.g_score = 999999999999
        self.f_score = 999999999999
        self.previous_node = None
        self.node = node

    def __str__(self):
        return f"Dist: {self.distance_from_source}, Prev: {self.previous_node.node.id if self.previous_node else 'NONE'}"

def astar(graph: Graph, start: GraphNode, end: GraphNode, heuristic: Callable[[GraphNode, GraphNode], float], weighted: bool = False) -> list[GraphNode]:
    node_info: dict[str, AStarNodeInfo] = {k: AStarNodeInfo(n) for k, n in graph.nodes.items()}

    open_set: dict[str: AStarNodeInfo] = {}
    open_set[start.id] = node_info[start.id]

    node_info[start.id].g_score = 0
    node_info[start.id].f_score = node_info[start.id].g_score + heuristic(start, end)

    while len(open_set.keys()) > 0:
        current = find_node_with_min_fscore(open_set)

        if current.node == end:
            return construct_path(current)

        del open_set[current.node.id]

        connections = graph.get_connections_from(current.node)
        for conn in connections:
            neigh_info = node_info[conn[0]]
            weight = 1 if not weighted else conn[1]
            
            prev_v: Vector2i = current.previous_node.node.value if current.previous_node is not None else None
            curr_v: Vector2i = current.node.value
            next_v: Vector2i = neigh_info.node.value
            
                
            
            is_turn =  prev_v is not None and not (prev_v.x == curr_v.x == next_v.x or prev_v.y == curr_v.y == next_v.y)
            
            g_score = current.g_score+weight
            if prev_v == next_v:
                continue
            if is_turn:
                g_score += 1000

            if g_score < neigh_info.g_score:
                neigh_info.previous_node = current
                neigh_info.g_score = g_score
                neigh_info.f_score = g_score + heuristic(neigh_info.node, end)

                if neigh_info.node.id not in open_set:
                    open_set[neigh_info.node.id] = neigh_info
    return []

def construct_path(end: AStarNodeInfo) -> list[GraphNode]:
    path: list[GraphNode] = []
    print(end.g_score)
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
    nodes_done: set[NodeInfo] = set()

    node_info[start.id].distance_from_source = 0

    while len(nodes_done) != len(graph.nodes):
        start = time.perf_counter()
        node = find_node_with_min_dist(node_info, nodes_done)
        print(time.perf_counter() - start)
        nodes_done.add(node.node.id)
        print(f"Done {len(nodes_done)}/{len(graph.nodes)}")

        connections = graph.get_connections_from(node.node)
        for conn in connections:
            neigh_info = node_info[conn[0]]
            
            weight = conn[1]
            
            prev_v: Vector2i = node.previous_node.node.value if node.previous_node is not None else None
            curr_v: Vector2i = node.node.value
            next_v: Vector2i = neigh_info.node.value
            
            is_turn =  prev_v is not None and not (prev_v.x == curr_v.x == next_v.x or prev_v.y == curr_v.y == next_v.y)
            
            if prev_v == next_v:
                continue
            if is_turn:
                weight += 1000
            
            if neigh_info.distance_from_source > node.distance_from_source+weight:
                neigh_info.distance_from_source = node.distance_from_source+weight
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

def find_node_with_min_dist(node_info: dict[str, NodeInfo], node_done: set[str]):
    nodes = sorted(node_info.values(), key=lambda nf: nf.distance_from_source)

    for n in nodes:
        if n.node.id not in node_done:
            return n