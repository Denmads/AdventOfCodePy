from typing import Dict, List, Type
from DailyAssignment import DailyAssignment
from dataclasses import dataclass, field

@dataclass
class ScoreKeeper:
    scores: Dict[str, int] = field(default_factory=dict)

    def add_score(self, player, amount):
        player_str = str(player)
        if player_str not in self.scores:
            self.scores[player_str] = 0
        self.scores[player_str] += amount
    
    def get_highest_score(self):
        return max(self.scores.values())

@dataclass
class MarbleChainNode:
    value: int
    prev_node: Type["MarbleChainNode"] = None
    next_node: Type["MarbleChainNode"] = None

    def next(self, num):
        if num == 0:
            return self
        return self.next_node.next(num-1)

    def prev(self, num):
        if num == 0:
            return self
        return self.prev_node.prev(num-1)
    

@dataclass
class MarbleCircle:
    current_node: MarbleChainNode = None

    def add_marble(self, num):
        new_node = MarbleChainNode(num)
        score = 0
        if num == 0:
            self.current_node = new_node
            new_node.prev_node = new_node
            new_node.next_node = new_node
        elif num % 23 == 0:
            score += num
            remove = self.current_node.prev(7)
            remove.prev_node.next_node = remove.next_node
            self.current_node = remove.next_node
            score += remove.value
        else:
            before = self.current_node.next(1)
            after = before.next_node
            before.next_node = new_node
            after.prev_node = new_node
            new_node.prev_node = before
            new_node.next_node = after
            self.current_node = new_node
        return score

class AGameOfMarbles(DailyAssignment):
    def __init__(self):
        super().__init__(9)

    def run_part_a(self, input: str):
        players, round = parse_players_and_rounds(input)
        score_keeper = ScoreKeeper()
        circle = MarbleCircle()
        circle.add_marble(0)

        current_player = 1

        for m in range(1, round+1):
            score = circle.add_marble(m)
            score_keeper.add_score(current_player, score)
            current_player = (current_player + 1) % players
        
        print(f"The highest score is '{score_keeper.get_highest_score()}'")

    # The key was to change to a data structure with insert with O(1)
    # Made own doubly linked list
    def run_part_b(self, input: str):
        players, round = parse_players_and_rounds(input)
        score_keeper = ScoreKeeper()
        circle = MarbleCircle()
        circle.add_marble(0)

        current_player = 1

        for m in range(1, (round*100)+1):
            score = circle.add_marble(m)
            score_keeper.add_score(current_player, score)
            current_player = (current_player + 1) % players
            if m % 10000 == 0:
                print(m)
        
        print(f"The highest score is '{score_keeper.get_highest_score()}'")

def parse_players_and_rounds(input):
    tokens = input.split(" ")
    players = int(tokens[0])
    rounds = int(tokens[6])
    return (players, rounds)