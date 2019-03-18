"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:23:57
Description: 
"""

BOARD_BOUND = 3

MOVE_DELTA = [(-1, 0), (0, -1), (1, -1), (1, 0),  (0, 1),  (-1, 1)]

MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"

""" play win when 4 pieces exit"""
PLAYER_WIN_THRESHOLD = 4

PLAYER_GOAL = {"red": [(BOARD_BOUND, -i) for i in range(0, PLAYER_WIN_THRESHOLD)],
               "green": [(i-BOARD_BOUND, BOARD_BOUND) for i in range(0, PLAYER_WIN_THRESHOLD)],
               "blue": [(-i, i-BOARD_BOUND) for i in range(0, PLAYER_WIN_THRESHOLD)]}
