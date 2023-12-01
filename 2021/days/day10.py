from DailyAssignment import DailyAssignment

class MEssedUpNavigation(DailyAssignment):
    def __init__(self):
        super().__init__(10)

    def run_part_a(self, input: str):
        lines = input.split("\n")
        point_table = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137
        }
        illegal_counts = {
            ")": 0,
            "]": 0,
            "}": 0,
            ">": 0
        }
        for line in lines:
            stack = []
            for ch in line:
                if ch in ["(", "[", "{", "<"]:
                    stack.append(ch)
                else:
                    opening = stack.pop()
                    if (ch == ")" and opening != "(") or (ch == "]" and opening != "[") or (ch == "}" and opening != "{") or (ch == ">" and opening != "<"):
                        illegal_counts[ch] += 1
        
        error_score = 0
        for ch in point_table.keys():
            error_score += point_table[ch] * illegal_counts[ch]
        print(error_score)

    def run_part_b(self, input: str):
        lines = input.split("\n")
        
        scores = []
        for line in lines:
            stack = []
            illegal = False
            for ch in line:
                if ch in ["(", "[", "{", "<"]:
                    stack.append(ch)
                else:
                    opening = stack.pop()
                    if (ch == ")" and opening != "(") or (ch == "]" and opening != "[") or (ch == "}" and opening != "{") or (ch == ">" and opening != "<"):
                        illegal = True
                        break
            if not illegal:
                scores.append(
                    calc_score(stack)
                )
        
        scores.sort()
        print(scores[len(scores) // 2])
                
def calc_score(chars):
    point_table = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }
    conversion_table = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">"
    }
    missing = list(map(lambda x: conversion_table[x], chars))
    missing.reverse()
    total = 0
    for ch in missing:
        total *= 5
        total += point_table[ch]
    return total
