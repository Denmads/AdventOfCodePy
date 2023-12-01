from typing import List
from DailyAssignment import DailyAssignment
from dataclasses import dataclass

@dataclass
class Light:
    position: List[int]
    velocity: List[int]

    def update(self, time_steps):
        self.position[0] += self.velocity[0] * time_steps
        self.position[1] += self.velocity[1] * time_steps

class AMessageInTheSky(DailyAssignment):
    def __init__(self):
        super().__init__(10)

    def run_part_a(self, input: str):
        lights = parse_lights(input)
        minp, maxp = find_bound(lights)
        prev_area = 9999999999999999
        area = light_area(minp, maxp)
        diff = area - prev_area

        while diff < 0:
            update_all_lights(lights, 1)
            minp, maxp = find_bound(lights)
            prev_area = area
            area = light_area(minp, maxp)
            diff = area - prev_area

        update_all_lights(lights, -1)
        minp, maxp = find_bound(lights)
        print_lights(lights, minp, maxp)

    def run_part_b(self, input: str):
        lights = parse_lights(input)
        minp, maxp = find_bound(lights)
        prev_area = 9999999999999999
        area = light_area(minp, maxp)
        diff = area - prev_area

        cnt = 0
        while diff < 0:
            update_all_lights(lights, 1)
            minp, maxp = find_bound(lights)
            prev_area = area
            area = light_area(minp, maxp)
            diff = area - prev_area
            cnt += 1

        print(f"They would have to wait '{cnt-1}'")

def print_lights(lights, min_pos, max_pos):
    grid = [[" "] * (max_pos[1] - min_pos[1]+1) for _ in range(max_pos[0] - min_pos[0]+1)]
    for light in lights:
        x = light.position[0]-min_pos[0]
        y = light.position[1]-min_pos[1]
        grid[x][y] = "#"

    for y in range(len(grid[0])):
        line = ""
        for x in range(len(grid)):
            line += grid[x][y]
        print(line)
                
def find_bound(lights):
    min_x = min(lights, key=lambda l: l.position[0])
    min_y = min(lights, key=lambda l: l.position[1])
    max_x = max(lights, key=lambda l: l.position[0])
    max_y = max(lights, key=lambda l: l.position[1])

    min_pos = (min_x.position[0], min_y.position[1])
    max_pos = (max_x.position[0], max_y.position[1])
    return min_pos, max_pos

def light_area(minp, maxp):
    return (maxp[1] - minp[1]) * (maxp[0] - minp[0])

def update_all_lights(lights, time_steps):
    for light in lights:
        light.update(time_steps)

def parse_lights(input):
    lines = input.split("\n")
    lights = []
    for line in lines:
        parts = line.split(" v")
        pos_parts = parts[0][10:-1].split(",")
        vel_parts = parts[1][9:-1].split(",")
        light = Light(
            [int(pos_parts[0]), int(pos_parts[1])],
            [int(vel_parts[0]), int(vel_parts[1])]
        )
        lights.append(light)
    return lights
