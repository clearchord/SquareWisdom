from typing import List
from enum import IntEnum
import itertools
import random

class Cell:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column
        self.number = 0
        self.area = None

    def set(self, number: int):
        success = True
        if 0 < number < 10:
            self.number = number
        else:
            success = False
        return success

    def reside_in(self, area: 'Area'):
        self.area = area

class Operator(IntEnum):
    NONE = 0
    PLUS = 1
    MINUS = 2
    TIMES = 3
    DIVIDE = 4

class Area:
    def __init__(self, id: int):
        self.id = id
        self.hint = 0
        self.operator = Operator.NONE
        self.cells: List[Cell] = []
    
    def add(self, cell: Cell):
        self.cells.append(cell)
        cell.reside_in(self)

    def __str__(self) -> str:
        return f'Area {chr(65 + self.id)}: {len(self.cells)}'

class Board:
    def __init__(self, size: int) -> None:
        self.size = size
        self.cells = [[Cell(row, column) for column in range(size)] for row in range(size)]
        self.areas: List[Area] = []
        self.transition_probability = [0.0, 0.1, 0.7, 1.0]

    def show(self):
        for row in range(self.height):
            line = list(map(lambda c: '?' if c.area is None else chr(65 + c.area.id), self.cells[row]))
            print(''.join(line))
        for area in self.areas:
            print(area)
        print()

    def is_divided(self):
        divided = True
        for row, column in itertools.product(range(self.size), range(self.size)):
            if self.cells[row][column].area is None:
                divided = False
                break
        return divided

    def find_non_resident_cell(self):
        found = None
        for row, column in itertools.product(range(self.size), range(self.size)):
            cell = self.cells[row][column]
            if cell.area is None:
                found = cell
                break
        return found
    
    def next_cell_to_include(self, cell: Cell):
        pass

    def define_area(self, id: int, max_chain: int):
        area = Area(id)
        print('Area: ', id)
        cell = self.find_non_resident_cell()
        area.add(cell)
        while len(area.cells) < max_chain:
            chain_length = len(area.cells)
            candidates = []
            for r, c in [(1, 0), (0, 1), (0, -1)]:
                target_row = cell.row + r
                target_column = cell.column + c
                if 0 <= target_row < self.height and 0 <= target_column < self.width:
                    if self.cells[target_row][target_column].area is None:
                        candidates.append((target_row, target_column))
            if 0 < len(candidates):
                index = random.randrange(0, len(candidates))
                selected = candidates[index]
                value = random.uniform(0.0, 1.0)
                print(value)
                print('tp:', self.transition_probability[chain_length])
                if self.transition_probability[chain_length] < value:
                    selected_cell = self.cells[selected[0]][selected[1]]
                    area.add(selected_cell)
                    cell = selected_cell
                else:
                    break
            else:
                break
        return area

    def divide_to_areas(self) -> None:
        max_chain = 4
        while not self.is_divided():
            area = self.define_area(len(self.areas), max_chain)
            self.areas.append(area)

    def make_latin_square(self):
        base_square = [[]]

def test():
    board = Board(6, 6)
    board.divide_to_areas()
    board.show()

if __name__ == '__main__':
    test()
