import math, random
import pygame
#using pygame-ce since it is supported on 3.14

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.cells_to_remove = removed_cells
        self.box_length = int(row_length ** 0.5)
        self.board = [[0] * row_length for _ in range(row_length)]

    def get_board(self):
        return self.board

    def print_board(self):
        for i in range(0, self.row_length):
            for j in range(0, self.row_length):
                print(f"[{self.board[i][j]}]", end="")
            print("")

    def valid_in_row(self, row, num):
        for i in range(0, self.row_length):
            if (self.board[row][i] == num):
                return False
        return True

    def valid_in_col(self, col, num):
        for i in range(0, self.row_length):
            if (self.board[i][col] == num):
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start + self.box_length):
            for j in range(col_start, col_start + self.box_length):
                if (self.board[i][j] == num):
                    return False
        return True

    def is_valid(self, row, col, num):
        box_row = row - row % self.box_length
        box_col = col - col % self.box_length

        return (
                self.valid_in_box(box_row, box_col, num)
                and self.valid_in_col(col, num)
                and self.valid_in_row(row, num)
        )

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        idx = 0
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = nums[idx]
                idx += 1

    def fill_diagonal(self):
        self.fill_box(0,0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

    Parameters:
    row, col specify the coordinates of the first empty (0) cell

    Return:
    boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

    Parameters: None
    Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        for i in range(self.cells_to_remove):
            j = random.randint(0, 8)
            k = random.randint(0, 8)
            while self.board[j][k] == 0:
                j = random.randint(0, 8)
                k = random.randint(0, 8)
            self.board[j][k] = 0

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen

        self.sketched_value = 0
        self.selected = False
        self.original = (value != 0)

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        cell_size = 60
        x = self.col * cell_size
        y = self.row * cell_size

        font = pygame.font.Font(None, 40)
        sketch_font = pygame.font.Font(None, 20)

        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + 20, y + 10))

        elif self.sketched_value != 0:
            text = sketch_font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, cell_size, cell_size), 3)

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen

        if difficulty == "easy":
            removed = 30
        elif difficulty == "medium":
            removed = 40
        else:
            removed = 50

        self.board, self.solution = generate_sudoku(9, removed)
        self.cells = [
            [Cell(self.board[r][c], r, c, screen) for c in range(9)]
            for r in range(9)
        ]

        self.selected = None

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        for r in self.cells:
            for cell in r:
                cell.selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def get_selected(self):
        if self.selected:
            r, c = self.selected
            return self.cells[r][c]
        return None

    def click(self, x, y):
        cell_size = self.width // 9

        if x < self.width and y < self.height:
            row = y // cell_size
            col = x // cell_size
            return (row, col)
        return None

    def sketch(self, value):
        cell = self.get_selected()
        if cell and not cell.original:
            cell.set_sketched_value(value)

    def place_number(self, value):
        cell = self.get_selected()
        if cell and not cell.original:
            cell.set_cell_value(value)
            cell.set_sketched_value(0)
            self.update_board()

    def clear(self):
        cell = self.get_selected()
        if cell and not cell.original:
            cell.set_cell_value(0)
            cell.set_sketched_value(0)

    def reset_to_original(self):
        for r in range(9):
            for c in range(9):
                if not self.cells[r][c].original:
                    self.cells[r][c].set_cell_value(0)
                    self.cells[r][c].set_sketched_value(0)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        for r in range(9):
            for c in range(9):
                self.board[r][c] = self.cells[r][c].value

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return (r, c)
        return None

    def check_board(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value != self.solution[r][c]:
                    return False
        return True

'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    solution = [row[:] for row in sudoku.get_board()]  # deep copy
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board, solution
