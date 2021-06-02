import pygame
from MileStone2.constant import RED, BLACK, BLUE, WHITE, WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE, GREY, CROWN, OUTLINE, PADDING
from MileStone2.gamestate import GameState


FPS = 60
pygame.display.set_caption("Checkers game")
WIN = pygame.display.set_mode((WIDTH,HEIGHT))


def get_col_row_from_mouse(pos):
    '''
    get_col_row_from_mouse -- Get row and col numbers based on mouse position
    Parameters:
        pos -- mouse position
    Return:
        Row and col corresponding to the position
    '''
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col


def display_winner(win_side, win):
    '''
    display_winner -- Display who is the winner on the screen
    Parameters:
        win_side -- value of winner side
        win -- screen
    '''
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 40)
    textsurface = myfont.render("win!", False,(0,0,0))
    win.blit(textsurface, (200, 200))


def main():
    run = True
    clock = pygame.time.Clock()
    game = GameState(WIN)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_col_row_from_mouse(pos)
                game.select(row, col)
        game.update()
        if game.isWinner() != None:
            display_winner(game.isWinner(), WIN)
    pygame.quit()


main()
