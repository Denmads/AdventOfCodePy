from typing import Callable


def parse_lines(input: str, func: Callable[[str], None]):
    lines = input.split("\n")
    for line in lines:
        func(line)