from utils.vector import Vector2i

class World:
    def __init__(self):
        self.tiles = {}
        self.min_point = Vector2i(500, 0)
        self.max_point = Vector2i(500, 0)
        
    def set_rock(self, x: int, y: int):
        self.tiles[f"{x}-{y}"] = "#"
        
        if x < self.min_point.x:
            self.min_point.x = x
        if y < self.min_point.y:
            self.min_point.y = y
        
        if x > self.max_point.x:
            self.max_point.x = x
        if y > self.max_point.y:
            self.max_point.y = y
    
    def set_sand(self, x: int, y: int):
        self.tiles[f"{x}-{y}"] = "O"
    
    def is_tile_empty(self, x: int, y: int):
        if self._is_floor(y):
            return False
        
        key = f"{x}-{y}"
        return not key in self.tiles
    
    def _is_floor(self, y: int) -> bool:
        return y == self.max_point.y + 2
    
    def highest_y(self):
        return self.max_point.y
    
    def print(self):
        padding = 5
        for y in range(self.min_point.y, self.max_point.y+2):
            line = ""
            for x in range(self.min_point.x - padding, self.max_point.x+1 + padding):
                key = f"{x}-{y}"
                line += "." if key not in self.tiles else self.tiles[key]
            print(line)
        
        print("#" * abs((self.min_point.x - padding) - (self.max_point.x+1 + padding)))
        

class Sand:
    
    def __init__(self, x: int, y: int):
        self.pos = Vector2i(x, y)
        
    def update(self, world: World) -> bool:
        """Returns True if the sand moved"""
        
        if world.is_tile_empty(self.pos.x, self.pos.y+1):
            self.pos.y += 1
            return True
        
        if world.is_tile_empty(self.pos.x-1, self.pos.y+1):
            self.pos.x -= 1
            self.pos.y += 1
            return True
        
        if world.is_tile_empty(self.pos.x+1, self.pos.y+1):
            self.pos.x += 1
            self.pos.y += 1
            return True
        
        return False
    
    def is_in_abyss(self, world: World):
        return self.pos.y >= world.max_point.y
        

# //////////////////// PARSING /////////////////////////

def parse_input(data: str) -> World:
    lines = data.split("\n")
    world = World()
    
    for line in lines:
        points = line.split(" -> ")
        
        prev = None
        
        for point in points:
            new_point = tuple(map(lambda x: int(x), point.split(",")))
            
            if prev is not None:
                dir_x = max(-1, min(1, new_point[0] - prev[0]))
                dir_y = max(-1, min(1, new_point[1] - prev[1]))
                
                p = Vector2i(prev[0], prev[1])
                
                
                while p.x != new_point[0] or p.y != new_point[1]:
                    world.set_rock(p.x, p.y)
                    
                    p.x += dir_x
                    p.y += dir_y
                
                world.set_rock(new_point[0], new_point[1])
            
            prev = new_point
    
    return world


# //////////////////// PARTS /////////////////////////

def run_a(data: World):
    sand_count = 1
    sand = Sand(500, 0)
    
    while not sand.is_in_abyss(data):
        if not sand.update(data):
            data.set_sand(sand.pos.x, sand.pos.y)
            sand_count += 1
            sand = Sand(500, 0)
            
        # data.tiles[f"{sand.pos.x}-{sand.pos.y}"] = "O"
        # data.print()
        # input()
        # del data.tiles[f"{sand.pos.x}-{sand.pos.y}"]
            
    print(f"Resting sand: {sand_count-1}")
    

def run_b(data: World):
    sand_count = 1
    sand = Sand(500, 0)
    
    while True:
        if not sand.update(data):
            data.set_sand(sand.pos.x, sand.pos.y)
            if sand.pos.x == 500 and sand.pos.y == 0:
                break
            
            sand_count += 1
            sand = Sand(500, 0)
            
        # data.tiles[f"{sand.pos.x}-{sand.pos.y}"] = "O"
        # data.print()
        # input()
        # del data.tiles[f"{sand.pos.x}-{sand.pos.y}"]
            
    print(f"Resting sand: {sand_count}")