from sudoku_generator import generate_sudoku

difficulties = {
    "easy": 30,
    "medium": 40,
    "hard": 50,
}

board = generate_sudoku(9, difficulties["easy"])
for row in board:
    print(row)