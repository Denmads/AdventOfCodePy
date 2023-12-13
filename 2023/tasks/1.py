from typing import Any
import re

# Parse all numbers out
def parse_input(data: str, part: str) -> list[str]:
    lines = data.split('\n')
    return lines
        
    

def run_a(data: list[str]):
    lines = list(map(lambda line: re.sub(r'[a-zA-Z]', '', line), data))
    
    
    sum = 0
    for ln in lines:
        number = ln[0] + ln[len(ln)-1]
        sum += int(number)
    
    print(sum)

def run_b(data: list[str]):
    
    sum = 0
    for ln in data:
        digits = get_digits_from_line(ln)
        number = digits[0] + digits[len(digits)-1]
        sum += int(number)
    
    print(sum)
    

def get_digits_from_line(string: str) -> str:
    digits = ""
    for i in range(len(string)):
        digits = check_for_digit_at_index_and_replace(digits, string, i, 'one', '1')
        digits = check_for_digit_at_index_and_replace(digits, string, i, 'two', '2')
        digits = check_for_digit_at_index_and_replace(digits, string, i, 'three', '3')
        digits = check_for_digit_at_index_and_replace(digits, string, i, 'four', '4')
        digits = check_for_digit_at_index_and_replace(digits, string, i, 'five', '5')
        digits = check_for_digit_at_index_and_replace(digits, string, i, 'six', '6')
        digits = check_for_digit_at_index_and_replace(digits, string, i, 'seven', '7')
        digits = check_for_digit_at_index_and_replace(digits, string, i, 'eight', '8')
        digits = check_for_digit_at_index_and_replace(digits, string, i, 'nine', '9')
        
        if (string[i].isdigit()):
            digits += string[i]
        
    return digits
        
    
    
def check_for_digit_at_index_and_replace(digits, string: str, index: int, digit_str: str, digit: str) -> str:
    if index + len(digit_str) > len(string):
        return digits
    
    if string[index : index + len(digit_str)] == digit_str:
        return digits + digit
    
    return digits
        