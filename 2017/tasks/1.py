def parse_input(data: str) -> list[int]:
    return list(map(lambda s: int(s), list(data)))


def next(data: list[int], index: int):
    return data[(index+1) % len(data)]

def run_a(data: list[list[int]]):
    total = 0
    for i in range(len(data)):
        if data[i] == next(data, i):
            total += data[i]
    
    print(f"Total of consecutives: {total}")


def next_new(data: list[int], index: int):
    l= len(data)
    return data[(index+(l // 2)) % l]

def run_b(data: list[list[int]]):
    total = 0
    for i in range(len(data)):
        if data[i] == next_new(data, i):
            total += data[i]
    
    print(f"Total of consecutives: {total}")