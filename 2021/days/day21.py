from DailyAssignment import DailyAssignment
from dataclasses import dataclass

@dataclass
class Pawn:
    space: int
    board_size: int
    score: int = 0

    def move(self, number_of_spaces):
        self.space = self.space + number_of_spaces
        while self.space > self.board_size:
            self.space -= self.board_size
        self.score += self.space
    
    def have_won(self):
        return self.score >= 1000

@dataclass
class DeterministicDie:
    val: int = 1
    rolls: int = 0

    def next(self):
        value = self.val
        self.val = max((self.val + 1) % 101, 1)
        self.rolls += 1
        return value

class ADiceGame(DailyAssignment):
    def __init__(self):
        super().__init__(21)

    def run_part_a(self, input: str):
        players = parse_players(input)
        cur_player = 0
        die = DeterministicDie()
        while True:
            to_move = die.next() + die.next() + die.next()
            players[cur_player].move(to_move)
            if players[cur_player].have_won():
                break
            cur_player = (cur_player + 1) % len(players)

        min_score = min(players, key=lambda x: x.score).score
        print(f"{min_score} * {die.rolls} = {min_score * die.rolls}")

    def run_part_b(self, input: str):
        sums = {}
        for i in [1, 2, 3]:
            for j in [1, 2, 3]:
                for k in [1, 2, 3]:
                    s = i+j+k
                    if s not in sums:
                        sums[s] = 0
                    sums[s] += 1
        print(sums)

played_games = {}

def simulate_game(players, cur_player):
    if (players[0].space, players[1].space, players[0].score, players[1].score, cur_player) in played_games:
        return 


def parse_players(input):
    lines = input.split("\n")

    players = []
    for line in lines:
        tokens = line.split(" ")
        player = Pawn(int(tokens[4]), 10)
        players.append(player)
    return players