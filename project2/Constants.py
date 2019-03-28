"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:23:57
Description: Constants used in program
"""

""" size of the chexer board """
BOARD_BOUND = 3

""" hexe piece's moving delta """
MOVE_DELTA = [(-1, 0), (0, -1), (1, -1), (1, 0),  (0, 1),  (-1, 1)]

""" move action """
MOVE = "MOVE"

""" jump action """
JUMP = "JUMP"

""" exit action """
EXIT = "EXIT"

""" player win when 4 pieces exit """
PLAYER_WIN_THRESHOLD = 4

MAX_TURN = 256

""" each player's goal hexes' axial coordinates """
PLAYER_GOAL = {"red": [(BOARD_BOUND, -i)
                       for i in range(0, PLAYER_WIN_THRESHOLD)],
               "green": [(i-BOARD_BOUND, BOARD_BOUND)
                         for i in range(0, PLAYER_WIN_THRESHOLD)],
               "blue": [(-i, i-BOARD_BOUND)
                        for i in range(0, PLAYER_WIN_THRESHOLD)]}

PLAYER_OEDER = ["red", "green", "blue"]

PLAYER_OEDER_DICT = {"red": 0, "green": 1, "blue": 2}

""" keys for information stored in json file """
JSON_FILE_KEYS = ["colour", "pieces", "blocks"]

N_PLAYER = 3
