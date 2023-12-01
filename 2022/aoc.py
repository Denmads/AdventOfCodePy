import loader
import sys
import time

def main(day: str, part: str):

    if part != "a" and part != "b":
        print("Part can only be 'a' or 'b'")
        exit(1)

    task = loader.load_task(day)
    input_txt = loader.load_input(day)
    print("")

    start = time.perf_counter()
    parsed_input = task.parse_input(input_txt)
    parse_time = time.perf_counter() - start
    
    start = time.perf_counter()
    if part == "a":
        task.run_a(parsed_input)
    elif part == "b":
        task.run_b(parsed_input)
    
    exec_time = time.perf_counter() - start
    print("----------------------")
    print(f"Parse: {parse_time} seconds")
    print(f"Run: {exec_time} seconds")
    print(f"Totaling: {parse_time + exec_time}")
    print("")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: aoc.py <day> <part>")
        exit()
    
    main(sys.argv[1], sys.argv[2])