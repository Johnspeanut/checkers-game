import pygame
from .constant import RED, BLACK, BLUE, WHITE, WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE, GREY, CROWN, OUTLINE, PADDING


class Piece():
    '''
    Class -- Piece
        Represents a piece.
    Attributes:
        row -- the row where a piece in, an integer.
        col -- the row where a piece in, an integer.
        color -- the color that a piece has, tuple
        isKing -- if the piece is king, boolean
        center_x -- x coordinate, left top is zero, integer
        center_y -- y coordinate, integer
    '''


    def __init__(self, row, col, color):
        '''
        Constructor -- creates a new instance of PlayingCard
        Parameters:
            self -- the current piece object
            row -- the row where a piece in, an integer.
            col -- the row where a piece in, an integer.
            color -- the color that a piece has, tuple
            isKing -- if the piece is king, boolean
            center_x -- x coordinate, left top is zero, integer
            center_y -- y coordinate, integer
        '''
        self.row = row
        self.col = col
        self.color = color
        self.isKing = False
        self.center_x, self.center_y = self._calc_x_y_from_col_row()


    def _calc_x_y_from_col_row(self):
        '''
        Method -- _calc_x_y_from_col_row
            Calculate x and y coordinates for a piece, private method
        Parameter:
            self -- The current piece object
        Returns:
            x and y coordinates
        '''

        self.center_x = self.col * SQUARE_SIZE + SQUARE_SIZE / 2
        self.center_y = self.row * SQUARE_SIZE + SQUARE_SIZE / 2
        return self.center_x, self.center_y


    def make_king(self):
        '''
        Method -- make_king
            Make a piece to be a king
        Parameter:
            self -- The current piece object
        Returns:
            No return
        '''
        self.isKing = True


    def move(self, to_row, to_col):
        '''
        Method -- move
            A piece move
        Parameter:
            self -- The current piece object
            to_row -- The row of destination cell that the piece gonna move to
            to_col -- The col of destination cell that the piece gonna move to
        Returns:
            No return
        '''
        self.row = to_row
        self.col = to_col
        if self.row == ROWS - 1 and self.color == RED:
            self.make_king()
        if self.row == 0 and self.color == BLACK:
            self.make_king()
        self.center_x, self.center_y = self._calc_x_y_from_col_row()


    def draw_piece(self, win):
        '''
        Method -- draw_piece
            Draw the piece on window
        Parameter:
            self -- The current piece object
            win -- The window that drawing on
        Returns:
            No return
        '''
        radius = SQUARE_SIZE / 2 - PADDING
        pygame.draw.circle(win, self.color, (self.center_x, self.center_y), radius + OUTLINE)
        pygame.draw.circle(win, self.color, (self.center_x, self.center_y), radius)
        if self.isKing:
            win.blit(CROWN, (self.center_x - CROWN.get_width()//2, self.center_y - CROWN.get_height()//2))
