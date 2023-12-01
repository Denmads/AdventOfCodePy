
from dataclasses import dataclass, field
from utils.vector import Vector2i

@dataclass
class Tetromino:
    x: int
    y: int
    tiles: list[Vector2i] = field(init=False, default=None)
    
    def initialize(self):
        self.y += self.get_height()-1
    
    def get_width(self) -> int:
        pass
    
    def get_height(self) -> int:
        pass
    
    def get_tile_positions(self) -> list[Vector2i]:
        return self.tiles
    
    def contains(self, x: int, y: int):
        return any(map(lambda p: p.x == x and p.y == y, self.tiles))
    
    def move_horizontal(self, world: set[tuple[int, int]], amount: int):
        new_x = self.x + amount
        right = new_x + self.get_width() - 1
        if 0 <= new_x and right < 7 and not self.collides(world, amount, 0):
            self.x = new_x
            for tile in self.tiles:
                tile.x += amount

    def collides(self, world: set[tuple[int, int]], x_offset: int, y_offset: int) -> bool:
        return any(map(lambda p: (p.x+x_offset, p.y - y_offset) in world or p.y - y_offset == -1, self.tiles))
    
    def move_down(self, world: set[tuple[int, int]], amount: int) -> bool:
        if self.collides(world, 0, amount): 
            return False
        
        self.y -= amount
        for tile in self.tiles:
            tile.y -= amount
        return True

class Flat(Tetromino):
    
    def initialize(self):
        super().initialize()
        self.tiles = [Vector2i(self.x, self.y),Vector2i(self.x+1, self.y),Vector2i(self.x+2, self.y),Vector2i(self.x+3, self.y)]
    
    def get_width(self) -> int:
        return 4
    
    def get_height(self) -> int:
        return 1
    
class Vertical(Tetromino):
    
    def initialize(self):
        super().initialize()
        self.tiles = [Vector2i(self.x, self.y),Vector2i(self.x, self.y-1),Vector2i(self.x, self.y-2),Vector2i(self.x, self.y-3)]
    
    def get_width(self) -> int:
        return 1
    
    def get_height(self) -> int:
        return 4 
    
class Plus(Tetromino):
    
    def initialize(self):
        super().initialize()
        self.tiles = [Vector2i(self.x+1, self.y),Vector2i(self.x, self.y-1),Vector2i(self.x+1, self.y-1),Vector2i(self.x+2, self.y-1),Vector2i(self.x+1, self.y-2)]
    
    def get_width(self) -> int:
        return 3
    
    def get_height(self) -> int:
        return 3     
    
class Square(Tetromino):
    
    def initialize(self):
        super().initialize()
        self.tiles = [Vector2i(self.x, self.y),Vector2i(self.x+1, self.y),Vector2i(self.x, self.y-1),Vector2i(self.x+1, self.y-1)]
    
    def get_width(self) -> int:
        return 2
    
    def get_height(self) -> int:
        return 2
    
class Corner(Tetromino):
    
    def initialize(self):
        super().initialize()
        self.tiles = [Vector2i(self.x+2, self.y),Vector2i(self.x+2, self.y-1),Vector2i(self.x, self.y-2),Vector2i(self.x+1, self.y-2),Vector2i(self.x+2, self.y-2)]
    
    def get_width(self) -> int:
        return 3
    
    def get_height(self) -> int:
        return 3


class Chamber:
    def __init__(self, jets: list[int]):
        self.jets: list[int] = jets
        self.jet_index: int = 0
        
        self.piece_count: int = 0
        self.world: set[tuple[int, int]] = set()
        self.y_top: int = -1

        self.current_piece: Tetromino = self.create_next_piece()
        self.current_piece.initialize()
    
    def create_next_piece(self) -> Tetromino:
        index = self.piece_count % 5
        spawn_y = self.y_top + 4
        
        if index == 0: return Flat(2, spawn_y)
        elif index == 1: return Plus(2, spawn_y)
        elif index == 2: return Corner(2, spawn_y)
        elif index == 3: return Vertical(2, spawn_y)
        elif index == 4: return Square(2, spawn_y)
    
    def update(self, debug: bool = False):
        # horizontal
        self.current_piece.move_horizontal(self.world, self.jets[self.jet_index])
        self.jet_index = (self.jet_index + 1) % len(self.jets)
        if debug:
            self.print_world()
        
        # vertical
        if not self.current_piece.move_down(self.world, 1):
            for p in self.current_piece.get_tile_positions():
                self.world.add((p.x, p.y))
            
            self.y_top = max(self.y_top, self.current_piece.y)
            self.piece_count += 1
            self.current_piece = self.create_next_piece()
            self.current_piece.initialize()
        if debug:
            self.print_world()
        
    
    def print_world(self):
        for y in range(self.y_top+4+self.current_piece.get_height(), -1, -1):
            line = ""
            for x in range(0, 7):
                if (x, y) in self.world:
                    line += "#"
                elif self.current_piece.contains(x, y):
                    line += "@"
                else:
                    line += "."
            
            print(line)
        print()


class ChamberV2:
    def __init__(self, jets: list[int]):
        self.jets: list[int] = jets
        self.jet_index: int = 0
        
        self.piece_count: int = 0
        self.world: set[tuple[int, int]] = set()
        self.y_top: int = -1

        self.current_piece: Tetromino = self.create_next_piece()
        self.current_piece.initialize()
    
    def create_next_piece(self) -> Tetromino:
        index = self.piece_count % 5
        spawn_y = self.y_top + 4
        
        if index == 0: return Flat(2, spawn_y)
        elif index == 1: return Plus(2, spawn_y)
        elif index == 2: return Corner(2, spawn_y)
        elif index == 3: return Vertical(2, spawn_y)
        elif index == 4: return Square(2, spawn_y)
    
    def update(self, debug: bool = False):
        # horizontal
        self.current_piece.move_horizontal(self.world, self.jets[self.jet_index])
        self.jet_index = (self.jet_index + 1) % len(self.jets)
        if debug:
            self.print_world()
        
        # vertical
        if not self.current_piece.move_down(self.world, 1):
            for p in self.current_piece.get_tile_positions():
                self.world.add((p.x, p.y))
            
            self.y_top = max(self.y_top, self.current_piece.y)
            self.piece_count += 1
            self.current_piece = self.create_next_piece()
            self.current_piece.initialize()
            
            self.check_lines()
            
        if debug:
            self.print_world()
    
    def check_lines(self):
        stored = []
        for y in range(self.y_top, -1, -1):
            positions = [(0,y),(1,y),(2,y),(3,y),(4,y),(5,y),(6,y)]
            contained_in = list(map(lambda p: p in self.world, positions))
            if all(contained_in):
                self.world = set()
                for pos in positions:
                    self.world.add(pos)
                for pos in stored:
                    self.world.add(pos)
                return
            else:
                for i in range(7):
                    if contained_in[i]:
                        stored.append(positions[i])
        # print(self.piece_count) 
        # print("exit")

    def print_world(self):
        for y in range(self.y_top+4+self.current_piece.get_height(), -1, -1):
            line = ""
            for x in range(0, 7):
                if (x, y) in self.world:
                    line += "#"
                elif self.current_piece.contains(x, y):
                    line += "@"
                else:
                    line += "."
            
            print(line)
        print()

# //////////////////// PARSING /////////////////////////

def map_to_int(x: str) -> int:
    return 1 if x == ">" else -1

def parse_input(data: str) -> Chamber:
    moves = list(data)
    jets = list(map(map_to_int, moves))
    return Chamber(jets)
    

# //////////////////// PARTS /////////////////////////

def run_a(data: Chamber):
    while data.piece_count != 2022:
        data.update(False)
    
    print(f"Height: {data.y_top+1}")

def run_b(data: Chamber):
    newChamber = ChamberV2(data.jets)
    # If a line fills, ignore everything below
    
    while newChamber.piece_count != 1_000_000_000_000:
        if newChamber.piece_count % 10000 == 0:
            print(newChamber.piece_count, len(newChamber.world))
        newChamber.update(False)
        # input()
    
    print(f"Height: {newChamber.y_top+1}")