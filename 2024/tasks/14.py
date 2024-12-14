from dataclasses import dataclass
import time
from typing import Any

from utils.vector import Vector2i

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Robot:
    position: Vector2i
    velocity: Vector2i

def parse_input(data: str, part: str) -> list[Robot]:
    
    def parse_robot(line: str) -> Robot:
        pos, vel = line.split(" ")
        return Robot(
            parse_vector(pos),
            parse_vector(vel)
        )
        
    def parse_vector(text: str) -> Vector2i:
        x_str, y_str = text[2:].split(",")
        return Vector2i(int(x_str), int(y_str))
    
    return list(map(parse_robot, data.splitlines("\n")))
    

# //////////////////// PARTS /////////////////////////

# FLOOR_WIDTH = 11
# FLOOR_HEIGHT = 7

FLOOR_WIDTH = 101
FLOOR_HEIGHT = 103

MIDDLE_X = FLOOR_WIDTH // 2
MIDDLE_Y = FLOOR_HEIGHT // 2

def run_a(data: list[Robot]):
    # Update robots
    seconds_to_update = 100
    
    quadrants = {
        "tl": 0,
        "tr": 0,
        "bl": 0,
        "br": 0
    }
    
    for robot in data:
        # Move n seconds
        robot.position.x += seconds_to_update * robot.velocity.x 
        robot.position.y += seconds_to_update * robot.velocity.y 
        
        # Limit to map
        robot.position.x = robot.position.x % FLOOR_WIDTH
        robot.position.y = robot.position.y % FLOOR_HEIGHT
        
        if robot.position.x < 0:
            robot.position.x += FLOOR_WIDTH
        if robot.position.y < 0:
            robot.position.y += FLOOR_HEIGHT
            
        if robot.position.x != MIDDLE_X and robot.position.y != MIDDLE_Y:
            if robot.position.y < MIDDLE_Y:
                if robot.position.x < MIDDLE_X:
                    quadrants["tl"] += 1
                else:
                    quadrants["tr"] += 1
            else:
                if robot.position.x < MIDDLE_X:
                    quadrants["bl"] += 1
                else:
                    quadrants["br"] += 1
            
    safety_score = quadrants["tl"] * quadrants["tr"] * quadrants["bl"] * quadrants["br"]
    print(f"Safety Score: {safety_score}")
            
    
PERCENTAGE = 0.6     

def run_b(data: list[Robot]):
    seconds_run = 0
    
    action = ""
    while action != "stop":
        # action = input("Seconds to update: ")
        
        # if action == "stop":
        #     continue
        
        # seconds_to_update = int(action)
        location_map: dict[Vector2i, list[Robot]] = {}
        for robot in data:
            # Move n seconds
            robot.position.x += 1 * robot.velocity.x 
            robot.position.y += 1 * robot.velocity.y 
            
            # Limit to map
            robot.position.x = robot.position.x % FLOOR_WIDTH
            robot.position.y = robot.position.y % FLOOR_HEIGHT
            
            if robot.position not in location_map:
                location_map[robot.position] = []
            
            location_map[robot.position].append(robot)
            
            if robot.position.x < 0:
                robot.position.x += FLOOR_WIDTH
            if robot.position.y < 0:
                robot.position.y += FLOOR_HEIGHT
                
        close_to_others = 0
        for i, robot in enumerate(data[:-1]):
            close = False
            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    
                    if Vector2i(robot.position.x + j, robot.position.y + i) in location_map:
                        close_to_others += 1
                        close = True
                        break
                    
                if close:
                    break
                
             
        seconds_run += 1
        
        if seconds_run % 100 == 0:
            print(f"Seconds Run: {seconds_run}")
        
        per = close_to_others / len(data)
        if per >= PERCENTAGE:
            for y in range(FLOOR_HEIGHT):
                for x in range(FLOOR_WIDTH):
                    print("#" if Vector2i(x, y) in location_map else ".", end="")
                    
                print()
                
            print(f"Seconds: {seconds_run}")
            input()
        