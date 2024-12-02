from typing import Any

from utils.parse_util import parse_lines

# //////////////////// PARSING & TYPES /////////////////////////

type Report = list[int]


def parse_input(data: str, part: str) -> list[Report]:
    reports = []
    
    def line_func(line: str):
        values = line.split(" ")
        report = list(map(lambda x: int(x), values))
        reports.append(report)

    parse_lines(data, line_func)
    
    return reports

# //////////////////// PARTS /////////////////////////

def run_a(data: list[Report]):
    safe_reports = 0
    
    for report in data:
        if is_report_safe(report):
            safe_reports += 1
            
    print(f"The number of safe reports is: {safe_reports}")
    

def run_b(data: list[Report]):
    safe_reports = 0
    
    for report in data:
        if is_report_safe(report):
            safe_reports += 1
        else:
            for modded_report in possible_modded_reports(report):
                if is_report_safe(modded_report):
                    safe_reports += 1
                    break
            
    print(f"The number of safe reports is: {safe_reports}")
    
   
def is_report_safe(report: Report) -> bool:
    report_diffs = [report[i+1] - report[i] for i in range(len(report)-1)]
    all_increasing = all(map(lambda diff: diff > 0, report_diffs))
    all_decreasing = all(map(lambda diff: diff < 0, report_diffs))
    all_small_steps = all(map(lambda diff: abs(diff) >= 1 and abs(diff) <= 3, report_diffs))
    
    return (all_increasing or all_decreasing) and all_small_steps
   
    
def possible_modded_reports(report: Report) -> list[Report]:
    reports = []
    
    for i in range(len(report)):
        modded_report = [x for idx, x in enumerate(report) if idx is not i]
        reports.append(modded_report)
    
    return reports