def parse_input(data: str) -> int:
    return int(data)



def get_ring_info(cell: int) -> tuple[int, int]: # Number, Size
    rn = 3
    n = 1
    while rn*rn <= cell:
        rn += 2
        n += 1
    return n-1, rn

def get_cell_pos(cell: int) -> tuple[int, int]:
    ring_num, ring_size = get_ring_info(cell)
    prev_ring_end_cell = (ring_size-2)**2
    pos = [ring_num, -ring_num]
    
    cell_diff = cell - prev_ring_end_cell
    
    if cell_diff == 0:
        return pos
    
    pos[0] += 1
    cell_diff -= 1
    if cell_diff == 0:
        return pos
    
    if cell_diff <= ring_size-2:
        pos[1] += cell_diff
        return pos
    else:
        cell_diff -= ring_size-2
        pos[1] += ring_size-2
    
    if cell_diff <= ring_size-1:
        pos[0] -= cell_diff
        return pos
    else:
        cell_diff -= ring_size-1
        pos[0] -= ring_size-1

        
    if cell_diff <= ring_size-1:
        pos[1] -= cell_diff
        return pos
    else:
        cell_diff -= ring_size-1
        pos[1] -= ring_size-1
    
    pos[0] += cell_diff
    return pos

def run_a(data: int):
    pos = get_cell_pos(data)
    steps = abs(pos[0]) + abs(pos[1])
    print(f"Steps to take: {steps}")

def calculate_cell_value(cells: dict[tuple[int, int], int], x: int, y: int) -> int:
    total = 0
    dirs = [(0, 1),(1, 1),(1, 0),(1, -1),(0, -1),(-1, -1),(-1, 0),(-1, 1)]
    for neigh in dirs:
        coord = (x + neigh[0], y + neigh[1])
        if coord in cells:
            print(coord)
            total += cells[coord]
    print("Done")
    return total
    

def run_b(data: int):
    cells: dict[tuple[int, int], int] = {(0, 0): 1}
    
    x: int = 0
    y: int = 0
    rn_size: int = 1
    cell_val: int = 1
    
    while True:
        # Move to next ring
        rn_size += 2
        x+= 1
        cell_val = calculate_cell_value(cells, x, y)
        cells[(x, y)] = cell_val
        
        if cell_val > data:
            break
        
        # Move up
        while y < rn_size // 2:
            y += 1

            cell_val = calculate_cell_value(cells, x, y)
            cells[(x, y)] = cell_val
            
            if cell_val > data:
                break
        
        if cell_val > data:
                break
            
        
        # Move left
        while x > -(rn_size // 2):
            x -= 1

            cell_val = calculate_cell_value(cells, x, y)
            cells[(x, y)] = cell_val
            
            if cell_val > data:
                break
        
        if cell_val > data:
                break
            
        
        # Move down
        while y > -(rn_size // 2):
            y -= 1

            cell_val = calculate_cell_value(cells, x, y)
            cells[(x, y)] = cell_val
            
            if cell_val > data:
                break
        
        if cell_val > data:
                break
        
        
        # Move right
        while x < (rn_size // 2):
            x += 1

            cell_val = calculate_cell_value(cells, x, y)
            cells[(x, y)] = cell_val
            
            if cell_val > data:
                break
        
        if cell_val > data:
                break
    
    print(f"Value: {cell_val}")