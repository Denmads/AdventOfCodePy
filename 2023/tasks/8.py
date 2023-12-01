from functools import reduce


IntMap = list[list[int]]

# //////////////////// PARSING /////////////////////////

def parse_input(data: str) -> IntMap:
    lines = data.split('\n')
    
    trees = [[] for _ in range(len(lines[0]))]
    
    for row in lines:
        for x, n in enumerate(row):
            trees[x].append(int(n))

    return trees        

# //////////////////// PARTS /////////////////////////

def mark_visible_trees(trees: IntMap, start_pos: tuple[int, int], look_dir: tuple[int, int], walk_dir: tuple[int, int]) -> IntMap:
    pos = start_pos
    visible = [
        [
            0 for _ in range(len(trees))    
        ] for _ in range(len(trees[0]))
    ]
    
    while pos[0] >= 0 and pos[0] < len(trees) and pos[1] >= 0 and pos[1] < len(trees[0]):
        walk_pos = pos
        highest_tree = -1
        while walk_pos[0] >= 0 and walk_pos[0] < len(trees) and walk_pos[1] >= 0 and walk_pos[1] < len(trees[0]):
            if trees[walk_pos[0]][walk_pos[1]] > highest_tree:
                highest_tree = trees[walk_pos[0]][walk_pos[1]]
                visible[walk_pos[0]][walk_pos[1]] = 1
            
            walk_pos = (walk_pos[0] + look_dir[0], walk_pos[1] + look_dir[1])
        
        pos = (pos[0] + walk_dir[0], pos[1] + walk_dir[1])
        
    return visible
            
def run_a(data: IntMap):
    width = len(data)
    height = len(data[0])
    
    visible_top = mark_visible_trees(data, (0, 0), (0, 1), (1, 0))
    visible_bottom = mark_visible_trees(data, (0, height-1), (0, -1), (1, 0))
    visible_left = mark_visible_trees(data, (0, 0), (1, 0), (0, 1))
    visible_right = mark_visible_trees(data, (width-1, 0), (-1, 0), (0, 1))
    
    total_visible = 0
    
    for y in range(len(visible_top[0])):
        for x in range(len(visible_top)):
            total = visible_top[x][y] + visible_bottom[x][y] + \
                    visible_left[x][y] + visible_right[x][y]
            total_visible += 1 if total > 0 else 0

    print(f"The amount of visible tree from the outside: {total_visible}")



def calculate_scenic_score(trees: IntMap, pos: tuple[int, int]):
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    scores = []
    for dir in dirs:
        cur_pos = (pos[0] + dir[0], pos[1] + dir[1])
        highest = -1
        count = 0
        while cur_pos[0] >= 0 and cur_pos[0] < len(trees) and cur_pos[1] >= 0 and cur_pos[1] < len(trees[0]):
            # if trees[cur_pos[0]][cur_pos[1]] >= highest:
            #     highest = trees[cur_pos[0]][cur_pos[1]]
            count += 1
            
            if trees[cur_pos[0]][cur_pos[1]] >= trees[pos[0]][pos[1]]:
                break
            
            cur_pos = (cur_pos[0] + dir[0], cur_pos[1] + dir[1])

        scores.append(count)
    
    return reduce(lambda x, y: x * y, scores, 1)

def run_b(data: IntMap):
    max_score = 0
    for y in range(len(data[0])):
        for x in range(len(data)):
            score = calculate_scenic_score(data, (x, y))
            if score > max_score:
                max_score = score
            
    print(f"Max scenic score: {max_score}")