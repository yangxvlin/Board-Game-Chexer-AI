"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:33:12
Description: Player class
"""
from Board import Board
from Hexe import Hexe


class Player:
    # TODO lower case or upper case or sting
    PLAYER_ORDER = {'red': 0, 'green': 1, 'blue': 2}

    GOAL = "goal"

    """ play win when 4 pieces exit"""
    PLAYER_WIN_THRESHOLD = 4

    # TODO check this
    PLAYER_GOAL = {0: [Hexe(Board.BOARD_BOUND, -i, GOAL) for i in range(0, PLAYER_WIN_THRESHOLD)],
                   1: [Hexe(i-Board.BOARD_BOUND, Board.BOARD_BOUND, GOAL) for i in range(0, PLAYER_WIN_THRESHOLD)],
                   2: [Hexe(-i, i-Board.BOARD_BOUND, GOAL) for i in range(0, PLAYER_WIN_THRESHOLD)]}
