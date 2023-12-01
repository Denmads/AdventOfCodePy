from DailyAssignment import DailyAssignment

class Node:
    def __init__(self, name, traverse_once):
        self.name = name
        self.traverse_once = traverse_once
        self.connections = []

    def add_connection(self, node):
        self.connections.append(node)

    def dfs_all_paths_to(self, name, current_path=[]):
        completed_paths = []
        for node in self.connections:
            if node.name == name:
                completed_paths.append(tuple(current_path + [self.name, node.name]))
            elif not node.traverse_once or node.name not in current_path:
                paths = node.dfs_all_paths_to(name, current_path + [self.name])
                for p in paths:
                    completed_paths.append(p)
        return completed_paths

    def advanced_dfs_all_paths_to(self, name, current_path=[], twice_node=None):
        completed_paths = []
        for node in self.connections:
            if node.name == name:
                completed_paths.append(tuple(current_path + [self.name, node.name]))
            elif not node.traverse_once or node.name not in current_path or (twice_node == node.name and current_path.count(node.name) < 2):
                paths = node.advanced_dfs_all_paths_to(name, current_path + [self.name], twice_node)
                for p in paths:
                    completed_paths.append(p)
                if twice_node is None and self.name != "start" and self.traverse_once:
                    double_paths = node.advanced_dfs_all_paths_to(name, current_path + [self.name], self.name)
                    for p in double_paths:
                        completed_paths.append(p)
        return completed_paths

class CaveSystems(DailyAssignment):
    def __init__(self):
        super().__init__(12)

    def run_part_a(self, input: str):
        nodes = parse_graph(input)
        start_to_end = nodes["start"].dfs_all_paths_to("end")
        unique = set(start_to_end)
        print(len(unique))

    def run_part_b(self, input: str):
        nodes = parse_graph(input)
        start_to_end = nodes["start"].advanced_dfs_all_paths_to("end")
        unique = set(start_to_end)
        print(len(unique))

def parse_graph(input):
    nodes = {}
    for line in input.split("\n"):
        points = line.split("-")
        if points[0] not in nodes:
            nodes[points[0]] = Node(points[0], points[0].islower())
        if points[1] not in nodes:
            nodes[points[1]] = Node(points[1], points[1].islower())
        nodes[points[0]].add_connection(nodes[points[1]])
        nodes[points[1]].add_connection(nodes[points[0]])
    return nodes
        