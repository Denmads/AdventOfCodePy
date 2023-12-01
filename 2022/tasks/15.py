from typing import Union
from utils.vector import Vector2i
from dataclasses import dataclass

@dataclass
class Sensor:
    pos: Vector2i
    beacon: Vector2i
    
    def dist_to_beacon(self):
        return abs(self.beacon.x - self.pos.x) + abs(self.beacon.y - self.pos.y)
    
    def within_reach(self, x: int, y: int) -> bool:
        dist_to_pos = abs(x - self.pos.x) + abs(y - self.pos.y)
        return self.dist_to_beacon() >= dist_to_pos
    
    def no_beacon_positions(self, min_coord: Vector2i, max_coord: Vector2i, region: 'Rect'):
        r = self.dist_to_beacon()
        min_y = max(min_coord.y, self.pos.y - r)
        max_y = min(max_coord.y, self.pos.y + r)
        
        for y in range(min_y, max_y+1):
            dist_from_sen = abs(y - self.pos.y)
            diff = r - dist_from_sen
            
            min_x = max(self.pos.x - diff, min_coord.x)
            max_x = min(self.pos.x + diff, max_coord.x)
            inter = Interval(min_x, max_x)
            region.remove_interval(y, inter)
            
            
                

# //////////////////// PARSING /////////////////////////

def parse_input(data: str) -> list[Sensor]:
    lines = data.split("\n")
    sensors = []
    
    for line in lines:
        tokens = line.split()
        
        sensor_x = int(tokens[2][2:-1])
        sensor_y = int(tokens[3][2:-1])
        
        beacon_x = int(tokens[8][2:-1])
        beacon_y = int(tokens[9][2:])
        
        sensors.append(Sensor(Vector2i(sensor_x, sensor_y), Vector2i(beacon_x, beacon_y)))
        
    return sensors


# //////////////////// PARTS /////////////////////////

def run_a(data: list[Sensor]):
    target_y = 2_000_000
    positions = set()
    
    for sensor in data:
        dist_to_target = abs(target_y - sensor.pos.y)
        if dist_to_target <= sensor.dist_to_beacon():
            diff = sensor.dist_to_beacon() - dist_to_target
            for x in range(sensor.pos.x - diff, sensor.pos.x + diff):
                positions.add((x, target_y))
    
    print(f"Number pos: {len(positions)}")
            

class Interval:
    def __init__(self, min: int, max:int):
        self.min = min
        self.max = max
        
        self.next: Union[Interval, None] = None
    
    def size(self):
        s = self.max - self.min + 1
        if self.next is None:
            return s
        else:
            return self.next.size() + s 
    
    def set_end(self, next: 'Interval'):
        if self.next is None:
            self.next = next
            return
        
        self.next.set_end(next)
    
    def intersects(self, other: 'Interval'):
        return (self.min <= other.min and other.min <= self.max) or (other.min <= self.min and self.min <= other.max)
    
    def remove(self, to_remove: 'Interval') -> Union['Interval', None]:
        if to_remove.min <= self.min and to_remove.max >= self.max:
            return None
        elif to_remove.min > self.min and to_remove.max < self.max:
            inter1 = Interval(self.min, to_remove.min-1)
            inter2 = Interval(to_remove.max+1, self.max)
            
            inter1.next = inter2
            return inter1
        elif self.min < to_remove.min:
            return Interval(self.min, to_remove.min-1)
        elif self.min > to_remove.min:
            return Interval(to_remove.max+1, self.max)
    
    def __str__(self):
        s = f"{self.min}-{self.max}"
        if self.next is None:
            return s
        else:
            return s + " | " + str(self.next) 

class Range:
    def __init__(self, min: int, max:int):
        self.head = Interval(min, max)
        
    def remove_interval(self, to_remove: Interval):
        interval = self.head
        prev = None
        while interval is not None:
            if interval.intersects(to_remove):
                new_chain = interval.remove(to_remove)
                
                if new_chain is not None:
                    if prev is None:
                        self.head = new_chain
                    else:
                        prev.next = new_chain
                        
                    new_chain.set_end(interval.next)
                    interval = new_chain
                else:
                    if prev is None:
                        self.head = interval.next
                        interval = interval.next
                    else:
                        prev.next = interval.next
                        interval = interval.next
            else:
                prev = interval
                interval = interval.next

    
    def size(self):
        if self.head is None: return 0
        return self.head.size()
    
    def __str__(self):
        return str(self.head)

class Rect:
    def __init__(self, w: int, h: int):
        self.rows: dict[tuple, Range] = {}
        for y in range(0, h+1):
            self.rows[(y,)] = Range(0, w)
    
    def remove_interval(self, y: int, interval_x: Interval):
        if (y,) not in self.rows: return
        
        self.rows[(y,)].remove_interval(interval_x)
        
        if self.rows[(y,)].size() == 0:
            del self.rows[(y,)]


def run_b(data: list[Sensor]):
    max = 4_000_000
    region = Rect(max, max)
    
    min_coord = Vector2i(0, 0)
    max_coord = Vector2i(max, max)
    
    for i, sensor in enumerate(data):
        print(f"Sensor {i+1}/{len(data)}")
        sensor.no_beacon_positions(min_coord, max_coord, region)
        
    y = region.rows.keys()[0][0]
    x = region.rows[(y,)].head.min
    
    print(f"Frequency: {x * 4_000_000 + y}")