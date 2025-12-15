from dataclasses import dataclass
from typing import Any
import re

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Button:
    lights_to_toggle: list[int]
    toggle_mask: int

    def press(self, current_state: int) -> int:
        return current_state ^ self.toggle_mask

@dataclass
class Machine:
    indicator_lights_goal: int
    buttons: list[Button]
    light_joltage_cost: list[int]
    

def parse_input(data: str, part: str) -> list[Machine]:
    machines = []

    def remove_chars(input: str, chars: str):
        for ch in chars:
            input = input.replace(ch, "")

        return input

    for line in data.split("\n"):

        lights, buttons, joltage = list(filter(lambda x: x is not None and len(x.strip()) > 0, re.split(r"((?<=\]) )|( (?=\{))", line)))

        lights = remove_chars(lights, "[]")
        num_lights = len(lights)
        light_goal_state = int("".join(map(lambda c: "1" if c == "#" else "0", lights)), 2)

        buttons_str = remove_chars(buttons, "()")
        buttons = []
        for btn in buttons_str.split(" "):
            ints = list(map(int, btn.split(",")))
            toggle_mask = int("".join(["1" if i in ints else "0" for i in range(num_lights)]), 2)
            buttons.append(Button(ints, toggle_mask))

        joltages = list(map(int, remove_chars(joltage, "{}").split(",")))

        machines.append(Machine(light_goal_state, buttons, joltages))
    
    return machines
        


# //////////////////// PARTS /////////////////////////

def run_a(data: list[Machine]):
    num_steps = []

    for machine in data:
        steps = 0
        next_possible_states: list[int] = [machine.indicator_lights_goal]
        turned_off = False
        while not turned_off:
            new_states: list[int] = []
            for state in next_possible_states:
                for button in machine.buttons:
                    if button.toggle_mask & state > 0:
                        ns = button.press(state)
                        if ns == 0:
                            turned_off = True
                            continue
                        new_states.append(ns)

            next_possible_states = new_states
            steps += 1

        num_steps.append(steps)

    print(sum(num_steps))

def run_b(data: list[Machine]):
    pass