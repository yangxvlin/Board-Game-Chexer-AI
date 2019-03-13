# board as a list of hexas

import numpy as np
from Hexa import Hexa


class Board:

    SIZE = 7
    board = np.array([])

    def __init__(self):
        board = []

        # 0, 1, 2, 3
        for i in range(self.SIZE//2 + 1):
            row = []
            # 3, 2, 1, 0
            for j in range(int(self.SIZE/2) - i, self.SIZE):
                row.append(Hexa(j, i))
            board.append(row)

        # 4, 5, 6
        for i in range(self.SIZE//2 + 1, self.SIZE):
            row = []
            for j in range(2*(Board.SIZE//2) + 1 - abs(Board.SIZE//2 - i)):
                row.append(Hexa(j, i))
            board.append(row)

        # an array of array
        temp = [np.array(i) for i in board]
        self.board = np.array(temp)

        # an array of lsit
        # self.board = np.array(board)

    def print_board(self):
        rows = self.board.shape[0]
        for i in range(rows):
            cols = self.board[i].shape[0]
            for j in range(cols):
                self.board[i][j].print_hexa()
            print("")
