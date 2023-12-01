from typing import List
from DailyAssignment import DailyAssignment
from dataclasses import dataclass, field

@dataclass
class Cell:
    number: int
    marked: bool = False

@dataclass
class Line:
    dir: str
    cells: List[Cell] = field(default_factory=list)

    def is_complete(self):
        all_marked = True
        for cell in self.cells:
            all_marked = all_marked and cell.marked
        return all_marked
    
    def mark(self, number):
        for cell in self.cells:
            if cell.number == number:
                cell.marked = True

    def unmarked_sum(self):
        total = 0
        for cell in self.cells:
            if not cell.marked:
                total += cell.number
        return total

@dataclass
class BingoBoard:

    def __init__(self, numbers):
        self.lines = []

        grid = [list(map(lambda x: Cell(x), col)) for col in numbers]

        # rows and colums - Assumption => Square board
        for x in range(len(grid)):
            row = Line("hor")
            col = Line("ver")
            for y in range(len(grid[x])):
                row.cells.append(grid[x][y])
                col.cells.append(grid[y][x])
            self.lines.append(row)
            self.lines.append(col)

    def mark(self, number):
        for line in self.lines:
            line.mark(number)

    def have_won(self):
        for line in self.lines:
            if line.is_complete():
                return True
        return False

    def sum_of_unmarked_cells(self):
        total = 0
        for line in self.lines:
            if line.dir == "hor":
                total += line.unmarked_sum()

        return total

class AGiantSquid(DailyAssignment):
    def __init__(self):
        super().__init__(4)

    def run_part_a(self, input: str):
        numbers, boards = parse_numbers_and_boards(input)
        winning_board = None
        for num in numbers:
            for board in boards:
                board.mark(num)
                if board.have_won():
                    winning_board = board
                    break
            if winning_board is not None:
                score = num * winning_board.sum_of_unmarked_cells()
                print(f"Score of the winning board is '{score}'")
                break

    def run_part_b(self, input: str):
        numbers, boards = parse_numbers_and_boards(input)
        winning_board = None
        for num in numbers:
            for board in boards:
                board.mark(num)
                if all_boards_done(boards):
                    winning_board = board
                    break
            if winning_board is not None:
                score = num * winning_board.sum_of_unmarked_cells()
                print(f"Score of the winning board is '{score}'")
                break

def all_boards_done(boards):
    all_done = True
    for board in boards:
        all_done = all_done and board.have_won()
    return all_done

def parse_numbers_and_boards(input):
    sections = input.split('\n\n')
    called_nums = list(map(lambda x: int(x), sections[0].split(",")))
    boards = []
    for board in sections[1:]:
        lines = board.split("\n")
        board_num = [list(map(lambda x: int(x), filter(lambda x: len(x) > 0, line.split(" ")))) for line in lines]
        boards.append(BingoBoard(board_num))
    return (called_nums, boards)