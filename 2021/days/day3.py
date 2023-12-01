from typing import List
from DailyAssignment import DailyAssignment

class SubmarineDiagnostic(DailyAssignment):
    def __init__(self):
        super().__init__(3)

    def run_part_a(self, input: str):
        lines = input.split("\n")

        half = len(lines) // 2

        gamma_str = ""
        epsilon_str = ""
        for i in range(len(lines[0])):
            ones = count_bits_in_position(lines, "1", i)
            gamma_str += "1" if ones > half else "0"
            epsilon_str += "0" if ones > half else "1"
        gamma = int(gamma_str, 2)
        epsilon = int(epsilon_str, 2)
        print(f"Gamma: {gamma}")
        print(f"Epsilon: {epsilon}")
        print(f"Power Consumption: {gamma * epsilon}")


    def run_part_b(self, input: str):
        lines = input.split("\n")

        oxygen_rating = int(find_oxygen_gen_rating(lines), 2)
        co2_rating = int(find_co2_scrubber_rating(lines), 2)
        print(f"Oxygen Generator Rating: {oxygen_rating}")
        print(f"CO2 Scrubber Rating: {co2_rating}")
        print(f"Life Support Rating: {oxygen_rating * co2_rating}")


def count_bits_in_position(binaries, bit, position):
    count = 0
    for line in binaries:
        count += 1 if line[position] == bit else 0
    return count

def find_oxygen_gen_rating(binaries):
    bin_cpy = [bin for bin in binaries]

    bit_index = 0
    while len(bin_cpy) > 1:
        ones = count_bits_in_position(bin_cpy, "1", bit_index)
        keeping = "1" if ones / len(bin_cpy) >= 0.5 else "0"
        bin_cpy = list(filter(lambda x: x[bit_index] == keeping, bin_cpy))
        bit_index += 1
    return bin_cpy[0]


def find_co2_scrubber_rating(binaries):
    bin_cpy = [bin for bin in binaries]

    bit_index = 0
    while len(bin_cpy) > 1:
        ones = count_bits_in_position(bin_cpy, "1", bit_index)
        keeping = "1" if ones / len(bin_cpy) < 0.5 else "0"
        bin_cpy = list(filter(lambda x: x[bit_index] == keeping, bin_cpy))
        bit_index += 1
    return bin_cpy[0]