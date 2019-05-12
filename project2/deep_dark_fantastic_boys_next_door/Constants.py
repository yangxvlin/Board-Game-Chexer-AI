"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:23:57
Description: Constants used in program
"""

""" initial score for players """
INITIAL_SCORE = [0, 0, 0]

""" an empty board """
EMPTY_BOARD = [[], [], []]

""" size of the chexer board """
BOARD_BOUND = 3

""" hexe piece's moving delta """
MOVE_DELTA = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]

PLAYER_PREFERRED_MOVE_DELTA = {0: [(1, -1), (1, 0), (0, -1), (0, 1), (-1, 1), (-1, 0)],
                               1: [(-1, 1), (0, 1), (-1, 0), (1, 0), (0, -1), (1, -1)],
                               2: [(-1, 0), (0, -1), (1, -1), (-1, 1), (1, 0), (0, 1)]}

""" move action """
MOVE = "MOVE"

""" jump action """
JUMP = "JUMP"

""" exit action """
EXIT = "EXIT"

PASS = "PASS"

PASS_ACTION = ("PASS", None)

""" player win when 4 pieces exit """
PLAYER_WIN_THRESHOLD = 4

""" max number of game turns """
MAX_TURN = 256

""" map player string with player playing order """
PLAYER_PLAYING_ORDER = {"red": 0, "green": 1, "blue": 2}

""" player index playing order """
PLAYER_ORDER = [0, 1, 2]

""" player playing order with map player string """
PLAYING_ORDER_PLAYER_MAP = {0: "red", 1: "green", 2: "blue"}

""" each player's goal hexes' axial coordinates """
PLAYER_GOAL = {0: [(BOARD_BOUND, -i) for i in range(0, PLAYER_WIN_THRESHOLD)],
               1: [(i-BOARD_BOUND, BOARD_BOUND)
                   for i in range(0, PLAYER_WIN_THRESHOLD)],
               2: [(-i, i-BOARD_BOUND) for i in range(0, PLAYER_WIN_THRESHOLD)]}

""" number of players in game """
N_PLAYER = 3

OPEN_GAME_TURN_LIMIT = 3

# TODO solitary at higher position (closer/far away) from origin
""" {player: {turn: action}} """
OPEN_GAME_AGENT = {0: {0: (MOVE, ((-3, 0), (-2, 0))),
                       1: (MOVE, ((-2, 0), (-2, 1))),
                       2: (MOVE, ((-3, 3), (-2, 2)))},
                   1: {0: (MOVE, ((0, -3), (0, -2))),
                       1: (MOVE, ((0, -2), (1, -2))),
                       2: (MOVE, ((3, -3), (2, -2)))},
                   2: {0: (MOVE, ((0,  3), (0,  2))),
                       1: (MOVE, ((3,  0), (2,  0))),
                       2: (MOVE, ((2,  0), (1,  1)))}}

NEGATIVE_INFINITY = float('-inf')
