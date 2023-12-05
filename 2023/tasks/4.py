from dataclasses import dataclass
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class Card:
    id: int
    winning_numbers: list[int]
    numbers: list[int]
    matches: int = 0
    card_count: int = 1
    
    def __post_init__(self):
        for win_num in self.winning_numbers:
            if win_num in self.numbers:
                self.matches += 1
        

def parse_input(data: str) -> list[Card]:
    cards: list[Card] = []
    
    for line in data.split('\n'):
        [info, numbers] = line.split(': ')
        [winning, own_numbers] = numbers.split(' | ')
        
        cards.append(
            Card(
                int(info[5:]),
                list(map(lambda n_str: int(n_str), 
                    filter(lambda n_str: n_str.isnumeric(), winning.split(' '))
                )),
                list(map(lambda n_str: int(n_str), 
                    filter(lambda n_str: n_str.isnumeric(), own_numbers.split(' '))
                ))
            )
        )
    
    return cards


# //////////////////// PARTS /////////////////////////

def run_a(cards: list[Card]):
    sum = 0
    for card in cards:
        if card.matches == 1:
            sum += 1
        if card.matches > 1:
            sum += 2**(card.matches-1)
 
    print(sum)

def run_b(cards: list[Card]):
    reverse_cards = list(reversed(cards))
    
    for idx, card in enumerate(reverse_cards):
        if card.matches > 0:
            card.card_count += sum(map(lambda c: c.card_count, reverse_cards[idx - card.matches : idx]))
            
    print(sum(map(lambda c: c.card_count, reverse_cards)))