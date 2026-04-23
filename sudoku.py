import pygame
from sudoku_generator import Board

pygame.init()

WIDTH = 540
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

difficulty = "easy"
board = Board(WIDTH, WIDTH, screen, difficulty)

running = True
selected = None

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked = board.click(pos[0], pos[1])

            if clicked:
                board.select(clicked[0], clicked[1])

        if event.type == pygame.KEYDOWN:

            # NUMBER INPUT (SKETCH)
            if event.key == pygame.K_1:
                board.sketch(1)
            if event.key == pygame.K_2:
                board.sketch(2)
            if event.key == pygame.K_3:
                board.sketch(3)
            if event.key == pygame.K_4:
                board.sketch(4)
            if event.key == pygame.K_5:
                board.sketch(5)
            if event.key == pygame.K_6:
                board.sketch(6)
            if event.key == pygame.K_7:
                board.sketch(7)
            if event.key == pygame.K_8:
                board.sketch(8)
            if event.key == pygame.K_9:
                board.sketch(9)

            if event.key == pygame.K_RETURN:
                cell = board.get_selected()
                if cell:
                    board.place_number(cell.sketched_value)
            if event.key == pygame.K_BACKSPACE:
                board.clear()
            if event.key == pygame.K_r:
                board.reset_to_original()
                
            if event.key == pygame.K_LEFT:
                cell = board.get_selected()
                if cell:
                    board.select(cell.row,cell.col -1)

            if event.key == pygame.K_RIGHT:
                cell = board.get_selected()
                if cell:
                    board.select(cell.row,cell.col +1)

            if event.key == pygame.K_UP:
                cell = board.get_selected()
                if cell:
                    board.select(cell.row-1,cell.col)

            if event.key == pygame.K_DOWN:
                cell = board.get_selected()
                if cell:
                    board.select(cell.row+1,cell.col)



    board.draw()
    if board.is_full():
        if board.check_board():
            print("YOU WIN!")
            running = False
        else:
            print("Game Over (Incorrect Solution)")
            running = False

    pygame.display.update()

pygame.quit()
