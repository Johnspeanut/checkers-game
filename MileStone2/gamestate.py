import pygame
from .constant import RED, BLACK, BLUE, WHITE, WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE, GREY, CROWN, OUTLINE, PADDING, INI_TURN
from .piece import Piece


class GameState():
    def __init__(self, win):
        self.pieces = []
        self.create_pieces()
        self.turn = RED
        self.selected = None
        self.valid_moves = {}
        self.pieces_left_red = self.pieces_left_black = 12
        self.left_red_kings = self.left_black_kings = 0
        self.win = win


    def create_pieces(self):
        '''
        create_pieces -- creates a initiaive pieces
        Parameters:
            self -- the current piece object
        '''
        for i in range(ROWS):
            self.pieces.append([])
            for j in range(COLS):
                if (i + j) % 2 != 0:
                    self.pieces[i].append(0)
                elif i < 3:
                    self.pieces[i].append(Piece(i, j, RED))
                elif i > 4:
                    self.pieces[i].append(Piece(i, j, BLACK))
                else:
                    self.pieces[i].append(0)


    def draw_pieces(self):
        '''
        draw_pieces -- Draw pieces
        Parameters:
            self -- the current piece object
            win -- The window that drawing on
        '''
        for i in range(ROWS):
            for j in range(COLS):
                if self.pieces[i][j] != 0:
                    self.pieces[i][j].draw_piece(self.win)


    def draw_squares(self):
        '''
        draw_pieces -- Draw pieces
        Parameters:
            self -- the current piece object
        '''
        for i in range(ROWS):
            for j in range(COLS):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.win, GREY, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(self.win, WHITE, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def get_piece(self, row, col):
        '''
        get_piece -- Get a piece
        Parameters:
            self -- the current piece object
            row -- A row where the piece locates in
            col -- A col where the piece locates in
        Return:
            A piece object that corresponding to row and col
        '''
        return self.pieces[row][col]


    def turn_change(self):
        '''
        urn_change -- Change turn
        Parameters:
            self -- the current piece object
            current_piece -- current piece
        '''
        self.valid_moves = {}
        if self.turn == RED:
            return BLACK
        else:
            return RED
    

    def remove(self, skipped):
        '''
        remove -- remove skipped pieces
        Parameters:
            self -- the current piece object
           skipped -- pieces that captured, Piece type
        '''
        for item in skipped:
            if item != 0:
                if item.color == RED:
                    self.pieces_left_red -= 1
                elif item.color == BLACK:
                    self.pieces_left_black -= 1
                self.pieces[item.row][item.col] = 0


    def draw_valid_move(self, moves):
        '''
        draw_valid_move -- draw blue blocks indicating valid moves
        Parameters:
            self -- the current piece object
            moves -- a list of valid moves
        '''
        for key in moves:
            i_row, i_col = key
            pygame.draw.rect(self.win, BLUE, (i_col * SQUARE_SIZE, i_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def move_a_piece_on_game(self, to_row, to_col, piece):
        '''
        move_a_piece_on_game -- move a piece on a game
        Parameters:
            self -- the current piece object
            to_row -- A row that the piece wants to move to
            to_col -- A col that the piece wants to move to
        '''
        if piece != 0 and piece.color == self.turn:
            self.pieces[piece.row][piece.col], self.pieces[to_row][to_col] = self.pieces[to_row][to_col], self.pieces[piece.row][piece.col]
            self.pieces[to_row][to_col].move(to_row, to_col)
        
    
    def select(self, row, col):
        '''
        select -- select a piece
        Parameters:
            self -- the current piece object
            row -- A row that the piece selected
            col -- A col that the piece selected
        '''
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.search_valid_moves(piece)
            return True
        return False


    def _move(self, row, col):
        '''
        _move -- move a piece on a game
        Parameters:
            self -- the current piece object
            to_row -- A row that the piece wants to move to
            to_col -- A col that the piece wants to move to
        '''
        piece = self.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.move_a_piece_on_game(row, col, self.selected)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.remove(skipped)
            self.turn = self.turn_change()
            return True
        else:
            return False


    def update(self):
        '''
        update -- update display and drawing every turn
        Parameters:
            self -- the current piece object
        '''
        self.draw_squares()
        self.draw_pieces()
        self.draw_valid_move(self.valid_moves)
        pygame.display.update()

    
    def search_valid_moves(self, current_piece):
        '''
        valid_move -- The list of tuple indicating next valid move of current_piece
        Parameters:
            self -- the current piece object
            current_piece -- current piece
        Return:
            A dictionary with valid moves as key, and a list of skipped pieces as value
        '''
        if isinstance(current_piece, Piece):
            valid_moves_dic = {}
            left = current_piece.col - 1
            right = current_piece.col + 1
            row = current_piece.row
            if current_piece.color == RED or current_piece.isKing:
                valid_moves_dic.update(self.left_search_moves(row + 1, min(row+3,ROWS), 1, current_piece.color, left))
                valid_moves_dic.update(self.right_search_moves(row + 1, min(row+3,ROWS), 1, current_piece.color, right))
            if current_piece.color == BLACK or current_piece.isKing:
                valid_moves_dic.update(self.left_search_moves(row - 1, max(row - 3, -1), -1, current_piece.color, left))
                valid_moves_dic.update(self.right_search_moves(row - 1,max(row - 3, -1), -1, current_piece.color, right))
            return valid_moves_dic


    def left_search_moves(self, start, end, step, color, left, skipped = []):
        '''
        left_search_moves -- search valid cells and skipped cells in left direction
        Parameters:
            self -- the current piece object
            start -- the begining row of search
            end --  the end row of search
            step -- -1 for upward search direction and 1 for downward search direction
            color -- piece color
            skipped -- a list of pieces skipped. Initiated is empty list 
        Return:
            A dictionary with valid moves as key, and a list of skipped pieces as value
        '''
        moves = {}
        last = []
        for i in range(start, end, step):
            if left < 0:
                break
            current = self.pieces[i][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(i, left)] = last + skipped
                else:
                    moves[(i, left)] = last
                
                if last:
                    if step == -1:
                        row = max(i-3, 0)
                    else:
                        row = min(i+3, ROWS)
                    moves.update(self.left_search_moves(i + step, row, step, color, left - 1, skipped = last))
                    moves.update(self.right_search_moves(i + step, row, step, color, left + 1, skipped = last))
                break

            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves


    def right_search_moves(self, start, end, step, color, right, skipped = []):
        '''
        right_search_moves -- search valid cells and skipped cells in right direction
        Parameters:
            self -- the current piece object
            start -- the begining row of search
            end --  the end row of search
            step -- -1 for upward search direction and 1 for downward search direction
            color -- piece color
            skipped -- a list of pieces skipped. Initiated is empty list
        Return:
            A dictionary with valid moves as key, and a list of skipped pieces as value
        '''
        moves = {}
        last = []
        for i in range(start, end, step):
            if right >= COLS:
                break

            current = self.pieces[i][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(i, right)] = last + skipped
                else:
                    moves[(i, right)] = last
                
                if last:
                    if step == -1:
                        row = max(i-3, 0)
                    else:
                        row = min(i+3, ROWS)
                    moves.update(self.left_search_moves(i + step, row, step, color, right - 1, skipped = last))
                    moves.update(self.right_search_moves(i + step, row, step, color, right + 1, skipped = last))
                break

            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves


    def isWinner(self):
        '''
        isWinner -- Check if there is a winner
        Parameters:
            self -- the current piece object
        Return:
            Winner side if there is a winner. Otherwise, None.
        '''
        if self.pieces_left_black <= 0:
            return RED
        if self.pieces_left_red <= 0:
            return BLACK
        return None
    
    
    def evaluate(self):
        return self.pieces_left_red - self.pieces_left_black + self.left_red_kings*0.5 - self.left_black_kings*0.5
