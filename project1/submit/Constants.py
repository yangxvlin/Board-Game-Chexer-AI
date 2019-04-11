"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:23:57
Description: Constants used in program
"""

""" an empty board """
EMPTY_BOARD = [[], [], []]

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

""" map player string with player playing order """
PLAYER_PLAYING_ORDER = {"red": 0, "green": 1, "blue": 2}

""" player playing order with map player string """
PLAYING_ORDER_PLAYER_MAP = {0: "red", 1: "green", 2: "blue"}

""" each player's goal hexes' axial coordinates """
PLAYER_GOAL = {0: set([(BOARD_BOUND, -i) for i in range(0, PLAYER_WIN_THRESHOLD)]),
               1: set([(i-BOARD_BOUND, BOARD_BOUND)
                   for i in range(0, PLAYER_WIN_THRESHOLD)]),
               2: set([(-i, i-BOARD_BOUND) for i in range(0, PLAYER_WIN_THRESHOLD)])}

""" keys for information stored in json file """
JSON_FILE_KEYS = ["colour", "pieces", "blocks"]
