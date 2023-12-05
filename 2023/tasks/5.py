from dataclasses import dataclass, field
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class TranslationRange:
    source_start: int
    destination_start: int
    length: int
    
    source_end: int = field(init=False)
    destination_end: int = field(init=False)
    
    diff_amount: int = field(init=False)
    
    def __post_init__(self):
        self.source_end = self.source_start + self.length - 1
        self.destination_end = self.destination_start + self.length - 1
        
        self.diff_amount = self.destination_start - self.source_start
    

@dataclass
class CategoryTranslator:
    ranges: list[TranslationRange]
    reversed_ranges: list[TranslationRange] = field(init=False)
    
    def __post_init__(self):
        self.reversed_ranges = list(reversed(self.ranges))
    
    def translate(self, value: int) -> int:
        for rng in self.ranges:
            if rng.source_start <= value and value <= rng.source_end:
                return rng.destination_start + rng.diff_amount
        
        return value
    
    def reverse_translate(self, value: int) -> int:
        for rng in self.reversed_ranges:
            if rng.destination_start <= value and value <= rng.destination_end:
                return rng.source_start - rng.diff_amount
        
        return value


def map_translator(string: str) -> CategoryTranslator:
    lines = string.split('\n')

    ranges = []
    for line in lines[1:]:
        [dest_start, src_start, length] = line.split(' ')
        ranges.append(TranslationRange(
            int(src_start),
            int(dest_start),
            int(length)
        ))
    
    return CategoryTranslator(ranges)

SeedList = list[int]

def parse_input(data: str) -> tuple[SeedList, list[CategoryTranslator]]:
    segments = data.split('\n\n')

    seeds = list(map(lambda x: int(x), segments[0][7:].split(' ')))
    translators = list(map(lambda tr_str: map_translator(tr_str), segments[1:]))

    return (seeds, translators)


# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[SeedList, list[CategoryTranslator]]):
    values = data[0] # starts as seeds

    for translator in data[1]:
        values = [translator.translate(x) for x in values]

    print(min(values))

def run_b(data: tuple[SeedList, list[CategoryTranslator]]):
    seed_ranges = list(divide_chunks(data[0], 2))

    cnt = 0
    while True:
        if cnt % 100000 == 0:
            print(cnt)
        
        value = cnt
        for translator in reversed(data[1]):
            value = translator.reverse_translate(value)
            
        if is_seed(value, seed_ranges):
            break
        
        cnt += 1

    print(cnt)

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
        
def is_seed(value: int, seed_ranges: list[list[int, int]]):
    for rng in seed_ranges:
        if rng[0] <= value and value <= rng[0] + rng[1] - 1:
            return True
        
    return False