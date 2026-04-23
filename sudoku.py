import pygame
from sudoku_generator import Board

pygame.init()

WIDTH = 540
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

state = "menu"

easy_button = pygame.Rect(170,200,200,50)
medium_button = pygame.Rect(170,270,200,50)
hard_button = pygame.Rect(170,340,200,50)

reset_button = pygame.Rect(70,530,100,50)
restart_button = pygame.Rect(200,530,100,50)
exit_button = pygame.Rect(330,530,100,50)

font = pygame.font.SysFont("Arial", 20)

running = True
selected = None


while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if state == "menu":

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    board = Board(WIDTH, WIDTH, screen, "easy")
                    state = "game"

                elif medium_button.collidepoint(event.pos):
                    board = Board(WIDTH, WIDTH, screen, "medium")
                    state = "game"

                elif hard_button.collidepoint(event.pos):
                    board = Board(WIDTH, WIDTH, screen, "hard")
                    state = "game"

        elif state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:

                if reset_button.collidepoint(event.pos):
                    board.reset_to_original()

                elif restart_button.collidepoint(event.pos):
                    state = "menu"
                    board = None

                elif exit_button.collidepoint(event.pos):
                    running = False

                else:
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(pos[0], pos[1])

                    if clicked:
                        board.select(clicked[0], clicked[1])

            if event.type == pygame.KEYDOWN:
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
                        board.select(cell.row, cell.col - 1)

                if event.key == pygame.K_RIGHT:
                    cell = board.get_selected()
                    if cell and cell.col < 8:
                        board.select(cell.row, cell.col + 1)

                if event.key == pygame.K_UP:
                    cell = board.get_selected()
                    if cell:
                        board.select(cell.row - 1, cell.col)

                if event.key == pygame.K_DOWN:
                    cell = board.get_selected()
                    if cell and cell.row < 8:
                        board.select(cell.row + 1, cell.col)

    if state == "menu":

        pygame.draw.rect(screen, (255,165,0), easy_button)
        pygame.draw.rect(screen, (255,165,0), medium_button)
        pygame.draw.rect(screen, (255,165,0), hard_button)

        screen.blit(font.render("Easy",True,(255,255,255)),(240,200))
        screen.blit(font.render("Medium", True, (255, 255, 255)), (240, 280))
        screen.blit(font.render("Hard", True, (255, 255, 255)), (240, 360))


    elif state == "game":

        board.draw()

        pygame.draw.rect(screen, (255,165,0), reset_button)
        screen.blit(font.render("Reset",True,(0,0,0)),(95,540))

        pygame.draw.rect(screen, (255, 165, 0), restart_button)
        screen.blit(font.render("Restart", True, (0, 0, 0)), (225, 540))

        pygame.draw.rect(screen, (255, 165, 0), exit_button)
        screen.blit(font.render("Exit", True, (0, 0, 0)), (355, 540))


        if board.is_full():
            if board.check_board():
                print("YOU WIN!")
                running = False
            else:
                print("Game Over (Incorrect Solution)")
                running = False

    pygame.display.update()

pygame.quit()