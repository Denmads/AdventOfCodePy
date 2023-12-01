from utils.graph import Graph, GraphNode
from utils.graphutils import astar

START_NODE = None
END_NODE = None

A_SQUARES = []

# //////////////////// PARSING /////////////////////////

def parse_nodes(grid: list[list[str]]) -> Graph:
    global START_NODE, END_NODE
    graph = Graph()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            value = {
                "val": grid[y][x],
                "x": x,
                "y": y
            }
            node = GraphNode(f"{x}-{y}", value)
            if grid[y][x] == "S":
                START_NODE = node
                A_SQUARES.append(node)
            elif grid[y][x] == "E":
                END_NODE = node
            elif grid[y][x] == "a":
                A_SQUARES.append(node)
            graph.add_node(node)
    return graph

def parse_connections(grid: list[list[str]], graph: Graph):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            check_connection(grid, graph, (x, y), (x, y-1))
            check_connection(grid, graph, (x, y), (x, y+1))
            check_connection(grid, graph, (x, y), (x-1, y))
            check_connection(grid, graph, (x, y), (x+1, y))

def check_connection(grid: list[list[str]], graph: Graph, point1: tuple[int, int], point2: tuple[int, int]):
    if point2[0] < 0 or point2[0] >= len(grid[0]) or point2[1] < 0 or point2[1] >= len(grid):
        return
    
    val1 = grid[point1[1]][point1[0]]
    if val1 == "S":
        val1 = "a"
    elif val1 == "E":
        val1 = "æ"

    val2 = grid[point2[1]][point2[0]]
    if val2 == "S":
        val2 = "æ"
    elif val2 == "E":
        val2 = "z"

    diff = ord(val2)-ord(val1)
    if  diff <= 1:
        graph.add_connection(f"{point1[0]}-{point1[1]}", f"{point2[0]}-{point2[1]}")

def parse_input(data: str) -> Graph:
    lines = data.split("\n")
    grid = list(map(lambda l: list(l), lines))

    graph = parse_nodes(grid)
    parse_connections(grid, graph)
    
    return graph

# //////////////////// PARTS /////////////////////////

def run_a(data: Graph):
    def h(n: GraphNode, g: GraphNode) -> float:
        return (n.value["x"] - g.value["x"])**2 + (n.value["y"] - g.value["y"])**2

    path = astar(data, START_NODE, END_NODE, h)
    print(f"Steps: {len(path)-1}")

def run_b(data: Graph):
    def h(n: GraphNode, g: GraphNode) -> float:
        return (n.value["x"] - g.value["x"])**2 + (n.value["y"] - g.value["y"])**2

    best = 99999999
    for start in A_SQUARES:
        path = astar(data, start, END_NODE, h)
        if len(path) != 0 and len(path)-1 < best:
            best = len(path)-1

    print(f"Best Path: {best}")