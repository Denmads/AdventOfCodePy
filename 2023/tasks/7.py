from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import functools

# //////////////////// PARSING & TYPES /////////////////////////

card_strength_dict = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

card_strength_dict_b = {
    'J': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

card_strength_dict_b_rev = {
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: 'T',
    11: 'Q',
    12: 'K',
    13: 'A'
}

class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

@dataclass
class Hand:
    cards: str
    bid: int
    
    card_strengths: list[int] = field(default_factory=list)
    type: HandType = field(init=False)
    
    def calculate(self):
        self.card_strengths = list(map(lambda c: card_strength_dict[c], self.cards))
        self.type = self._find_hand_type()
        
    def calculate_b(self):
        self.card_strengths = list(map(lambda c: card_strength_dict_b[c], self.cards))
        self.type = self._find_hand_type_b()
     
    def _get_card_counts(self, cards):
        counts = {
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
            '7': 0,
            '8': 0,
            '9': 0,
            'T': 0,
            'J': 0,
            'Q': 0,
            'K': 0,
            'A': 0
        }
        
        for c in cards:
            counts[c] += 1
            
        return counts
        
        
    def _find_hand_type(self):
        counts = self._get_card_counts(self.cards)
        
        counts = list(counts.values())
        counts.sort(reverse=True)
        
        if counts[0] == 5:
            return HandType.FIVE_OF_A_KIND
        elif counts[0] == 4:
            return HandType.FOUR_OF_A_KIND
        elif counts[0] == 3 and counts[1] == 2:
            return HandType.FULL_HOUSE
        elif counts[0] == 3 and counts[1] == 1:
            return HandType.THREE_OF_A_KIND
        elif counts[0] == 2 and counts[1] == 2:
            return HandType.TWO_PAIR
        elif counts[0] == 2 and counts[1] == 1:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD
        
    
    def _find_hand_type_b(self):
        jokers = []
        for c in self.cards:
            if c == 'J':
                jokers.append(2)
                
        if len(jokers) == 0:
            return self._find_hand_type()
                
        best_type: HandType = HandType.HIGH_CARD
        while not jokers[-1] > 13:
            counts = self._get_card_counts(self.cards)
            del counts['J']
            
            for jk in jokers:
                counts[card_strength_dict_b_rev[jk]] += 1
                
            counts = list(counts.values())
            counts.sort(reverse=True)
            
            hand_type: HandType = HandType.HIGH_CARD
            if counts[0] == 5:
                hand_type = HandType.FIVE_OF_A_KIND
            elif counts[0] == 4:
                hand_type = HandType.FOUR_OF_A_KIND
            elif counts[0] == 3 and counts[1] == 2:
                hand_type = HandType.FULL_HOUSE
            elif counts[0] == 3 and counts[1] == 1:
                hand_type = HandType.THREE_OF_A_KIND
            elif counts[0] == 2 and counts[1] == 2:
                hand_type = HandType.TWO_PAIR
            elif counts[0] == 2 and counts[1] == 1:
                hand_type = HandType.ONE_PAIR
                
            if hand_type.value > best_type.value:
                best_type = hand_type
                
            jokers = self._increment_jokers(jokers)
        
        return best_type
        
    def _increment_jokers(self, jokers) -> list[int]:
        jokers[0] += 1
        
        for i in range(len(jokers)-1):
            if jokers[i] > 13:
                jokers[i] = 2
                jokers[i+1] += 1
        
        return jokers
        
        

def parse_input(data: str, part: str) -> list[Hand]:
    hands = []
    for line in data.split('\n'):
        (cards, bid) = line.split(' ')
        hands.append(Hand(cards, int(bid)))
        
    return hands


# //////////////////// PARTS /////////////////////////

def compare_hands(hand1: Hand, hand2: Hand) -> int:
    type_diff = hand2.type.value - hand1.type.value
    
    if type_diff != 0:
        return type_diff
    
    for i in range(len(hand1.cards)):
        card_strength_diff = hand2.card_strengths[i] - hand1.card_strengths[i]
        if card_strength_diff != 0:
            return card_strength_diff
    
    return 0

def run_a(hands: list[Hand]):
    for h in hands:
        h.calculate()
    
    hands.sort(key=functools.cmp_to_key(compare_hands), reverse=True)
    
    sum = 0
    for idx, h in enumerate(hands):
        sum += (idx+1) * h.bid
        
    print(sum)
        

def run_b(hands: list[Hand]):
    for h in hands:
        h.calculate_b()
        
    hands.sort(key=functools.cmp_to_key(compare_hands), reverse=True)
        
    sum = 0
    for idx, h in enumerate(hands):
        sum += (idx+1) * h.bid
        
    print(sum)
        