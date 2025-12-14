from dataclasses import dataclass
from typing import Any
import re

# //////////////////// PARSING & TYPES /////////////////////////

@dataclass
class ParsedData:
    start_index: int
    splitter_rows: list[list[int]]
    row_width: int

def parse_input(data: str, part: str) -> list[list[int]]:
    splitter_rows = []
    lines = data.split("\n")
    start_index = lines[0].find("S")
    width = len(lines[0])

    for line in lines[1:]:
        splitter_indicies = [i for i, letter in enumerate(line) if letter == "^"]
        splitter_rows.append(splitter_indicies)

    return ParsedData(start_index, splitter_rows, width)

# //////////////////// PARTS /////////////////////////

def run_a(data: ParsedData):
    beam_indicies = set([data.start_index])

    split_count = 0
    for row in data.splitter_rows:
        new_beams = set()
        for beam_idx in beam_indicies:
            if beam_idx in row:
                split_count +=1
                if beam_idx > 0:
                    new_beams.add(beam_idx-1)
                if beam_idx <  data.row_width-1:
                    new_beams.add(beam_idx+1)
            else:
                new_beams.add(beam_idx)

        beam_indicies = new_beams

    print(split_count)

def run_b(data: ParsedData):
    beam_indicies = {
        data.start_index: 1
    }

    cnt = 0
    for row in data.splitter_rows:
        new_beams = beam_indicies.copy()

        for beam_idx in beam_indicies:
            if beam_idx in row:
                new_beams[beam_idx] -= beam_indicies[beam_idx]
                if new_beams[beam_idx] == 0:
                    del new_beams[beam_idx]

                if beam_idx > 0:
                    if beam_idx-1 not in new_beams:
                        new_beams[beam_idx-1] = beam_indicies[beam_idx]
                    else:
                        new_beams[beam_idx-1] += beam_indicies[beam_idx]
                if beam_idx <  data.row_width-1:
                    if beam_idx+1 not in new_beams:
                        new_beams[beam_idx+1] = beam_indicies[beam_idx]
                    else:
                        new_beams[beam_idx+1] += beam_indicies[beam_idx]

        print(f"Row {cnt} / {len(data.splitter_rows)}")
        cnt += 1
        beam_indicies = new_beams

    print(sum(map(lambda v: v, beam_indicies.values())))