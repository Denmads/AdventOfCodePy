SpreadSheet = list[list[int]]

def parse_input(data: str) -> SpreadSheet:
    rows = data.split("\n")
    return list(map(lambda r: list(map(lambda c: int(c), r.split())), rows))

def run_a(data: SpreadSheet):
    total = 0
    for row in data:
        total += max(row) - min(row)
        
    print(f"The checksum is: {total}")



def find_even_division(row: list[int]) -> int:
    for i in range(len(row)):
        for j in range(i+1, len(row)):
            res = row[i] / row[j]
            if res % 1 == 0:
                return res
            res = row[j] / row[i]
            if res % 1 == 0:
                return res

def run_b(data: SpreadSheet):
    total = 0
    for row in data:
        total += find_even_division(row)
        
    print(f"The sum is: {total}")