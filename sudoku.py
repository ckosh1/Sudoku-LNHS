from sudoku_generator import generate_sudoku

board = generate_sudoku(9, 30)
for row in board:
    print(row)