Rounds = list[list[str, str]]

def parse_input(data: str) -> Rounds:
    lines = data.split("\n")
    return list(map(lambda l: l.split(" "), lines))


def shape_score(shape: str, opponent: bool = False) -> int:
    return ord(shape) - (64 if opponent else 87)

def round_score(round: list[str, str]) -> int:
    # Draw
    if shape_score(round[0], True) - shape_score(round[1]) == 0: return 3
    
    # Win
    if round == ["A", "Y"] or \
        round == ["B", "Z"] or \
        round == ["C", "X"]: return 6
    
    # Loss
    return 0


def run_a(data: Rounds):
    scores = list(map(lambda r: shape_score(r[1]) + round_score(r), data))
    total_score = sum(scores)
    print(f"The total score for all rounds are: {total_score}")



from utils.numberutils import loop_int

def extract_shape_score(round: list[str, str]) -> int:
    opponent_score = shape_score(round[0], True)
    
    if round[1] == "Y": return opponent_score
    
    if round[1] == "Z":
        return loop_int(opponent_score + 1, 1, 3)
    
    if round[1] == "X":
        return loop_int(opponent_score - 1, 1, 3)

def round_score_new(round_outcome: str) -> int:
    return (ord(round_outcome) - 88) * 3

def run_b(data: Rounds):
    scores = list(map(lambda r: extract_shape_score(r) + round_score_new(r[1]), data))
    total_score = sum(scores)
    print(f"The total score for all rounds are: {total_score}")