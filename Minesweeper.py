import sys
import random

class Cell:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.mine = False
        self.open = False
        self.checked = False
        self.neighbor = 0

    def mine_symbol(self) -> str:
        return 'o' if self.mine else '-'

    def open_symbol(self) -> str:
        symbol = None
        if self.open:
            symbol = str(self.neighbor)
        else:
            if self.checked:
                symbol = '*'
            else:
                symbol = '?'
        return symbol

    def set_mine(self, mine: bool) -> None:
        self.mine = mine

    def increment_neighbor(self):
        self.neighbor += 1

class Board:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.cells = [[Cell(row, column) for column in range(width)] for row in range(height)]

    def show_mines(self):
        for row in range(self.height):
            columns = []
            for column in range(self.width):
                columns.append(self.cells[row][column].mine_symbol())
            print(''.join(columns))
        print()

    def show_neighbors(self):
        for row in range(self.height):
            columns = []
            for column in range(self.width):
                columns.append(str(self.cells[row][column].neighbor))
            print(''.join(columns))
        print()

    def show(self):
        for row in range(self.height):
            columns = []
            for column in range(self.width):
                columns.append(self.cells[row][column].open_symbol())
            print(''.join(columns))
        print()


    def place_mines(self, percentage: float) -> None:
        for row in range(self.height):
            for column in range(self.width):
                if percentage < random.random():
                    self.cells[row][column].set_mine(True)

    def count_neighbors(self) -> None:
        for row in range(self.height):
            for column in range(self.width):
                for r in range(-1, 2):
                    row_target = row + r
                    if 0 <= row_target < self.height:
                        for c in range(-1, 2):
                            column_target = column + c
                            if 0 <= column_target < self.width:
                                if self.cells[row_target][column_target].mine:
                                    self.cells[row][column].increment_neighbor()

    def open_initial_cell(self) -> None:
        undetermined = True
        while undetermined:
            row = random.randrange(self.height)
            column = random.randrange(self.width)
            cell = self.cells[row][column]
            if not cell.mine:
                print(f'{row}, {column}')
                self.open(row, column)
                undetermined = False

    def count_checked(self, row: int, column: int) -> int:
        checked = 0
        for r in range(max(0, row - 1), min(self.height, row + 1)):
            for c in range(max(0, column - 1), min(self.width, column + 1)):
                cell = self.cells[r][c]
                checked += 1 if cell.checked else 0
        return checked

    def count_closed(self, row: int, column: int) -> int:
        closed = 0
        for r in range(max(0, row - 1), min(self.height, row + 1)):
            for c in range(max(0, column - 1), min(self.width, column + 1)):
                cell = self.cells[r][c]
                closed += 0 if cell.open else 1
        return closed

    def open(self, row: int, column: int) -> None:
        success = True
        cell = self.cells[row][column]
        if not cell.open:
            if cell.mine:
                success = False
            else:
                cell.open = True
                self.process_if_satisfied(row, column)
        return success

    def process_if_satisfied(self, row: int, column: int) -> None:
        target = self.cells[row][column]
        if target.open:
            if target.neighbor == self.count_closed(row, column):
                for r in range(max(0, row - 1), min(self.height, row + 1)):
                    for c in range(max(0, column - 1), min(self.width, column + 1)):
                        cell = self.cells[r][c]
                        if not cell.open and not cell.checked:
                            cell.checked = True
            if target.neighbor == self.count_checked(row, column):
                for r in range(max(0, row - 1), min(self.height, row + 1)):
                    for c in range(max(0, column - 1), min(self.width, column + 1)):
                        cell = self.cells[r][c]
                        if not cell.open and not cell.checked:
                            self.open(r, c)

    def test(self):
        for row in range(self.height):
            for column in range(self.width):
                self.process_if_satisfied(row, column)

    #def solve(self):

def main():
    board = Board(10, 10)
    board.place_mines(0.9)
    board.show_mines()
    board.count_neighbors()
    board.show_neighbors()
    board.open_initial_cell()
    board.show()
    board.test()
    board.show()
    board.test()
    board.show()
    board.test()
    board.show()

if __name__ == '__main__':
    main()