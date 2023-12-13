from dataclasses import dataclass
from typing import Any

# //////////////////// PARSING /////////////////////////
@dataclass
class GameRound:
    red: int = 0
    green: int = 0
    blue: int = 0
    
@dataclass
class Game:
    id: int
    rounds: list[GameRound]
    
    

def parse_input(data: str, part: str) -> list[Game]:
    games = data.split('\n')
    return list(map(parse_game, games))

def parse_game(game_str: str) -> Game:
    # Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    [info, rounds] = game_str.split(': ')
    
    parsed_rounds = list(map(parse_round, rounds.split('; ')))
    return Game(int(info[5:]), parsed_rounds)

def parse_round(round_str: str) -> GameRound:
    #3 green, 4 blue, 1 red
    groups = round_str.split(', ')
    
    round = GameRound()
    for group in groups:
        [amount, color] = group.split(' ')
        
        if color == "red":
            round.red = int(amount)
        elif color == "green":
            round.green = int(amount)
        elif color == "blue":
            round.blue = int(amount)
        
    return round


# //////////////////// PARTS /////////////////////////

max_red = 12
max_green = 13
max_blue = 14
def run_a(games: list[Game]):
    def no_more_than_max(round: GameRound) -> bool:
        return round.red <= max_red and round.green <= max_green and round.blue <= max_blue
    
    possible_games: list[Game] = []
    for game in games:
        if (all(no_more_than_max(round) for round in game.rounds)):
            possible_games.append(game)
            
    sum_of_ids = sum(map(lambda game: game.id, possible_games))
    print(f"Sum {sum_of_ids}")

def run_b(games: Any):
    power_sum = 0
    
    for game in games:
        min_red = max(game.rounds, key=lambda round: round.red).red
        min_green = max(game.rounds, key=lambda round: round.green).green
        min_blue = max(game.rounds, key=lambda round: round.blue).blue
        
        power_sum += min_red * min_green * min_blue
    
    print(f"Sum {power_sum}")
    
        