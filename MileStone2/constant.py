import pygame

WIDTH, HEIGHT = 500, 500
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

RED = (255, 0 , 0)
BLACK = (0 , 0 , 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

PADDING = 10
OUTLINE = 2

INI_TURN = BLACK

CROWN = pygame.transform.scale(pygame.image.load("MileStone2\\crown.png"), (45, 25))
