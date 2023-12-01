from dataclasses import dataclass
from typing import Type, Union


@dataclass
class File:
    name: str
    size: int


class Directory:
    def __init__(self, name: str, parent: Union['Directory', None]):
        self.name = name
        self.parent = parent
        self.size: int = 0
        self.contents: dict[str, Union[File, 'Directory']] = {}
    
    def calculate_total_sizes(self) -> int:
        total = 0
        for _, c in self.contents.items():
            if type(c) == File:
                total += c.size
            elif type(c) == Directory:
                c.calculate_total_sizes()
                total += c.size
        self.size = total
    
    def get_nested_contents_of_type(self, content_type: Type, content_list: list = None):
        if content_list is None:
            content_list = []
        
        for _, v in self.contents.items():
            if type(v) == content_type:
                content_list.append(v)
                
            if type(v) == Directory:
                v.get_nested_contents_of_type(content_type, content_list)
        
        return content_list
    
    def print_structure(self, level: int = 0):
        tab = "  "
        print(f"{tab*level}- {self.name} (dir)")
        
        for name, val in self.contents.items():
            if type(val) == Directory:
                val.print_structure(level+1)
            else:
                print(f"{tab*(level+1)}- {val.name} (file, size={val.size})")

# //////////////////// PARSING /////////////////////////

def parse_dir_contents(directory: Directory, lines: list[str], line_index: int) -> int:
    index = line_index
    currentLine = lines[index]
    
    # dir e
    # 29116 f
    while not currentLine.startswith("$"):
        tokens = currentLine.split()
        if tokens[0].startswith("dir"):
            dir = Directory(tokens[1], directory)
            directory.contents[tokens[1]] = dir
        else:
            file = File(tokens[1], int(tokens[0]))
            directory.contents[tokens[1]] = file
        
        index += 1
        if index >= len(lines): break
        currentLine = lines[index]
        
    return index
        

def parse_input(data: str) -> Directory:
    lines = data.split("\n")[1:]
    root = Directory("/", None)
    currentDir = root
    
    line_index = 0
    while line_index < len(lines):
        commandTokens = lines[line_index].split()
        if commandTokens[1] == "cd":
            if commandTokens[2] == "..":
                currentDir = currentDir.parent
            else:
                currentDir = currentDir.contents[commandTokens[2]]
            
            line_index += 1
        elif commandTokens[1] == "ls":
            line_index += 1
            line_index = parse_dir_contents(currentDir, lines, line_index)
    
    root.calculate_total_sizes()
    return root
    


# //////////////////// PARTS /////////////////////////

def run_a(data: Directory):
    directories: list[Directory] = data.get_nested_contents_of_type(Directory)
    
    total = 0
    for dir in directories:
        if dir.size <= 100_000:
            total += dir.size
    
    print(f"Total sum of candidates: {total}")

def run_b(data: Directory):
    directories: list[Directory] = data.get_nested_contents_of_type(Directory)
    
    unused_space = 70_000_000 - data.size
    missing_space = 30_000_000 - unused_space
    min_dir = None
    
    for dir in directories:
        if dir.size >= missing_space and (min_dir is None or dir.size < min_dir.size):
            min_dir = dir
            
    print(f"Total size: {min_dir.size}")