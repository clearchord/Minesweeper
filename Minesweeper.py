import sys
import random
from pathlib import Path
from typing import List, Tuple

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
            symbol = '*' if self.checked else '?'
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

    def load(path_problem: str) -> None:
        with open(path_problem, 'r', encoding='utf-8') as file:
            height, width = list(map(int, file.readline().split()))
            initialrow, initialcolumn = list(map(int, file.readline().split()))
            mines = int(file.readline())
            mine_positions = []
            for _ in range(mines):
                r, c = list(map(int, file.readline().split()))
                mine_positions.append((r, c))
        board = Board(height, width)
        for row, column in mine_positions:
            board.cells[row][column].set_mine(True)
        board.count_neighbors()
        board.initial_cell_position = (initialrow, initialcolumn)
        board.open(initialrow, initialcolumn)
        board.show()
        return board                

    def save(self, path_problem: str) -> None:
        path = Path(path_problem)
        if not path.parent.exists():
            path.parent.mkdir()
        with open(path, 'w', encoding='utf-8') as file:
            file.write(f'{self.height} {self.width}\n')
            file.write(f'{self.initial_cell_position[0]} {self.initial_cell_position[1]}\n')
            mines = self.count_mines()
            file.write(f'{mines}\n')
            for row in range(self.height):
                for column in range(self.width):
                    cell = self.cells[row][column]
                    if cell.mine:
                        file.write(f'{row} {column}\n')

    def place_mines(self, mine_ratio: float) -> None:
        for row in range(self.height):
            for column in range(self.width):
                if random.random() < mine_ratio:
                    self.cells[row][column].set_mine(True)

    def count_neighbors(self) -> None:
        for row in range(self.height):
            for column in range(self.width):
                for r in range(max(0, row - 1), min(self.height, row + 2)):
                    for c in range(max(0, column - 1), min(self.width, column + 2)):
                        if self.cells[r][c].mine:
                            self.cells[row][column].increment_neighbor()

    def find_safe_cell_at_random(self) -> Tuple[int, int]:
        found = None
        while found is None:
            row = random.randrange(self.height)
            column = random.randrange(self.width)
            if self.cells[row][column].neighbor == 0:
                print(f'safe cell: ({row}, {column}), neighbor: {self.cells[row][column].neighbor}')
                found = (row, column)
        return found

    def open_initial_cell(self) -> None:
        cell_position = self.find_safe_cell_at_random()
        self.initial_cell_position = cell_position
        self.open(cell_position[0], cell_position[1])

    def count_mines(self):
        mines = 0
        for row in range(self.height):
            for column in range(self.width):
                if self.cells[row][column].mine:
                    mines += 1
        return mines

    def count_checked(self, row: int, column: int) -> int:
        checked = 0
        for r in range(max(0, row - 1), min(self.height, row + 2)):
            for c in range(max(0, column - 1), min(self.width, column + 2)):
                cell = self.cells[r][c]
                checked += 1 if cell.checked else 0
        return checked

    def count_closed(self, row: int, column: int) -> int:
        closed = 0
        for r in range(max(0, row - 1), min(self.height, row + 2)):
            for c in range(max(0, column - 1), min(self.width, column + 2)):
                cell = self.cells[r][c]
                closed += 0 if cell.open else 1
        return closed

    def open(self, row: int, column: int) -> None:
        success = True
        board_changed = False
        cell = self.cells[row][column]
        if not cell.open:
            cell.open = True
            board_changed = True
            if cell.mine:
                success = False
        return (success, board_changed)

    def process_if_satisfied(self, row: int, column: int) -> None:
        success = True
        board_changed = False
        target = self.cells[row][column]
        if target.open:
            if target.neighbor == self.count_closed(row, column):
                for r in range(max(0, row - 1), min(self.height, row + 2)):
                    for c in range(max(0, column - 1), min(self.width, column + 2)):
                        cell = self.cells[r][c]
                        if not cell.open and not cell.checked:
                            cell.checked = True
                            board_changed = True
            if target.neighbor == self.count_checked(row, column):
                for r in range(max(0, row - 1), min(self.height, row + 2)):
                    for c in range(max(0, column - 1), min(self.width, column + 2)):
                        cell = self.cells[r][c]
                        if not cell.open and not cell.checked:
                            neighbor_success, neighbor_board_changed = self.open(r, c)
                            success = success and neighbor_success
                            board_changed = board_changed or neighbor_board_changed
        return (success, board_changed)

    def sweep(self):
        success = True
        board_changed = False
        for row in range(self.height):
            for column in range(self.width):
                cell_success, cell_board_changed = self.process_if_satisfied(row, column)
                success = success and cell_success
                board_changed = board_changed or cell_board_changed
        return (success, board_changed)

    def solve(self) -> None:
        board_changed = True
        success = True
        loop = 0
        while board_changed:
            loop += 1
            print(f'Loop: {loop}')
            self.show()
            success, board_changed = self.sweep()
            if not success:
                print('Failed! Wrong algorithm!')
                break
        solved = self.check_if_solved()
        message = 'Problem solved!' if solved else 'Hmm, problem not solved yet.'
        print(message)

    def check_if_solved(self):
        checked = 0
        mines = 0
        for row in range(self.height):
            for column in range(self.width):
                cell = self.cells[row][column]
                if cell.checked:
                    checked += 1
                if cell.mine:
                    mines += 1
        return mines == checked

def generate(height: int, width: int, mine_ratio: float):
    board = Board(height, width)
    board.place_mines(mine_ratio)
    board.count_neighbors()
    board.show_mines()
    board.show_neighbors()
    board.open_initial_cell()
    board.show()
    return board

def test():
    board = Board(20, 20)
    board.place_mines(0.2)
    board.show_mines()
    board.count_neighbors()
    board.show_neighbors()
    board.open_initial_cell()
    board.solve()

def main():
    if 1 < len(sys.argv):
        command = sys.argv[1]
        if command == 'solve':
            path_problem = sys.argv[2]
            print(f'Solving problem {path_problem}')
            board = Board.load(path_problem)
            board.solve()
        elif command == 'generate':
            path_problem = sys.argv[2]
            height = int(sys.argv[3])
            width = int(sys.argv[4])
            mine_ratio = float(sys.argv[5])
            print(f'Generating a problem with mine ratio {str(mine_ratio)} to {path_problem}')
            board = generate(height, width, mine_ratio)
            board.save(path_problem)
            board.process_if_satisfied(board.initial_cell_position[0], board.initial_cell_position[1])
            board.show()
        elif command == 'test':
            test()
        else:
            test()
    else:
        print('Usage:')
        print('\tpython Minesweeper.py test')
        print('\tpython Minesweeper.py solve <path to problem>')
        print('\tpython Minesweeper.py generate <path to problem> <board height> <board width> <mine ratio>')

if __name__ == '__main__':
    main()