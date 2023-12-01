def parse_input(data: str) -> list[list[str]]:
    lines = data.split("\n")
    return [l.split() for l in lines]


def is_valid(passphrase: list[str]):
    return len(set(passphrase)) == len(passphrase)

def run_a(data: list[list[str]]):
    count = 0
    for phrase in data:
        if is_valid(phrase):
            count += 1
    print(f"Number of valid passphrases: {count}")

def run_b(data: list[list[str]]):
    count = 0
    for phrase in data:
        new_phrase = ["".join(sorted(word)) for word in phrase]
        
        if is_valid(new_phrase):
            count += 1
    print(f"Number of valid passphrases: {count}")