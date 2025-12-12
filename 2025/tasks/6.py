from dataclasses import dataclass, field
from typing import Any
import re

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class MathProblem:
    numbers: list[int] = field(init=False, default_factory=list)
    operation: str = field(default="")

def parse_input(data: str, part: str) -> list[MathProblem]:
    if part == "a":
        return parse_a(data)
    elif part == "b":
        return parse_b(data)

    

def parse_a(data: str) -> list[MathProblem]:
    lines = data.split("\n")
    num_columns = len(list(filter(None, re.split(r"\s+", lines[0]))))
    problems = [MathProblem() for _ in range(num_columns)]

    for i in range(len(lines)-1):
        for i_n, n in enumerate(filter(None, re.split(r"\s+", lines[i]))):
            problems[i_n].numbers.append(int(n))

    for i_o, o in enumerate(filter(None, re.split(r"\s+", lines[-1]))):
        problems[i_o].operation = o

    return problems

def parse_b(data: str) -> list[MathProblem]:
    lines = data.split("\n")
    num_columns = len(list(filter(None, re.split(r"\s+", lines[0]))))
    problems = [MathProblem() for _ in range(num_columns)]

    column_numbers = []
    column_start = 0
    i = 0
    while i < len(lines[0]):

        if all([line[i] == " " for line in lines[:-1]]):
            column_numbers.append([line[column_start:i] for line in lines[:-1]])
            i += 1
            column_start = i
        else:
            i += 1

    column_numbers.append([line[column_start:i] for line in lines[:-1]])

    for i in range(num_columns):
        num_numbers = len(column_numbers[i][0])
        for j in range(num_numbers):
            num = int("".join([num_str[j] for num_str in column_numbers[i]]))
            problems[i].numbers.append(num)

    for i_o, o in enumerate(filter(None, re.split(r"\s+", lines[-1]))):
        problems[i_o].operation = o

    return problems

# //////////////////// PARTS /////////////////////////

def run_a(data: list[MathProblem]):
    sum = 0

    for problem in data:
        res = 0
        for n in problem.numbers:
            if problem.operation == "+":
                res += n
            elif problem.operation == "*":
                if res == 0:
                    res = n
                else:
                    res *= n
        sum += res

    print(sum)

def run_b(data: list[MathProblem]):
    sum = 0

    for problem in data:
        res = 0
        print(problem)
        for n in problem.numbers:
            if problem.operation == "+":
                res += n
            elif problem.operation == "*":
                if res == 0:
                    res = n
                else:
                    res *= n
        sum += res

    print(sum)