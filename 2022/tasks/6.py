def parse_input(data: str) -> dict[int, str]:
    return {i: v for i, v in enumerate(list(data))}

def run_a(data: dict[int, str]):
    marker_length = 4
    for i in range(len(data)-(marker_length-1)):
        if len(set([data[j] for j in range(i, i+marker_length)])) == marker_length:
            print(f"Chars to end of first marker: {i+marker_length}")
            return

def run_b(data: dict[int, str]):
    marker_length = 14
    for i in range(len(data)-(marker_length-1)):
        if len(set([data[j] for j in range(i, i+marker_length)])) == marker_length:
            print(f"Chars to end of first marker: {i+marker_length}")
            return