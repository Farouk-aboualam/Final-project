import collections

import pygame
import copy
from .constants import BLACK, WHITE, ROWS, COLS, RED, SQUARE_SIZE
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_queens = self.white_queens = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # make queen
        if row == ROWS - 1 or row == 0:
            piece.make_queen()
            if piece.color == WHITE:
                self.white_queens += 1
            else:
                self.red_queens += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < (ROWS//2-1):
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > (ROWS//2):
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def get_valid_moves(self, piece):
        jumped = collections.defaultdict(list)
        valid_jumped = collections.defaultdict(list)
        jumped = self._generate_jump(piece, jumped, 0)
        moves = self._generate_move(piece)
        if jumped:
            length = 0
            # for key, value in jumped.items():
            #     print(key, value)
            for key in jumped.keys():
                # print(len(jumped[key]))
                if len(jumped[key]) > length:
                    length = len(jumped[key])
            for key in jumped.keys():
                if len(jumped[key]) == length:
                    valid_jumped[key] = jumped[key]
            return valid_jumped
            return jumped
        else:
            return moves
        return moves

    def _get_steps(self, piece):
        RED_steps = [(-1, -1), (-1, 1)]
        WHITE_steps = [(1, -1), (1, 1)]
        steps = []
        if piece.color == RED or piece.queen == True: steps.extend(RED_steps)
        if piece.color == WHITE or piece.queen == True: steps.extend(WHITE_steps)
        return steps

    def _generate_move(self, piece):
        moves = []
        for step in self._get_steps(piece):
            row, col = piece.row + step[0], piece.col + step[1]
            if 0 <= row < ROWS and col >= 0 and col < COLS and self.board[row][col] == 0:
                moves.append((row, col))
        return moves

    def _generate_jump(self, piece, jumped, LIMIT):
        for step in self._get_steps(piece):
            row, col = piece.row + step[0], piece.col + step[1]
            if 0 <= row < ROWS and col >= 0 and col < COLS and self.board[row][col] != 0 and self.board[row][col].color != piece.color:
                jrow, jcol = row + step[0], col + step[1]
                if 0 <= jrow < ROWS and jcol >= 0 and jcol < COLS and self.board[jrow][jcol] == 0:
                    if jumped:
                        # jumped[jrow, jcol] = copy.copy(jumped[(row - step[0], col - step[1])])
                        # jumped[jrow, jcol].append((row, col))
                        jumped[jrow, jcol] = copy.copy(jumped[(row - step[0], col - step[1])])
                        jumped[jrow, jcol].append((self.board[row][col]))
                    else:
                        # jumped[jrow, jcol] = [(row, col)]
                        jumped[jrow, jcol] = [(self.board[row][col])]
                    jpiece = copy.deepcopy(piece)
                    jpiece.row, jpiece.col = jrow, jcol
                    if LIMIT > 12:
                        break
                    else:
                        self._generate_jump(jpiece, jumped, LIMIT+1)

        return jumped

    # def generate_jump(self, piece):
    #     jumps = {}
    #     if piece.color == RED:
    #         if self.board[piece.row - 1][piece.col - 1] != 0 and self.board[piece.row - 2][piece.col - 2] == 0:
    #             jumps.update({(piece.row - 2, piece.col - 2): (piece.row - 1, piece.col - 1)})
    #         if self.board[piece.row - 1][piece.col + 1] != 0 and self.board[piece.row - 2][piece.col + 2] == 0:
    #             jumps.update({(piece.row - 2, piece.col + 2): (piece.row - 2, piece.col + 2)})
    #     return jumps
    # def winner(self):
    #     if self.red_left <= 0:
    #         return WHITE
    #     elif self.white_left <= 0:
    #         return RED
    #     else:
    #         return None
    #
    # def get_valid_moves(self, piece):
    #     moves = {}
    #     left = piece.col - 1
    #     right = piece.col + 1
    #     row = piece.row
    #
    #     if piece.color == RED or piece.queen:
    #         moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
    #         moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
    #     if piece.color == WHITE or piece.queen:
    #         moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
    #         moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
    #
    #     return moves
    #
    # def _traverse_left(self, start, stop, step, color, left, skipped=[]):
    #     moves = {}
    #     last = []
    #     for r in range(start, stop, step):
    #         if left < 0:
    #             break
    #         current = self.board[r][left]
    #         if current == 0:
    #             if skipped and not last:
    #                 break
    #             elif skipped:
    #                 moves[(r, left)] = last + skipped
    #             else:
    #                 moves[(r, left)] = last
    #             if last:
    #                 if step == -1:
    #                     row = max(r-3, 0)
    #                 else:
    #                     row = min(r+3, ROWS)
    #                 moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped = last))
    #                 moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
    #             break
    #         elif current.color == color:
    #             break
    #         else:
    #             last = [current]
    #         left -= 1
    #     return moves
    #
    # def _traverse_right(self, start, stop, step, color, right, skipped=[]):
    #     moves = {}
    #     last = []
    #     for r in range(start, stop, step):
    #         if right >= COLS:
    #             break
    #
    #         current = self.board[r][right]
    #         if current == 0:
    #             if skipped and not last:
    #                 break
    #             elif skipped:
    #                 moves[(r, right)] = last + skipped
    #             else:
    #                 moves[(r, right)] = last
    #             if last:
    #                 if step == -1:
    #                     row = max(r - 3, 0)
    #                 else:
    #                     row = min(r + 3, ROWS)
    #                 moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
    #                 moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
    #             break
    #         elif current.color == color:
    #             break
    #         else:
    #             last = [current]
    #         right += 1
    #
    #     return moves
