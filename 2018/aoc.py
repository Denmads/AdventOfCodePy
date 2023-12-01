from inspect import isclass
import sys, os, importlib
from DailyAssignment import DailyAssignment


days_module = "days"
day_modules = [
    "day1",
    "day2",
    "day3",
    "day4",
    "day5",
    "day6",
    "day7",
    "day8",
    "day9",
    "day10",
    "day11",
    "day12",
    "day13"
]
inputs_folder = "inputs"

def load_assignment(name: str) -> DailyAssignment:
    return importlib.import_module(days_module + "." + name)

def load_daily_assignments():
    days = {}
    for mod in day_modules:
        day_assign = load_assignment(mod)
        for key, val in day_assign.__dict__.items():
            if isclass(val) and issubclass(val, DailyAssignment) and val != DailyAssignment:
                day = val()
                days[str(day.day_index)] = day
    return days

def load_inputs():
    path = os.path.join(os.path.dirname(__file__), inputs_folder)
    files = os.listdir(path)

    inputs = {}
    for f in files:
        with open(path + "\\" + f, "r") as input:
            inputs[f.split(".")[0]] = input.read()
    return inputs

def main():
    if len(sys.argv) != 4 and len(sys.argv) != 3:
        print("Invalid number of arguments!")
        print("Usage: aoc.py <dayIndex> <part> [input_name]")
        exit()

    days = load_daily_assignments()
    inputs = load_inputs()

    if sys.argv[1] not in days:
        print("The day '" + sys.argv[1] + "' is not a valid index!")
        exit()

    if sys.argv[2] not in ["a", "b"]:
        print("The part must be 'a' or 'b'!")
        exit()

    if len(sys.argv) == 3:
        input_name = sys.argv[1]
        if input_name not in inputs:
            print("No input exists for '" + input_name + "'!")
            exit()
        
        input = inputs[input_name]
    else:
        if sys.argv[3] not in inputs:
            print("No input exists for '" + sys.argv[3] + "'!")
            exit()

        input = inputs[sys.argv[3]]
    
    print("Running '" + type(days[sys.argv[1]]).__name__ + "'")
    if sys.argv[2] == "a":
        days[sys.argv[1]].run_part_a(input)
    else:
        days[sys.argv[1]].run_part_b(input)


if __name__ == '__main__':
    main()