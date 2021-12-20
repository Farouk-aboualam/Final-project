import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, ROWS, COLS
from .board import Board


class Game:
    def __init__(self, win, selected ="None", board = Board(), turn = RED, valid_moves = {}):
        self._init(selected, board, turn, valid_moves)
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self, selected, board, turn, valid_moves):
        self.selected = selected
        self.board = board
        self.turn = turn
        self.valid_moves = valid_moves

    def reset(self):
        self._init()

    def make_move(self, Piece, row, col):
        self.select(Piece.row, Piece.col)
        self.select(row, col)

    def agent_move(self, initP, finalP):
        Piece = self.board.get_piece(initP[0], initP[1])
        self.make_move(Piece, finalP[0], finalP[1])

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece !=0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            if self._can_eat() and not isinstance(self.board.get_valid_moves(piece), dict):
                self.valid_moves = []

            return True
        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE //2), 15)

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            # skipped = self.valid_moves[(row, col)]
            if isinstance(self.valid_moves, dict):
                skipped = self.valid_moves[(row, col)]
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def winner(self):
        if self.board.red_left <= 0:
            return WHITE
        elif self.board.white_left <= 0:
            return RED
        if not self._can_move(RED):
            return WHITE
        elif not self._can_move(WHITE):
            return RED
        else:
            return None

    def _can_move(self, color):
        can_move = False
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == color:
                    if self.board.get_valid_moves(piece):
                        can_move = True
        return can_move

    def _can_eat(self):
        can_eat = False
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == self.turn:
                    if isinstance(self.board.get_valid_moves(piece), dict):
                        can_eat = True
        return can_eat

    def change_turn(self):
        self.valid_moves = []
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def encode(self):
        board = []
        for row in range(ROWS):
            board.append([])
            for col in range(COLS):
                Piece = self.board.get_piece(row, col)
                if Piece == 0:
                    board[row].append(0)
                else:
                    if Piece.color == RED:
                        if Piece.queen:
                            board[row].append('R')
                        else:
                            board[row].append('r')
                    else:
                        if Piece.queen:
                            board[row].append('W')
                        else:
                            board[row].append('w')
        return board
