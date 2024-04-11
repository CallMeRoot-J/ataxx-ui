from copy import deepcopy

import numpy as np


class chessboard:
    BLACK = 1
    WHITE = -1
    EMPTY = 0

    dx = [1, 1, 1, 0, 0, -1, -1, -1]
    dy = [1, 0, -1, 1, -1, 1, 0, -1]

    def __init__(self, board_len):
        self.board_len = board_len
        self.current_player = self.BLACK
        self.board = self.get_init_board()
        self.previous_state = []

    def get_init_board(self):
        b = np.zeros((self.board_len, self.board_len), dtype=int)
        b[0][0] = b[self.board_len - 1][self.board_len - 1] = self.WHITE
        b[0][self.board_len - 1] = b[self.board_len - 1][0] = self.BLACK
        return b

    def clear(self):
        self.board = self.get_init_board()
        self.previous_state.clear()
        self.current_player = self.BLACK

    def copy(self):
        return deepcopy(self)

    def in_board(self, x, y):
        return 0 <= x < self.board_len and 0 <= y < self.board_len

    def get_available_actions(self, x, y):
        available_actions = []
        for X in range(x - 2, x + 3):
            for Y in range(y - 2, y + 3):
                if not self.in_board(X, Y):
                    continue
                if (X, Y) == (x, y):
                    continue
                if self.board[X][Y] == self.EMPTY:
                    available_actions.append((X, Y))
        return available_actions

    def do_action(self, oldX, oldY, newX, newY):
        self.previous_state.append(self.board.copy())
        if max(abs(newY - oldY), abs(newX - oldX)) == 2:
            self.board[oldX][oldY] = self.EMPTY
        self.board[newX][newY] = self.current_player
        for i in range(8):
            X, Y = newX + self.dx[i], newY + self.dy[i]
            if not self.in_board(X, Y):
                continue
            if self.board[X][Y] == -self.current_player:
                self.board[X][Y] = self.current_player
        self.current_player = -self.current_player
        return max(abs(newY - oldY), abs(newX - oldX)) == 2

    def is_game_over(self):
        """
        0 not over
        1 black win
        -1 white win
        2 draw
        """
        white_available = False
        black_available = False
        for i in range(self.board_len):
            for j in range(self.board_len):
                if self.board[i][j] == self.EMPTY:
                    continue
                if len(self.get_available_actions(i, j)):
                    if self.board[i][j] == self.BLACK:
                        black_available = True
                    else:
                        white_available = True
        if white_available and black_available:
            return 0
        black = 0
        white = 0
        for i in range(self.board_len):
            for j in range(self.board_len):
                if self.board[i][j] == self.BLACK and not black_available:
                    black += 1
                if self.board[i][j] == self.WHITE and not white_available:
                    white += 1
        if black == 0:
            black = self.board_len**2 - white
        else:
            white = self.board_len**2 - black

        if black > white:
            return 1
        if black < white:
            return -1
        return 2

    def withdraw(self):
        if len(self.previous_state) == 0:
            return False
        state = self.previous_state.pop()
        self.board = state
        self.current_player = -self.current_player
        return True

    def is_available(self, x, y):
        if self.board[x][y] == self.current_player:
            return True
        return False

    def to_fen(self):
        fen = ''
        for j in range(self.board_len - 1, -1, -1):
            empty_count = 0
            for i in range(self.board_len):
                if self.board[i][j] == self.EMPTY:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    if self.board[i][j] == self.BLACK:
                        fen += 'x'
                    else:
                        fen += 'o'
            if empty_count > 0:
                fen += str(empty_count)
            if j != 0:
                fen += '/'
        fen += ' '
        if self.current_player == self.BLACK:
            fen += 'b'
        else:
            fen += 'w'

        return fen
