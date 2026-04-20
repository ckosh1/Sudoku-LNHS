import math, random

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.cells_to_remove = removed_cells
        self.box_length = int(row_length ** 0.5)
        self.board = [["_"] * row_length for _ in range(row_length)]

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
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
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
        num = random.randint(1, 9)
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                while (not self.is_valid(i, j, num)):
                    num = random.randint(1, 9)
                self.board[i][j] = num

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
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board