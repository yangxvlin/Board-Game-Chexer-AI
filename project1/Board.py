"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:30:38
Description: Class used to represent the board
"""
from Hexe import Hexe


class Board(object):
    BOARD_BOUND = 3

    BOARD_HEXES = [Hexe(0, -3), Hexe(0, -2), Hexe(0, -1), Hexe(0, 0),
                   Hexe(0, 1), Hexe(0, 2), Hexe(0, 3),

                   Hexe(1, -3), Hexe(1, -2), Hexe(1, -1), Hexe(1, 0),
                   Hexe(1, 1), Hexe(1, 2),

                   Hexe(2, -3), Hexe(2, -2), Hexe(2, -1), Hexe(2, 0),
                   Hexe(2, 1),

                   Hexe(3, -3), Hexe(3, -2), Hexe(3, -1), Hexe(3, 0),

                   Hexe(-1, -2), Hexe(-1, -1), Hexe(-1, 0), Hexe(-1, 1),
                   Hexe(-1, 2), Hexe(-1, 3),

                   Hexe(-2, -1), Hexe(-2, 0), Hexe(-2, 1), Hexe(-2, 2),
                   Hexe(-2, 3),

                   Hexe(-3, 0), Hexe(-3, 1), Hexe(-3, 2), Hexe(-3, 3)]

    N_PLAYER = 3
