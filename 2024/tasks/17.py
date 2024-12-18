from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# //////////////////// PARSING & TYPES /////////////////////////

class Register(Enum):
    A = "A"
    B = "B"
    C = "C"

@dataclass
class B3PC:
    _registers: dict[Register, int] = field(default_factory=dict, init=False)
    _instruction_pointer: int = field(default=0, init=False)
    _output_list: list[int] = field(default_factory=list, init=False)
    
    _skip_pointer_increment: bool = field(default=False, init=False)
    
    def __post_init__(self):
        self._registers[Register.A] = 0
        self._registers[Register.B] = 0
        self._registers[Register.C] = 0
        
    def reset(self):
        self._registers[Register.A] = 0
        self._registers[Register.B] = 0
        self._registers[Register.C] = 0
        self._instruction_pointer = 0
        self._output_list = []
        self._skip_pointer_increment = False
    
    def set_register(self, register: Register, value: int):
        self._registers[register] = value
        
    def get_output(self) -> list[int]:
        return self._output_list
    
    def run_program(self, program: list[int], debug: bool = False):
        if debug:
            print("New Run")
        
        while self._instruction_pointer < len(program):
            op_code = program[self._instruction_pointer]
            operand = program[self._instruction_pointer+1]
            
            if debug:
                self._print_debug(program, op_code, operand)
                input()
            
            if op_code == 0:
                self._adv(self._get_combo_operand(operand))
            elif op_code == 1:
                self._bxl(operand)
            elif op_code == 2:
                self._bst(self._get_combo_operand(operand))
            elif op_code == 3:
                self._jnz(operand)
            elif op_code == 4:
                self._bxc(self._get_combo_operand(operand))
            elif op_code == 5:
                self._out(self._get_combo_operand(operand))
            elif op_code == 6:
                self._bdv(self._get_combo_operand(operand))
            elif op_code == 7:
                self._cdv(self._get_combo_operand(operand))
            
            if not self._skip_pointer_increment:
                self._instruction_pointer += 2
                
            self._skip_pointer_increment = False
            
        if debug:
            print(f"Result: {self._output_list}")
            print(f"------------------------------------------")
            
    def _print_debug(self, program: list[int], op_code: int, operand: int):
        
        combo = self._get_combo_operand(operand)
        
        cmd_to_execute = ""
        if op_code == 0:
            cmd_to_execute = f"adv -> {self._registers[Register.A]} // 2**{combo} = {self._registers[Register.A] // 2**combo} in A"
        elif op_code == 1:
            cmd_to_execute = f"bxl -> {self._registers[Register.B]} ^ {operand} = {self._registers[Register.B] ^ operand} in B"
        elif op_code == 2:
            cmd_to_execute = f"bst -> {combo} % 8 = {combo % 8} in B"
        elif op_code == 3:
            cmd_to_execute = f"jnz -> if {self._registers[Register.A]} != 0 then goto {operand}"
        elif op_code == 4:
            cmd_to_execute = f"bxc -> {self._registers[Register.B]} ^ {self._registers[Register.C]} = {self._registers[Register.B] ^ self._registers[Register.C]} in B"
        elif op_code == 5:
            cmd_to_execute = f"out -> {combo} % 8 = {combo % 8}"
        elif op_code == 6:
            cmd_to_execute = f"bdv -> {self._registers[Register.A]} // 2**{combo} = {self._registers[Register.A] // 2**combo} in B"
        elif op_code == 7:
            cmd_to_execute = f"cdv -> {self._registers[Register.A]} // 2**{combo} = {self._registers[Register.A] // 2**combo} in C"
        
        print("Program: " + ",".join(map(str, program)))
        space_str = " " * (9 + self._instruction_pointer * 2)
        print(space_str + "^")
        print()
        print("Command: " + cmd_to_execute)
        print()
        print("Registers:")
        print(f"\tA: {self._registers[Register.A]}")
        print(f"\tB: {self._registers[Register.B]}")
        print(f"\tC: {self._registers[Register.C]}")
        print()
        print(f"Output: {",".join(map(str, self._output_list))}")
        print()
        print("================================================================")
            
    def _get_combo_operand(self, operand: int) -> int:
        if operand in [0, 1, 2, 3]:
            return operand
        elif operand == 4:
            return self._registers[Register.A]
        elif operand == 5:
            return self._registers[Register.B]
        elif operand == 6:
            return self._registers[Register.C]
        
        return -1
        
    def _output(self, value: int):
        self._output_list.append(value)
        
    def _adv(self, operand: int):
        numerator = self._registers[Register.A]
        denominator = 2**operand
        
        result = numerator // denominator
        self.set_register(Register.A, result)
    
    def _bxl(self, operand: int):
        result = self._registers[Register.B] ^ operand
        self.set_register(Register.B, result)
    
    def _bst(self, operand: int):
        result = operand % 8
        self.set_register(Register.B, result)
    
    def _jnz(self, operand: int):
        if self._registers[Register.A] != 0:
            self._instruction_pointer = operand
            self._skip_pointer_increment = True
    
    def _bxc(self, operand: int):
        result = self._registers[Register.B] ^ self._registers[Register.C]
        self.set_register(Register.B, result)
    
    def _out(self, operand: int):
        result = operand % 8
        self._output(result)
    
    def _bdv(self, operand: int):
        numerator = self._registers[Register.A]
        denominator = 2**operand
        
        result = numerator // denominator
        self.set_register(Register.B, result)
    
    def _cdv(self, operand: int):
        numerator = self._registers[Register.A]
        denominator = 2**operand
        
        result = numerator // denominator
        self.set_register(Register.C, result)
        

def parse_input(data: str, part: str) -> tuple[list[int], list[int]]:
    registers_str, program_str = data.split("\n\n")
    
    registers_values = list(map(lambda l: int(l.split(": ")[1]) , registers_str.split("\n")))
    program = list(map(int, program_str.split(": ")[1].split(",")))

    return (program, registers_values)

# //////////////////// PARTS /////////////////////////

def run_a(data: tuple[list[int], list[int]]):
    program, registers = data
    
    pc = B3PC()
    pc.set_register(Register.A, registers[0])
    pc.set_register(Register.B, registers[1])
    pc.set_register(Register.C, registers[2])
    
    pc.run_program(program)
    
    print(f"Output: {",".join(map(str, pc.get_output()))}")

def run_b(data: tuple[list[int], list[int]]):
    program, registers = data
            # 35184372088832
    counter = 35984372088832
    output = []
    
    while output != program:
        # counter += 1
        counter = int(input("A: "))
        
        pc = B3PC()
        pc.set_register(Register.A, counter)
        pc.set_register(Register.B, registers[1])
        pc.set_register(Register.C, registers[2])
        
        pc.run_program(program)
        
        output = pc.get_output()
        
        print(f"{counter} = {output}")
        
        # if counter == 20000:
        #     break
    # print(f"A Value: {counter}")
    
    
def matches(output, program):
    for i, val in enumerate(output):
        program_index = len(program)-1-i
        if val != program[program_index]:
            return False
        
    return True