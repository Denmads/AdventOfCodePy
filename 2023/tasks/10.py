from dataclasses import dataclass, field
from typing import Any, Union

# //////////////////// PARSING & TYPES /////////////////////////

neighbour_positions = {
    'F': {
        'prev': (0, 1),
        'next': (1, 0)
    },
    '7': {
        'prev': (-1, 0),
        'next': (0, 1)
    },
    'J': {
        'prev': (0, -1),
        'next': (-1, 0)
    },
    'L': {
        'prev': (1, 0),
        'next': (0, -1)
    },
    '-': {
        'prev': (-1, 0), # left
        'next': (1, 0) # right
    },
    '|': {
        'prev': (0, -1), # top
        'next': (0, 1) # bottom
    },
}

@dataclass
class Pipe:
    type: str
    x: int
    y: int
    
    up: Union['Pipe', None] = field(init=False)
    down: Union['Pipe', None] = field(init=False)
    left: Union['Pipe', None] = field(init=False)
    right: Union['Pipe', None] = field(init=False)

def parse_input(data: str, part: str) -> tuple[list[list[Pipe]], Pipe]:
    pipes: list[list[Pipe]] = []
    start_pipe: Pipe = None
    
    lines = data.split('\n')
    for _ in range(len(lines[0])):
        pipes.append([])
    
    print()
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'S':
                start_type = get_start_type(lines, x, y)
                start_pipe = Pipe(start_type, x, y)
                pipes[x].append(start_pipe)  
            elif char == '.':
                pipes[x].append(None)          
            else:
                pipes[x].append(Pipe(char, x, y))
           
    # Link pipes
    for x, line in enumerate(pipes):
        for y, pipe in enumerate(line):
            if pipe is not None:
                pipe.up = get_pipe_neighbour(pipes, pipe, 0, -1)
                pipe.down = get_pipe_neighbour(pipes, pipe, 0, 1)
                pipe.left = get_pipe_neighbour(pipes, pipe, -1, 0)
                pipe.right = get_pipe_neighbour(pipes, pipe, 1, 0)
    
    return pipes, start_pipe   


def get_start_type(lines: list[str], start_x: int, start_y: int) -> str: 
    top_type = lines[start_y-1][start_x] if start_y > 0 else None
    bottom_type = lines[start_y+1][start_x] if start_y < len(lines)-1 else None
    left_type = lines[start_y][start_x-1] if start_x > 0 else None
    right_type = lines[start_y][start_x+1] if start_x < len(lines[0])-1 else None

    top_connects = top_type != None and (top_type == '|' or top_type == 'F' or top_type == '7')
    bottom_connects = bottom_type != None and (bottom_type == '|' or bottom_type == 'L' or bottom_type == 'J')
    left_connects = left_type != None and (left_type == '-' or left_type == 'F' or left_type == 'L')
    right_connects = right_type != None and (right_type == '-' or right_type == '7' or right_type == 'J')
    
    if top_connects and bottom_connects:
        return '|'
    elif left_connects and right_connects:
        return '-'
    elif top_connects and left_connects:
        return 'J'
    elif top_connects and right_connects:
        return 'L'
    elif bottom_connects and left_connects:
        return '7'
    elif bottom_connects and right_connects:
        return 'F'

def get_pipe_neighbour(pipes: list[list[Pipe]], pipe: Pipe, x_off: int, y_off: int) -> Union[Pipe, None]:
    our_neighbours = [
        (
            pipe.x + neighbour_positions[pipe.type]['prev'][0],
            pipe.y + neighbour_positions[pipe.type]['prev'][1]
        ),
        (
            pipe.x + neighbour_positions[pipe.type]['next'][0],
            pipe.y + neighbour_positions[pipe.type]['next'][1]
        )
    ]
    
    
    pos = (pipe.x + x_off, pipe.y + y_off)
    neighbour_pipe: Pipe = pipes[pos[0]][pos[1]]  if (0 <= pos[0] < len(pipes)) and (0 <= pos[1] < len(pipes[0])) else None 
    neigbour_neighbours = [
        (
            pos[0] + neighbour_positions[neighbour_pipe.type]['prev'][0],
            pos[1] + neighbour_positions[neighbour_pipe.type]['prev'][1]
        ),
        (
            pos[0] + neighbour_positions[neighbour_pipe.type]['next'][0],
            pos[1] + neighbour_positions[neighbour_pipe.type]['next'][1]
        )
    ] if neighbour_pipe else []
    
    if (pipe.x, pipe.y) in neigbour_neighbours and (neighbour_pipe.x, neighbour_pipe.y) in our_neighbours:
        return neighbour_pipe
    else:
        return None


# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[list[list[Pipe]], Pipe]):
    (pipes, start) = data
        
    prev = start
    cur = get_next_pipe(prev, start)
    steps = 1
    
        
    while cur.x != start.x or cur.y != start.y:
        cur_tmp = cur
        cur = get_next_pipe(prev, cur)
        prev = cur_tmp
        steps += 1
        
    print(steps // 2)
    
def get_next_pipe(prev_pipe: Pipe, pipe: Pipe) -> Pipe:
        def is_equal(a: Pipe, b: Pipe) -> bool:
            return a.x == b.x and a.y == b.y
        
        if pipe.right is not None and not is_equal(prev_pipe, pipe.right):
            return pipe.right
        elif pipe.down is not None and not is_equal(prev_pipe, pipe.down):
            return pipe.down
        elif pipe.left is not None and not is_equal(prev_pipe, pipe.left):
            return pipe.left
        elif pipe.up is not None and not is_equal(prev_pipe, pipe.up):
            return pipe.up


@dataclass
class Point:
    x: int
    y: int
    
@dataclass
class Line:
    p1: Point
    p2: Point


def run_b(data: tuple[list[list[Pipe]], Pipe]):
    (pipes, start) = data
        
    prev = start
    cur = get_next_pipe(prev, start)
    
    loop_pos = [
        (start.x, start.y)
    ]
    
    line_start: Pipe = start
    loop_lines: list[Line] = []
    
    def is_corner(type: str) -> bool:
        return type == 'F' or type == '7' or type == 'J' or type == 'L'
        
    while cur.x != start.x or cur.y != start.y:
        loop_pos.append((cur.x, cur.y))
        if is_corner(cur.type):
            loop_lines.append(Line(
                Point(line_start.x, line_start.y),
                Point(cur.x, cur.y)
            ))
            line_start = cur
        
        cur_tmp = cur
        cur = get_next_pipe(prev, cur)
        prev = cur_tmp
        
    
    loop_lines.append(Line(
        Point(line_start.x, line_start.y),
        Point(start.x, start.y)
    ))    
    
    
        
    inside = 0
    for x in range(len(pipes)):
        print(f'X: {x+1}/{len(pipes)}')
        for y in range(len(pipes[0])):
            if (x, y) not in loop_pos:
                intersections = count_intersections(loop_lines, loop_pos, x, y, len(pipes))
                if intersections % 2 == 1:
                    inside += 1
                 
    print(f'Points inside: {inside}')
                
                
def count_intersections(lines: list[Line], loop: list[tuple[int, int]], x: int, y: int, max_x: int) -> int:
    count = 0
    
    l = Line(Point(x, y), Point(9999, y))
    
    for line in lines:
        if isIntersect(l, line):
            
            if line.p1.y == y:
                if line.p2.y > y:
                    count += 1
            elif line.p2.y == y:
                if line.p1.y > y:
                    count += 1
            else:
                count += 1 
            
    return count


def onLine(l1, p):
    # Check whether p is on the line or not
    if (
        p.x <= max(l1.p1.x, l1.p2.x)
        and p.x >= min(l1.p1.x, l1.p2.x)
        and (p.y <= max(l1.p1.y, l1.p2.y) and p.y >= min(l1.p1.y, l1.p2.y))
    ):
        return True
    return False

def direction(a, b, c):
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if val == 0:
        # Collinear
        return 0
    elif val < 0:
        # Anti-clockwise direction
        return 2
    # Clockwise direction
    return 1
 
def isIntersect(l1: Line, l2: Line):
    # Four direction for two lines and points of other line
    dir1 = direction(l1.p1, l1.p2, l2.p1)
    dir2 = direction(l1.p1, l1.p2, l2.p2)
    dir3 = direction(l2.p1, l2.p2, l1.p1)
    dir4 = direction(l2.p1, l2.p2, l1.p2)
 
    # When intersecting
    if dir1 != dir2 and dir3 != dir4:
        return True
 
    # When p2 of line2 are on the line1
    if dir1 == 0 and onLine(l1, l2.p1):
        return True
 
    # When p1 of line2 are on the line1
    if dir2 == 0 and onLine(l1, l2.p2):
        return True
 
    # When p2 of line1 are on the line2
    if dir3 == 0 and onLine(l2, l1.p1):
        return True
 
    # When p1 of line1 are on the line2
    if dir4 == 0 and onLine(l2, l1.p2):
        return True
 
    return False